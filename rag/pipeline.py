# # import torch
# # from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# # from config import TRANSLATION_MODEL, LLM_MODEL, DEVICE
# # from utils.helpers import contains_arabic
# # from rag.retrieval import MedicalRetriever

# # class MedicalRAGPipeline:
# #     def __init__(self):
# #         self.retriever = MedicalRetriever()
        
# #         # Translation model for Arabic
# #         self.translation_tokenizer = AutoTokenizer.from_pretrained(TRANSLATION_MODEL)
# #         self.translation_model = AutoModelForSeq2SeqLM.from_pretrained(TRANSLATION_MODEL).to(DEVICE)
# #         self.translation_model.eval()
        
# #         # LLM for answer generation
# #         self.llm_tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
# #         self.llm = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL).to(DEVICE)
# #         self.llm.eval()
    
# #     def translate_text(self, text, source_lang, target_lang, max_new_tokens=256):
# #         """Translate text between Arabic and English"""
# #         self.translation_tokenizer.src_lang = source_lang
# #         inputs = self.translation_tokenizer(
# #             str(text),
# #             return_tensors="pt",
# #             truncation=True,
# #             max_length=512
# #         )
# #         inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
        
# #         forced_bos_token_id = self.translation_tokenizer.convert_tokens_to_ids(target_lang)
        
# #         with torch.no_grad():
# #             outputs = self.translation_model.generate(
# #                 **inputs,
# #                 forced_bos_token_id=forced_bos_token_id,
# #                 max_new_tokens=max_new_tokens,
# #                 num_beams=4
# #             )
        
# #         return self.translation_tokenizer.batch_decode(
# #             outputs,
# #             skip_special_tokens=True
# #         )[0]
    
# #     def prepare_query(self, question):
# #         """Prepare query for retrieval (Arabic -> English if needed)"""
# #         if contains_arabic(question):
# #             return self.translate_text(question, "arb_Arab", "eng_Latn")
# #         return question
    
# #     def translate_answer(self, answer):
# #         """Translate answer to Arabic if needed"""
# #         return self.translate_text(answer, "eng_Latn", "arb_Arab")
    
# #     def build_context(self, results, max_chars_per_doc=1800):
# #         """Build context from retrieved documents"""
# #         parts = []
# #         for i, result in enumerate(results, 1):
# #             parts.append(
# #                 f"[Medical Source {i}]\n"
# #                 f"Title: {result['title']}\n"
# #                 f"Source: {result['source']}\n"
# #                 f"Content: {str(result['text'])[:max_chars_per_doc]}"
# #             )
# #         return "\n\n".join(parts)
    
# #     def generate_answer(self, question, results, answer_in_arabic=False, max_new_tokens=220):
# #         """Generate patient-friendly answer"""
# #         context = self.build_context(results)
        
# #         prompt = (
# #             "You are a medical information assistant.\n\n"
# #             "Use the retrieved medical sources as your evidence.\n"
# #             "Do not diagnose the patient.\n"
# #             "Do not invent facts.\n"
# #             "Explain medical terms in simple language.\n"
# #             "Do not prescribe medication or create a personalized treatment plan.\n"
# #             "If the context is insufficient, say so.\n"
# #             "Encourage professional medical evaluation when appropriate.\n\n"
# #             f"Retrieved medical sources:\n{context}\n\n"
# #             f"User question:\n{question}\n\n"
# #             "Patient-friendly answer:"
# #         )
        
# #         inputs = self.llm_tokenizer(
# #             prompt,
# #             return_tensors="pt",
# #             truncation=True,
# #             max_length=1024
# #         )
# #         inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
        
# #         with torch.no_grad():
# #             outputs = self.llm.generate(
# #                 **inputs,
# #                 max_new_tokens=max_new_tokens,
# #                 num_beams=4,
# #                 early_stopping=True
# #             )
        
# #         answer = self.llm_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
# #         if answer_in_arabic:
# #             answer = self.translate_answer(answer)
        
# #         return answer
    
# #     def answer(self, question, k=5):
# #         """Complete RAG pipeline"""
# #         is_arabic = contains_arabic(question)
# #         retrieval_query = self.prepare_query(question)
        
