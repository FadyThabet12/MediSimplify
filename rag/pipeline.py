import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from config import TRANSLATION_MODEL, LLM_MODEL, DEVICE
from utils.helpers import contains_arabic
from rag.retrieval import MedicalRetriever

class MedicalRAGPipeline:
    def __init__(self):
        self.retriever = MedicalRetriever()
        
        # Translation model for Arabic
        self.translation_tokenizer = AutoTokenizer.from_pretrained(TRANSLATION_MODEL)
        self.translation_model = AutoModelForSeq2SeqLM.from_pretrained(TRANSLATION_MODEL).to(DEVICE)
        self.translation_model.eval()
        
        # LLM for answer generation
        self.llm_tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
        self.llm = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL).to(DEVICE)
        self.llm.eval()
    
    def translate_text(self, text, source_lang, target_lang, max_new_tokens=256):
        """Translate text between Arabic and English"""
        self.translation_tokenizer.src_lang = source_lang
        inputs = self.translation_tokenizer(
            str(text),
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
        
        forced_bos_token_id = self.translation_tokenizer.convert_tokens_to_ids(target_lang)
        
        with torch.no_grad():
            outputs = self.translation_model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_new_tokens=max_new_tokens,
                num_beams=4
            )
        
        return self.translation_tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True
        )[0]
    
    def prepare_query(self, question):
        """Prepare query for retrieval (Arabic -> English if needed)"""
        if contains_arabic(question):
            return self.translate_text(question, "arb_Arab", "eng_Latn")
        return question
    
    def translate_answer(self, answer):
        """Translate answer to Arabic if needed"""
        return self.translate_text(answer, "eng_Latn", "arb_Arab")
    
    def build_context(self, results, max_chars_per_doc=1800):
        """Build context from retrieved documents"""
        parts = []
        for i, result in enumerate(results, 1):
            parts.append(
                f"[Medical Source {i}]\n"
                f"Title: {result['title']}\n"
                f"Source: {result['source']}\n"
                f"Content: {str(result['text'])[:max_chars_per_doc]}"
            )
        return "\n\n".join(parts)
    
    def generate_answer(self, question, results, answer_in_arabic=False, max_new_tokens=220):
        """Generate patient-friendly answer"""
        context = self.build_context(results)
        
        prompt = (
            "You are a medical information assistant.\n\n"
            "Use the retrieved medical sources as your evidence.\n"
            "Do not diagnose the patient.\n"
            "Do not invent facts.\n"
            "Explain medical terms in simple language.\n"
            "Do not prescribe medication or create a personalized treatment plan.\n"
            "If the context is insufficient, say so.\n"
            "Encourage professional medical evaluation when appropriate.\n\n"
            f"Retrieved medical sources:\n{context}\n\n"
            f"User question:\n{question}\n\n"
            "Patient-friendly answer:"
        )
        
        inputs = self.llm_tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )
        inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
        
        with torch.no_grad():
            outputs = self.llm.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                num_beams=4,
                early_stopping=True
            )
        
        answer = self.llm_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if answer_in_arabic:
            answer = self.translate_answer(answer)
        
        return answer
    
    def answer(self, question, k=5):
        """Complete RAG pipeline"""
        is_arabic = contains_arabic(question)
        retrieval_query = self.prepare_query(question)
        
        results = self.retriever.retrieve(retrieval_query, k)
        answer = self.generate_answer(retrieval_query, results, answer_in_arabic=is_arabic)
        
        return {
            "question": question,
            "retrieval_query": retrieval_query,
            "answer": answer,
            "language": "ar" if is_arabic else "en",
            "sources": results
        }