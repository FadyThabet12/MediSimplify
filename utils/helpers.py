import re

def contains_arabic(text):
    """Check if text contains Arabic characters"""
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]', str(text)))

def process_prediction(result_df, threshold=0.5):
    """
    Convert raw multi-label predictions into user-facing findings.
    No Finding is displayed only when no other finding crosses threshold.
    """
    df = result_df.copy()
    
    # All findings except No Finding
    disease_df = df[df["Finding"] != "No Finding"].copy()
    positive_diseases = disease_df[disease_df["Score"] >= threshold].copy()
    
    if len(positive_diseases) == 0:
        final_findings = df[df["Finding"] == "No Finding"].copy()
        final_status = "No significant finding detected"
    else:
        final_findings = positive_diseases.sort_values("Score", ascending=False)
        final_status = "Potential findings detected"
    
    return {
        "status": final_status,
        "findings": final_findings,
        "raw": df
    }