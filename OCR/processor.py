# OCR/processor.py
import re
import html
from bs4 import BeautifulSoup
from jiwer import wer, cer
from collections import Counter

class SuryaProcessor:
    
    @staticmethod
    def html_to_text(raw_html):
        """
        Converts the raw HTML output from Surya into clean, readable text.
        """
        if not raw_html:
            return ""
        
        s = str(raw_html).strip()
        # Remove markdown code blocks if they exist
        s = re.sub(r"^```(?:html)?\s*", "", s, flags=re.I)
        s = re.sub(r"\s*```$", "", s)
        
        soup = BeautifulSoup(s, "html.parser")

        # Convert <br> to newlines
        for br in soup.find_all("br"):
            br.replace_with("\n")

        # Add spacing around table cells to avoid concatenated words
        for cell in soup.find_all(["td", "th"]):
            cell.insert_before(" ")
            cell.insert_after(" ")

        text = soup.get_text("\n")
        text = html.unescape(text)
        # Collapse extra whitespace and empty lines
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @staticmethod
    def clean_for_metric(s):
        """Standardize text for CER/WER calculation."""
        s = str(s or "").lower()
        s = re.sub(r"\s+", " ", s).strip()
        return s

    @staticmethod
    def numeric_tokens(s):
        """Extract medical numeric values (e.g., 120/80, 98.6F, 5mg)."""
        return re.findall(
            r"(?<![A-Za-z])\d+(?:[.,]\d+)*(?:%|[A-Za-z]+)?", 
            str(s or "")
        )

    @staticmethod
    def calculate_numeric_recall(gt, pred):
        """Calculates recall of numerical values in the prediction."""
        gt_nums = [x.lower() for x in SuryaProcessor.numeric_tokens(gt)]
        pred_nums = [x.lower() for x in SuryaProcessor.numeric_tokens(pred)]

        if not gt_nums:
            return None

        counts = Counter(pred_nums)
        hits = 0

        for token in gt_nums:
            if counts[token] > 0:
                hits += 1
                counts[token] -= 1

        return hits / len(gt_nums)

    @staticmethod
    def evaluate_predictions(df_results):
        """
        Takes a pandas DataFrame with 'ground_truth' and 'prediction' columns.
        Returns the same DataFrame with 'CER', 'WER', and 'numeric_recall' added.
        """
        # Apply cleaning
        df_results["gt_metric"] = df_results["ground_truth"].map(SuryaProcessor.clean_for_metric)
        df_results["pred_metric"] = df_results["prediction"].map(SuryaProcessor.clean_for_metric)

        # Calculate Metrics
        df_results["CER"] = [
            cer(a, b) 
            for a, b in zip(df_results["gt_metric"], df_results["pred_metric"])
        ]
        
        df_results["WER"] = [
            wer(a, b) 
            for a, b in zip(df_results["gt_metric"], df_results["pred_metric"])
        ]

        df_results["numeric_recall"] = [
            SuryaProcessor.calculate_numeric_recall(a, b)
            for a, b in zip(df_results["ground_truth"], df_results["prediction"])
        ]

        return df_results