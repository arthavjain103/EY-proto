from typing import Dict, Any
from .base_agent import BaseAgent
from config import Config
import numpy as np

class UnderwritingAgent(BaseAgent):
    """Underwriting Agent evaluates creditworthiness and risk assessment"""
    
    def __init__(self):
        super().__init__(
            agent_name="UnderwritingAgent",
            system_prompt="""You are an Underwriting Agent responsible for credit risk assessment.
            Your role includes:
            1. Evaluating creditworthiness based on credit score and bureau data
            2. Assessing loan eligibility and EMI affordability
            3. Making approval, rejection, or counter-offer decisions
            4. Calculating risk scores and loan terms
            
            Make data-driven decisions while ensuring responsible lending practices."""
        )
    
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process underwriting decision"""
        credit_score_data = context.get("credit_score", {})
        offer_mart_data = context.get("offer_mart_data", {})
        verification_result = context.get("verification_result", {})
        customer_data = context.get("customer_data", {})
        
        # Extract key metrics
        credit_score = credit_score_data.get("score", 0)
        pre_approval_limit = offer_mart_data.get("pre_approval_limit", 0)
        verification_confidence = verification_result.get("confidence_score", 0)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(
            credit_score,
            verification_confidence,
            customer_data
        )
        
        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)
        
        # Check if salary slip is required
        requires_salary_slip = verification_confidence < Config.VERIFICATION_CONFIDENCE_HIGH
        
        # If salary slip provided, check EMI eligibility
        emi_check = None
        if customer_data.get("salary_slip") and requires_salary_slip:
            emi_check = await self._check_emi_eligibility(customer_data, pre_approval_limit)
        
        # Make final decision
        decision_result = self._make_decision(
            risk_score,
            credit_score,
            pre_approval_limit,
            verification_confidence,
            emi_check,
            customer_data
        )
        
        result = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "credit_score": credit_score,
            "pre_approval_limit": pre_approval_limit,
            "verification_confidence": verification_confidence,
            "requires_salary_slip": requires_salary_slip,
            "emi_check": emi_check,
            "decision": decision_result["decision"],
            "loan_amount": decision_result.get("loan_amount", 0),
            "interest_rate": decision_result.get("interest_rate", 0),
            "tenure_months": decision_result.get("tenure_months", 0),
            "emi_amount": decision_result.get("emi_amount", 0),
            "reason": decision_result.get("reason", ""),
            "counter_offer": decision_result.get("counter_offer")
        }
        
        self.log_action("Underwriting Processing", result)
        return result
    
    def _calculate_risk_score(self, credit_score: int, verification_confidence: float, 
                             customer_data: Dict[str, Any]) -> float:
        """Calculate comprehensive risk score"""
        # Normalize credit score (0-900 scale to 0-1)
        credit_score_norm = credit_score / 900.0
        
        # Weighted risk calculation
        weights = {
            "credit_score": 0.5,
            "verification": 0.3,
            "customer_profile": 0.2
        }
        
        # Credit score component (inverse - higher score = lower risk)
        credit_risk = 1.0 - credit_score_norm
        
        # Verification component (inverse - higher confidence = lower risk)
        verification_risk = 1.0 - verification_confidence
        
        # Customer profile risk (placeholder - would analyze employment, income stability, etc.)
        profile_risk = 0.3  # Default moderate risk
        
        # Calculate weighted risk score
        risk_score = (
            credit_risk * weights["credit_score"] +
            verification_risk * weights["verification"] +
            profile_risk * weights["customer_profile"]
        )
        
        return round(risk_score, 3)
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level based on score"""
        if risk_score <= (1.0 - Config.LOW_RISK_THRESHOLD):
            return "low"
        elif risk_score <= (1.0 - Config.MEDIUM_RISK_THRESHOLD):
            return "medium"
        else:
            return "high"
    
    async def _check_emi_eligibility(self, customer_data: Dict[str, Any], 
                                    requested_amount: float) -> Dict[str, Any]:
        """Check EMI eligibility based on salary slip"""
        salary = customer_data.get("salary", 0)
        salary_slip_data = customer_data.get("salary_slip_data", {})
        
        # Extract salary from salary slip if available
        if salary_slip_data.get("net_salary"):
            salary = salary_slip_data["net_salary"]
        
        if salary == 0:
            return {
                "eligible": False,
                "reason": "Salary information not available"
            }
        
        # Calculate EMI for requested amount (simplified calculation)
        interest_rate = 0.12  # 12% annual
        tenure_years = 5
        tenure_months = tenure_years * 12
        
        # EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)
        monthly_rate = interest_rate / 12
        emi = requested_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months) / \
              (((1 + monthly_rate) ** tenure_months) - 1)
        
        # Check if EMI is less than 50% of salary
        emi_ratio = emi / salary
        eligible = emi_ratio <= Config.EMI_SALARY_RATIO_THRESHOLD
        
        return {
            "eligible": eligible,
            "salary": salary,
            "requested_amount": requested_amount,
            "emi": round(emi, 2),
            "emi_ratio": round(emi_ratio, 3),
            "threshold": Config.EMI_SALARY_RATIO_THRESHOLD,
            "reason": "EMI within acceptable range" if eligible else "EMI exceeds 50% of salary"
        }
    
    def _make_decision(self, risk_score: float, credit_score: int, pre_approval_limit: float,
                      verification_confidence: float, emi_check: Dict[str, Any],
                      customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make final underwriting decision"""
        requested_amount = float(customer_data.get("requested_amount", 0) or pre_approval_limit)
        
        # Decision logic
        if risk_score > 0.7:  # High risk
            return {
                "decision": "reject",
                "reason": "High risk profile based on credit score and verification",
                "loan_amount": 0
            }
        
        elif verification_confidence < Config.VERIFICATION_CONFIDENCE_LOW:
            return {
                "decision": "reject",
                "reason": "Verification confidence too low",
                "loan_amount": 0
            }
        
        elif credit_score < 600:  # Low credit score
            return {
                "decision": "reject",
                "reason": "Credit score below minimum threshold",
                "loan_amount": 0
            }
        
        # Check EMI eligibility if salary slip was required
        if emi_check:
            if not emi_check.get("eligible"):
                # Offer counter-offer with lower amount
                eligible_amount = self._calculate_eligible_amount(
                    emi_check.get("salary", 0),
                    customer_data
                )
                
                if eligible_amount > 0:
                    return {
                        "decision": "counter_offer",
                        "loan_amount": eligible_amount,
                        "interest_rate": 0.12,
                        "tenure_months": 60,
                        "emi_amount": self._calculate_emi(eligible_amount, 0.12, 60),
                        "reason": f"Requested amount results in high EMI. Counter-offer: ₹{eligible_amount:,.0f}",
                        "counter_offer": {
                            "original_amount": requested_amount,
                            "offered_amount": eligible_amount,
                            "reason": "EMI affordability"
                        }
                    }
                else:
                    return {
                        "decision": "reject",
                        "reason": "Salary insufficient for loan eligibility",
                        "loan_amount": 0
                    }
        
        # Approval decision
        # Cap loan amount at pre-approval limit
        approved_amount = min(requested_amount, pre_approval_limit)
        
        # Determine interest rate based on risk
        if risk_score <= 0.3:
            interest_rate = 0.10  # 10% for low risk
        elif risk_score <= 0.5:
            interest_rate = 0.12  # 12% for medium risk
        else:
            interest_rate = 0.15  # 15% for higher risk
        
        tenure_months = 60  # 5 years default
        
        return {
            "decision": "approve",
            "loan_amount": approved_amount,
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
            "emi_amount": self._calculate_emi(approved_amount, interest_rate, tenure_months),
            "reason": "Approved based on credit score, verification, and eligibility"
        }
    
    def _calculate_eligible_amount(self, salary: float, customer_data: Dict[str, Any]) -> float:
        """Calculate maximum eligible loan amount based on salary"""
        # Maximum EMI = 50% of salary
        max_emi = salary * Config.EMI_SALARY_RATIO_THRESHOLD
        
        # Calculate loan amount for given EMI (reverse EMI calculation)
        interest_rate = 0.12
        tenure_months = 60
        monthly_rate = interest_rate / 12
        
        # Reverse EMI formula
        loan_amount = max_emi * (((1 + monthly_rate) ** tenure_months) - 1) / \
                     (monthly_rate * ((1 + monthly_rate) ** tenure_months))
        
        return round(loan_amount, 0)
    
    def _calculate_emi(self, principal: float, interest_rate: float, tenure_months: int) -> float:
        """Calculate EMI amount"""
        monthly_rate = interest_rate / 12
        emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / \
              (((1 + monthly_rate) ** tenure_months) - 1)
        return round(emi, 2)

