from typing import Dict, Any, List
from .base_agent import BaseAgent
from config import Config
import asyncio

class VerificationAgent(BaseAgent):
    """Verification Agent performs adaptive multi-layer eKYC verification"""
    
    def __init__(self):
        super().__init__(
            agent_name="VerificationAgent",
            system_prompt="""You are a Verification Agent responsible for multi-layer eKYC verification.
            Your role includes:
            1. OCR processing of documents
            2. Selfie matching with ID documents
            3. OTP validation
            4. Fraud detection
            5. IP and liveliness checks
            
            Determine verification confidence scores and flag suspicious activities."""
        )
    
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process verification with adaptive multi-layer KYC"""
        documents = context.get("documents", [])
        customer_data = context.get("customer_data", {})
        risk_level = context.get("risk_level", "medium")
        
        # Determine verification requirements based on risk level
        verification_steps = self._get_verification_steps(risk_level)
        
        # Execute verification steps
        results = {}
        
        # Step 1: Document OCR
        if "ocr" in verification_steps:
            ocr_result = await self._perform_ocr(documents)
            results["ocr"] = ocr_result
        
        # Step 2: OTP Validation
        if "otp" in verification_steps:
            otp_result = await self._validate_otp(customer_data.get("otp_code"), customer_data.get("phone"))
            results["otp"] = otp_result
        
        # Step 3: Selfie Match
        if "selfie" in verification_steps:
            selfie_result = await self._match_selfie(documents, customer_data.get("selfie_image"))
            results["selfie"] = selfie_result
        
        # Step 4: Fraud Check
        if "fraud_check" in verification_steps:
            fraud_result = await self._fraud_detection(customer_data, documents)
            results["fraud_check"] = fraud_result
        
        # Step 5: IP and Liveliness Check
        if "ip_liveliness" in verification_steps:
            ip_result = await self._ip_liveliness_check(customer_data)
            results["ip_liveliness"] = ip_result
        
        # Calculate overall confidence score
        confidence_score = self._calculate_confidence_score(results, risk_level)
        
        result = {
            "verification_steps": verification_steps,
            "results": results,
            "confidence_score": confidence_score,
            "risk_level": risk_level,
            "status": "verified" if confidence_score >= Config.VERIFICATION_CONFIDENCE_HIGH else "needs_review"
        }
        
        self.log_action("Verification Processing", result)
        return result
    
    def _get_verification_steps(self, risk_level: str) -> List[str]:
        """Get required verification steps based on risk level"""
        if risk_level == "low":
            return ["ocr", "otp"]
        elif risk_level == "medium":
            return ["ocr", "otp", "selfie"]
        else:  # high risk
            return ["ocr", "otp", "selfie", "fraud_check", "ip_liveliness"]
    
    async def _perform_ocr(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform OCR on uploaded documents using Google Vision API"""
        # Placeholder - would integrate with Google Vision API
        ocr_results = {}
        
        for doc in documents:
            doc_type = doc.get("type", "unknown")
            doc_url = doc.get("url", "")
            
            # Simulate OCR processing
            ocr_results[doc_type] = {
                "extracted_text": f"Extracted text from {doc_type}",
                "fields": {
                    "name": "John Doe",
                    "dob": "1990-01-01",
                    "address": "123 Main St",
                    "id_number": "ABCD123456"
                },
                "confidence": 0.92
            }
        
        return {
            "status": "success",
            "results": ocr_results,
            "confidence": 0.92
        }
    
    async def _validate_otp(self, otp_code: str, phone: str) -> Dict[str, Any]:
        """Validate OTP sent to customer phone"""
        # Placeholder - would integrate with Twilio or Firebase Auth
        # In real implementation, verify OTP against stored value
        
        if otp_code and len(otp_code) == 6:
            return {
                "status": "verified",
                "phone": phone,
                "confidence": 0.95
            }
        else:
            return {
                "status": "failed",
                "phone": phone,
                "confidence": 0.0
            }
    
    async def _match_selfie(self, documents: List[Dict[str, Any]], selfie_image: str) -> Dict[str, Any]:
        """Match selfie with ID document photo using AWS Rekognition"""
        # Placeholder - would integrate with AWS Rekognition
        
        # Find ID document (Aadhaar, PAN, etc.)
        id_document = next((doc for doc in documents if doc.get("type") in ["aadhaar", "pan", "passport"]), None)
        
        if id_document and selfie_image:
            # Simulate face matching
            match_confidence = 0.88  # Would be actual Rekognition result
            
            return {
                "status": "matched" if match_confidence > 0.80 else "not_matched",
                "confidence": match_confidence,
                "threshold": 0.80
            }
        else:
            return {
                "status": "failed",
                "confidence": 0.0,
                "reason": "Missing selfie or ID document"
            }
    
    async def _fraud_detection(self, customer_data: Dict[str, Any], documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform fraud detection checks"""
        fraud_indicators = []
        fraud_score = 0.0
        
        # Check for duplicate applications
        # Check document authenticity
        # Check for suspicious patterns
        
        # Placeholder fraud detection logic
        if customer_data.get("phone") and len(customer_data.get("phone", "")) != 10:
            fraud_indicators.append("Invalid phone number")
            fraud_score += 0.2
        
        # Check IP address (would check against known fraud IPs)
        ip_address = customer_data.get("ip_address", "")
        if ip_address:
            # Placeholder check
            fraud_score += 0.1
        
        return {
            "fraud_score": fraud_score,
            "indicators": fraud_indicators,
            "status": "clean" if fraud_score < 0.3 else "suspicious",
            "requires_review": fraud_score >= 0.3
        }
    
    async def _ip_liveliness_check(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check IP address and perform liveliness detection"""
        ip_address = customer_data.get("ip_address", "")
        
        # Placeholder IP check
        ip_risk = 0.1  # Would check against known VPN/proxy/fraud IP databases
        
        # Liveliness check (would use face detection to ensure person is alive)
        liveliness_score = 0.95  # Placeholder
        
        return {
            "ip_address": ip_address,
            "ip_risk": ip_risk,
            "liveliness_score": liveliness_score,
            "status": "passed" if ip_risk < 0.3 and liveliness_score > 0.8 else "failed"
        }
    
    def _calculate_confidence_score(self, results: Dict[str, Any], risk_level: str) -> float:
        """Calculate overall verification confidence score"""
        weights = {
            "low": {"ocr": 0.4, "otp": 0.6},
            "medium": {"ocr": 0.3, "otp": 0.3, "selfie": 0.4},
            "high": {"ocr": 0.2, "otp": 0.2, "selfie": 0.25, "fraud_check": 0.2, "ip_liveliness": 0.15}
        }
        
        weight_map = weights.get(risk_level, weights["medium"])
        total_score = 0.0
        
        for step, weight in weight_map.items():
            step_result = results.get(step, {})
            step_confidence = step_result.get("confidence", 0.0)
            total_score += step_confidence * weight
        
        return round(total_score, 2)