# #         results = self.retriever.retrieve(retrieval_query, k)
# #         answer = self.generate_answer(retrieval_query, results, answer_in_arabic=is_arabic)
        
# #         return {
# #             "question": question,
# #             "retrieval_query": retrieval_query,
# #             "answer": answer,
# #             "language": "ar" if is_arabic else "en",
# #             "sources": results
# #         }
# import torch
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, M2M100Tokenizer
# from config import TRANSLATION_MODEL, LLM_MODEL, DEVICE
# from utils.helpers import contains_arabic
# from rag.retrieval import MedicalRetriever

# class MedicalRAGPipeline:
#     def __init__(self):
#         self.retriever = MedicalRetriever()
        
#         # Translation model for Arabic (M2M100)
#         try:
#             self.translation_tokenizer = M2M100Tokenizer.from_pretrained(TRANSLATION_MODEL)
#             self.translation_model = AutoModelForSeq2SeqLM.from_pretrained(TRANSLATION_MODEL).to(DEVICE)
#             self.translation_model.eval()
#             self.translation_available = True
#         except Exception as e:
#             print(f"Translation model not available: {e}")
#             self.translation_tokenizer = None
#             self.translation_model = None
#             self.translation_available = False
        
#         # LLM for answer generation
#         self.llm_tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
#         self.llm = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL).to(DEVICE)
#         self.llm.eval()
    
#     def translate_text(self, text, source_lang, target_lang, max_new_tokens=256):
#         """Translate text between Arabic and English using M2M100"""
#         if not self.translation_available:
#             return text
        
#         # M2M100 uses language codes like 'ar' and 'en'
#         lang_map = {
#             'arb_Arab': 'ar',
#             'eng_Latn': 'en'
#         }
        
#         src = lang_map.get(source_lang, 'ar')
#         tgt = lang_map.get(target_lang, 'en')
        
#         self.translation_tokenizer.src_lang = src
#         inputs = self.translation_tokenizer(
#             str(text),
#             return_tensors="pt",
#             truncation=True,
#             max_length=512
#         )
#         inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
        
#         with torch.no_grad():
#             outputs = self.translation_model.generate(
#                 **inputs,
#                 forced_bos_token_id=self.translation_tokenizer.get_lang_id(tgt),
#                 max_new_tokens=max_new_tokens,
#                 num_beams=4
#             )
        
#         return self.translation_tokenizer.batch_decode(
#             outputs,
#             skip_special_tokens=True
#         )[0]
    
#     def prepare_query(self, question):
#         """Prepare query for retrieval (Arabic -> English if needed)"""
#         if contains_arabic(question):
#             return self.translate_text(question, "arb_Arab", "eng_Latn")
#         return question
    
#     def translate_answer(self, answer):
#         """Translate answer to Arabic if needed"""
#         return self.translate_text(answer, "eng_Latn", "arb_Arab")
    
#     def build_context(self, results, max_chars_per_doc=1800):
#         """Build context from retrieved documents"""
#         parts = []
#         for i, result in enumerate(results, 1):
#             parts.append(
#                 f"[Medical Source {i}]\n"
#                 f"Title: {result['title']}\n"
#                 f"Source: {result['source']}\n"
#                 f"Content: {str(result['text'])[:max_chars_per_doc]}"
#             )
#         return "\n\n".join(parts)
    
#     def generate_answer(self, question, results, answer_in_arabic=False, max_new_tokens=220):
#         """Generate patient-friendly answer"""
#         context = self.build_context(results)
        
#         prompt = (
#             "You are a medical information assistant.\n\n"
#             "Use the retrieved medical sources as your evidence.\n"
#             "Do not diagnose the patient.\n"
#             "Do not invent facts.\n"
#             "Explain medical terms in simple language.\n"
#             "Do not prescribe medication or create a personalized treatment plan.\n"
#             "If the context is insufficient, say so.\n"
#             "Encourage professional medical evaluation when appropriate.\n\n"
#             f"Retrieved medical sources:\n{context}\n\n"
#             f"User question:\n{question}\n\n"
#             "Patient-friendly answer:"
#         )
        
