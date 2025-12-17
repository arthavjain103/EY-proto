from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from .base_agent import BaseAgent
from .sales_agent import SalesAgent
from .verification_agent import VerificationAgent
from .underwriting_agent import UnderwritingAgent
from .sanction_agent import SanctionLetterAgent
import asyncio

class MasterAgent(BaseAgent):
    """Master Agent that orchestrates all worker agents"""
    
    def __init__(self):
        super().__init__(
            agent_name="MasterAgent",
            system_prompt="""You are the Master Agent orchestrating a loan processing workflow.
            Your role is to coordinate Sales, Verification, Underwriting, and Sanction agents.
            Make intelligent routing decisions based on customer context and risk levels."""
        )
        
        # Initialize worker agents
        self.sales_agent = SalesAgent()
        self.verification_agent = VerificationAgent()
        self.underwriting_agent = UnderwritingAgent()
        self.sanction_agent = SanctionLetterAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(dict)
        
        # Define nodes
        workflow.add_node("entry", self._entry_point)
        workflow.add_node("sales", self._sales_processing)
        workflow.add_node("emergency_check", self._emergency_check)
        workflow.add_node("parallel_verification", self._parallel_verification)
        workflow.add_node("risk_assessment", self._risk_assessment)
        workflow.add_node("underwriting", self._underwriting_processing)
        workflow.add_node("decision", self._final_decision)
        workflow.add_node("sanction", self._sanction_processing)
        workflow.add_node("feedback", self._feedback_learning)
        
        # Define edges
        workflow.set_entry_point("entry")
        workflow.add_edge("entry", "sales")
        workflow.add_conditional_edges(
            "sales",
            self._route_after_sales,
            {
                "interested": "emergency_check",
                "not_interested": END,
                "objection": "sales"
            }
        )
        workflow.add_conditional_edges(
            "emergency_check",
            self._route_emergency,
            {
                "emergency": "parallel_verification",
                "normal": "risk_assessment"
            }
        )
        workflow.add_edge("risk_assessment", "parallel_verification")
        workflow.add_edge("parallel_verification", "underwriting")
        workflow.add_edge("underwriting", "decision")
        workflow.add_conditional_edges(
            "decision",
            self._route_decision,
            {
                "approve": "sanction",
                "counter_offer": "sanction",
                "reject": END
            }
        )
        workflow.add_edge("sanction", "feedback")
        workflow.add_edge("feedback", END)
        
        return workflow.compile()
    
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process customer request through the workflow"""
        initial_state = {
            "customer_id": context.get("customer_id"),
            "message": context.get("message", ""),
            "documents": context.get("documents", []),
            "customer_data": context.get("customer_data", {}),
            "status": "processing",
            "history": []
        }
        
        result = await self.workflow.ainvoke(initial_state)
        return result
    
    async def _entry_point(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Entry point for customer requests"""
        state["history"].append({"step": "entry", "action": "Customer entry received"})
        return state
    
    async def _sales_processing(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process through Sales Agent"""
        sales_result = await self.sales_agent.process({
            "message": state.get("message", ""),
            "customer_data": state.get("customer_data", {})
        })
        
        state["sales_result"] = sales_result
        state["history"].append({"step": "sales", "result": sales_result})
        return state
    
    def _route_after_sales(self, state: Dict[str, Any]) -> str:
        """Route after sales processing"""
        sales_result = state.get("sales_result", {})
        if sales_result.get("objection_detected"):
            return "objection"
        elif sales_result.get("interested"):
            return "interested"
        else:
            return "not_interested"
    
    async def _emergency_check(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Check for emergency cases"""
        message = state.get("message", "").lower()
        emergency_keywords = ["urgent", "emergency", "immediate", "asap", "critical"]
        is_emergency = any(keyword in message for keyword in emergency_keywords)
        
        state["is_emergency"] = is_emergency
        state["history"].append({"step": "emergency_check", "is_emergency": is_emergency})
        return state
    
    def _route_emergency(self, state: Dict[str, Any]) -> str:
        """Route based on emergency status"""
        return "emergency" if state.get("is_emergency") else "normal"
    
    async def _risk_assessment(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Preliminary risk assessment"""
        # This would integrate with credit bureau for initial scoring
        state["preliminary_risk_score"] = 0.6  # Placeholder
        state["history"].append({"step": "risk_assessment", "score": state["preliminary_risk_score"]})
        return state
    
    async def _parallel_verification(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parallel verification processes"""
        customer_data = state.get("customer_data", {})
        documents = state.get("documents", [])
        
        # Parallel execution
        tasks = [
            self._get_credit_score(customer_data),
            self._get_offer_mart_data(customer_data),
            self.verification_agent.process({
                "documents": documents,
                "customer_data": customer_data,
                "risk_level": state.get("risk_level", "medium")
            })
        ]
        
        credit_score, offer_mart, verification = await asyncio.gather(*tasks)
        
        state["credit_score"] = credit_score
        state["offer_mart_data"] = offer_mart
        state["verification_result"] = verification
        state["history"].append({"step": "parallel_verification", "completed": True})
        
        return state
    
    async def _get_credit_score(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get credit score from Credit Bureau API"""
        # Placeholder - would integrate with actual API
        return {"score": 750, "out_of": 900, "status": "good"}
    
    async def _get_offer_mart_data(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get pre-approval data from Offer Mart API"""
        # Placeholder - would integrate with actual API
        return {"pre_approval_limit": 500000, "eligibility": True}
    
    async def _underwriting_processing(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process through Underwriting Agent"""
        underwriting_result = await self.underwriting_agent.process({
            "credit_score": state.get("credit_score", {}),
            "offer_mart_data": state.get("offer_mart_data", {}),
            "verification_result": state.get("verification_result", {}),
            "customer_data": state.get("customer_data", {})
        })
        
        state["underwriting_result"] = underwriting_result
        state["history"].append({"step": "underwriting", "result": underwriting_result})
        return state
    
    def _route_decision(self, state: Dict[str, Any]) -> str:
        """Route based on underwriting decision"""
        decision = state.get("underwriting_result", {}).get("decision", "reject")
        return decision
    
    async def _final_decision(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Final decision processing"""
        underwriting = state.get("underwriting_result", {})
        state["final_decision"] = underwriting.get("decision", "reject")
        state["decision_details"] = underwriting
        state["history"].append({"step": "decision", "decision": state["final_decision"]})
        return state
    
    async def _sanction_processing(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate and deliver sanction letter"""
        if state.get("final_decision") in ["approve", "counter_offer"]:
            sanction_result = await self.sanction_agent.process({
                "customer_data": state.get("customer_data", {}),
                "loan_details": state.get("underwriting_result", {}),
                "decision": state.get("final_decision")
            })
            
            state["sanction_result"] = sanction_result
            state["status"] = "approved"
            state["history"].append({"step": "sanction", "result": sanction_result})
        
        return state
    
    async def _feedback_learning(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Feedback learning engine"""
        # Store case for learning
        feedback_data = {
            "customer_id": state.get("customer_id"),
            "decision": state.get("final_decision"),
            "verification_score": state.get("verification_result", {}).get("confidence_score", 0),
            "risk_score": state.get("preliminary_risk_score", 0),
            "outcome": "pending"  # Would be updated based on actual loan performance
        }
        
        state["feedback_data"] = feedback_data
        state["history"].append({"step": "feedback", "data": feedback_data})
        return state

