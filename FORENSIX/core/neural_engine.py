import math
import re

class NeuralEngine:
    """
    The 'AI' Brain of Forensix Sentinel.
    Uses heuristic scoring and basic anomaly detection to classify threats.
    """
    def __init__(self):
        # Weights for our scoring model
        self.weights = {
            'entropy': 2.5,
            'hidden_strings': 1.5,
            'suspicious_header': 5.0,
            'embedded_files': 3.0,
            'known_bad_signature': 10.0
        }

    def score_artifact(self, entropy, findings, file_type):
        """
        Returns a Threat Score (0-100) and AI Assessment.
        """
        score = 0.0
        details = []

        # 1. Entropy Analysis (2.5x)
        # Normal text is ~4.5. Encrypted/Compressed is ~7.9.
        if entropy > 7.2:
            score += (entropy - 7.0) * 10 * self.weights['entropy']
            details.append("High Entropy (Compression/Encryption)")
        elif entropy < 2.0:
            details.append("Low Entropy (Padding/Text)")

        # 2. Heuristic Pattern Matching
        bad_keywords = ["password", "admin", "root", "token", "key", "flag", "ctf"]
        detected_keywords = set()
        
        # Parse list of findings from other modules
        for finding in findings:
            finding_lower = finding.lower()
            
            # Critical Flags
            if "flag" in finding_lower or "ctf" in finding_lower:
                score += 50
                details.append("CONFIRMED FLAG ARTIFACT")
                
            # Stego detections
            if "steghide" in finding_lower or "zsteg" in finding_lower:
                score += 20 * self.weights['embedded_files']
                details.append("Steganography Tool Signature")
                
            # Volatility detections
            if "volatility" in finding_lower:
                score += 15
                details.append("Memory Image Artifact")

        # 3. Anomaly Detection based on type
        if "image" in file_type and entropy > 7.95:
             score += 30
             details.append("Abnormal Image Entropy (Likely Payload)")

        # Cap score
        score = min(100, score)
        
        assessment = "SAFE"
        if score > 80: assessment = "CRITICAL THREAT"
        elif score > 50: assessment = "SUSPICIOUS"
        elif score > 20: assessment = "INTERESTING"

        return {
            "score": round(score, 1),
            "assessment": assessment,
            "ai_notes": details
        }