#         inputs = self.llm_tokenizer(
#             prompt,
#             return_tensors="pt",
#             truncation=True,
#             max_length=1024
#         )
#         inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
        
#         with torch.no_grad():
#             outputs = self.llm.generate(
#                 **inputs,
#                 max_new_tokens=max_new_tokens,
#                 num_beams=4,
#                 early_stopping=True
#             )
        
#         answer = self.llm_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
#         if answer_in_arabic and self.translation_available:
#             answer = self.translate_answer(answer)
        
#         return answer
    
#     def answer(self, question, k=5):
#         """Complete RAG pipeline"""
#         is_arabic = contains_arabic(question)
#         retrieval_query = self.prepare_query(question)
        
#         results = self.retriever.retrieve(retrieval_query, k)
#         answer = self.generate_answer(retrieval_query, results, answer_in_arabic=is_arabic)
        
#         return {
#             "question": question,
#             "retrieval_query": retrieval_query,
#             "answer": answer,
#             "language": "ar" if is_arabic else "en",
#             "sources": results
#         } 
# import torch
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# from config import TRANSLATION_MODEL, LLM_MODEL, DEVICE
# from utils.helpers import contains_arabic
# from rag.retrieval import MedicalRetriever
# from rag.embeddings import QueryEncoder  # ← import صح

# class MedicalRAGPipeline:
#     def __init__(self):
#         self.retriever = MedicalRetriever()
        
#         # Translation model for Arabic
#         try:
#             self.translation_tokenizer = AutoTokenizer.from_pretrained(TRANSLATION_MODEL)
#             self.translation_model = AutoModelForSeq2SeqLM.from_pretrained(TRANSLATION_MODEL).to(DEVICE)
#             self.translation_model.eval()
#             self.translation_available = True
#         except Exception as e:
#             print(f"Translation model not available: {e}")
#             self.translation_tokenizer = None
#             self.translation_model = None
#             self.translation_available = False
        
#         # LLM for answer generation
#         self.llm_tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
#         self.llm = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL).to(DEVICE)
#         self.llm.eval()
    
#     def translate_text(self, text, source_lang, target_lang, max_new_tokens=256):
#         """Translate text between Arabic and English"""
#         if not self.translation_available:
#             return text
        
#         # Handle different translation models
#         if "m2m100" in TRANSLATION_MODEL:
#             # M2M100 uses 'ar' and 'en'
#             lang_map = {
#                 'arb_Arab': 'ar',
#                 'eng_Latn': 'en'
#             }
#             src = lang_map.get(source_lang, 'ar')
#             tgt = lang_map.get(target_lang, 'en')
            
#             self.translation_tokenizer.src_lang = src
#             inputs = self.translation_tokenizer(
#                 str(text),
#                 return_tensors="pt",
#                 truncation=True,
#                 max_length=512
#             )
#             inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
            
#             with torch.no_grad():
#                 outputs = self.translation_model.generate(
#                     **inputs,
#                     forced_bos_token_id=self.translation_tokenizer.get_lang_id(tgt),
#                     max_new_tokens=max_new_tokens,
#                     num_beams=4
#                 )
#         else:
#             # Fallback for other models
#             inputs = self.translation_tokenizer(
#                 str(text),
#                 return_tensors="pt",
#                 truncation=True,
#                 max_length=512
#             )
#             inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
            
#             with torch.no_grad():
#                 outputs = self.translation_model.generate(
#                     **inputs,
#                     max_new_tokens=max_new_tokens,
#                     num_beams=4
#                 )
        
#         return self.translation_tokenizer.batch_decode(
#             outputs,
#             skip_special_tokens=True
#         )[0]
    
#     def prepare_query(self, question):
#         """Prepare query for retrieval (Arabic -> English if needed)"""
#         if contains_arabic(question):
#             return self.translate_text(question, "arb_Arab", "eng_Latn")
#         return question
    
#     def translate_answer(self, answer):
#         """Translate answer to Arabic if needed"""
#         return self.translate_text(answer, "eng_Latn", "arb_Arab")
    
#     def build_context(self, results, max_chars_per_doc=1800):
#         """Build context from retrieved documents"""
#         parts = []
#         for i, result in enumerate(results, 1):
#             parts.append(
#                 f"[Medical Source {i}]\n"
#                 f"Title: {result['title']}\n"
#                 f"Source: {result['source']}\n"
#                 f"Content: {str(result['text'])[:max_chars_per_doc]}"
#             )
#         return "\n\n".join(parts)
    
#     def generate_answer(self, question, results, answer_in_arabic=False, max_new_tokens=220):
#         """Generate patient-friendly answer"""
#         context = self.build_context(results)
        
#         prompt = (
#             "You are a medical information assistant.\n\n"
#             "Use the retrieved medical sources as your evidence.\n"
#             "Do not diagnose the patient.\n"
#             "Do not invent facts.\n"
#             "Explain medical terms in simple language.\n"
#             "Do not prescribe medication or create a personalized treatment plan.\n"
#             "If the context is insufficient, say so.\n"
#             "Encourage professional medical evaluation when appropriate.\n\n"
#             f"Retrieved medical sources:\n{context}\n\n"
#             f"User question:\n{question}\n\n"
#             "Patient-friendly answer:"
#         )
        
#         inputs = self.llm_tokenizer(
#             prompt,
#             return_tensors="pt",
#             truncation=True,
#             max_length=1024
#         )
#         inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
        
#         with torch.no_grad():
#             outputs = self.llm.generate(
#                 **inputs,
#                 max_new_tokens=max_new_tokens,
#                 num_beams=4,
#                 early_stopping=True
#             )
        
#         answer = self.llm_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
#         if answer_in_arabic and self.translation_available:
#             answer = self.translate_answer(answer)
        
#         return answer
    
#     def answer(self, question, k=5):
#         """Complete RAG pipeline"""
#         is_arabic = contains_arabic(question)
#         retrieval_query = self.prepare_query(question)
        
#         results = self.retriever.retrieve(retrieval_query, k)
#         answer = self.generate_answer(retrieval_query, results, answer_in_arabic=is_arabic)
        
#         return {
#             "question": question,
#             "retrieval_query": retrieval_query,
#             "answer": answer,
#             "language": "ar" if is_arabic else "en",
#             "sources": results
#         }
import torch
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from config import TRANSLATION_MODEL, LLM_MODEL, DEVICE
from utils.helpers import contains_arabic
from rag.retrieval import MedicalRetriever, INTENT_TERMS

class MedicalRAGPipeline:
    def __init__(self):
        self.retriever = MedicalRetriever()
        
        # Translation model for Arabic
        try:
            self.translation_tokenizer = AutoTokenizer.from_pretrained(TRANSLATION_MODEL)
            self.translation_model = AutoModelForSeq2SeqLM.from_pretrained(TRANSLATION_MODEL).to(DEVICE)
            self.translation_model.eval()
            self.translation_available = True
        except Exception as e:
            print(f"Translation model not available: {e}")
            self.translation_tokenizer = None
            self.translation_model = None
            self.translation_available = False
        
        # LLM for answer generation
        self.llm_tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
        self.llm = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL).to(DEVICE)
        self.llm.eval()
    
    def translate_text(self, text, source_lang, target_lang, max_new_tokens=256):
        """Translate text between Arabic and English"""
        if not self.translation_available:
            return text
        
        # Handle different translation models
        if "m2m100" in TRANSLATION_MODEL:
            # M2M100 uses 'ar' and 'en'
            lang_map = {
                'arb_Arab': 'ar',
                'eng_Latn': 'en'
            }
            src = lang_map.get(source_lang, 'ar')
            tgt = lang_map.get(target_lang, 'en')
            
            self.translation_tokenizer.src_lang = src
            inputs = self.translation_tokenizer(
                str(text),
                return_tensors="pt",
                truncation=True,
                max_length=512
            )
            inputs = {key: value.to(DEVICE) for key, value in inputs.items()}
            
            with torch.no_grad():
                outputs = self.translation_model.generate(
                    **inputs,
                    forced_bos_token_id=self.translation_tokenizer.get_lang_id(tgt),
                    max_new_tokens=max_new_tokens,
                    num_beams=4
                )
        else:
            # NLLB model (facebook/nllb-200-distilled-600M)
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
            text = result.get('text', '')
            parts.append(
                f"[Medical Source {i}]\n"
                f"Title: {result['title']}\n"
                f"Content: {str(text)[:max_chars_per_doc]}"
            )
        return "\n\n".join(parts)
    
    def _sentences(self, text):
        """Split text into sentences"""
        if not text:
            return []
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", str(text)) if s.strip()]
    
    def extract_answer_from_evidence(self, question, results, max_sentences=6):
        """Strict, intent-aware extraction from evidence"""
        intent = self.retriever.question_intent(question)
        terms = INTENT_TERMS.get(intent, [])
        candidates = []
        seen = set()
        
        q_words = self.retriever.lexical_tokens(question)
        
        topic_words = {"migraine", "headache", "headaches", "disease", "condition", "disorder"}
        q_words -= topic_words
        
        for source_idx, result in enumerate(results[:5], 1):
            text = result.get("text", "")
            if not text:
                continue
            for sentence in self._sentences(text):
                low = sentence.lower().strip()
                if not low or low in seen or len(low.split()) < 3:
                    continue
                
                intent_hits = [term for term in terms if term in low]
                q_overlap = len(q_words & self.retriever.lexical_tokens(sentence))
                
                # For symptoms, require a real symptom phrase
                if intent == "symptoms":
                    strong_symptom = any(term in low for term in [
                        "sensitivity to light", "sensitivity to sound", "sensitivity to movement",
                        "nausea", "vomiting", "throbbing", "pulsing", "photophobia",
                        "phonophobia", "aura", "visual", "headache", "pain", "weakness",
                        "fever", "rash"
                    ])
                    if not strong_symptom:
                        continue
                    # Reject sentences whose main purpose is prevalence/classification/etiology
                    if any(x in low for x in ["most common", "second most common", "vascular", "benign", "recurring syndrome", "activators", "triggers"]):
                        symptom_phrase_count = sum(1 for x in [
                            "sensitivity", "nausea", "vomiting", "throbbing", "pulsing", 
                            "photophobia", "phonophobia", "aura"
                        ] if x in low)
                        if symptom_phrase_count < 2:
                            continue
                elif intent != "general" and not intent_hits:
                    continue
                
                score = len(intent_hits) * 5 + q_overlap
                candidates.append((score, source_idx, sentence))
                seen.add(low)
        
        candidates.sort(key=lambda x: (-x[0], x[1]))
        selected = []
        for _, _, sentence in candidates:
            if not any(sentence.lower() in x.lower() or x.lower() in sentence.lower() for x in selected):
                selected.append(sentence)
            if len(selected) >= max_sentences:
                break
        
        return " ".join(selected)
    
    def generate_answer(self, question, results, answer_in_arabic=False, max_new_tokens=80):
        """Generate patient-friendly answer using extraction"""
        # Try extraction first
        answer = self.extract_answer_from_evidence(question, results)
        
        # If extraction fails, use FLAN-T5 generation
        if not answer:
            context = self.build_context(results)
            prompt = (
                "Use only the evidence below. Answer ONLY the question. "
                "Do not repeat titles, metadata, prevalence, or unrelated facts. "
                "If the evidence does not answer the question, say: Insufficient evidence.\n\n"
                f"Evidence:\n{context}\n\nQuestion: {question}\nAnswer:"
            )
            inputs = self.llm_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.llm.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    num_beams=4,
                    do_sample=False,
                    early_stopping=True,
                    no_repeat_ngram_size=3
                )
            answer = self.llm_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        
        # Remove common generic FLAN failures
        bad = {
            "symptoms, signs, causes, and risk factors.",
            "symptoms, signs, causes and risk factors.",
            "symptoms signs causes and risk factors."
        }
        if answer.lower() in bad:
            answer = "Insufficient evidence."
        
        if answer_in_arabic and self.translation_available:
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