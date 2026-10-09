"""Dynamic LLM Router & Cost/Latency Optimizer.
100% Python Standard Library.
"""

class DynamicLLMRouter:
    """Selects optimal model endpoint based on query complexity, budget, and latency tolerance."""
    
    MODELS = {
        "fast_tier": {"name": "flash-light-v2", "cost_per_1k": 0.0001, "latency_ms": 120, "max_tokens": 8192},
        "reasoning_tier": {"name": "pro-reasoner-v3", "cost_per_1k": 0.0030, "latency_ms": 850, "max_tokens": 32768},
        "coding_tier": {"name": "code-expert-v2", "cost_per_1k": 0.0015, "latency_ms": 400, "max_tokens": 16384}
    }
    
    @classmethod
    def route_request(cls, prompt: str, max_budget_usd: float = 0.01, require_deep_reasoning: bool = False) -> dict:
        prompt_len = len(prompt)
        prompt_lower = prompt.lower()
        
        is_code = any(kw in prompt_lower for kw in ["def ", "class ", "import ", "function", "sql", "bug", "traceback"])
        is_math_or_logic = any(kw in prompt_lower for kw in ["prove", "calculate", "analyze tradeoff", "multi-step", "architect"])
        
        if require_deep_reasoning or (is_math_or_logic and prompt_len > 300):
            selected = "reasoning_tier"
        elif is_code:
            selected = "coding_tier"
        else:
            selected = "fast_tier"
            
        model_info = cls.MODELS[selected]
        estimated_cost = (prompt_len / 4000) * model_info["cost_per_1k"]
        
        if estimated_cost > max_budget_usd and selected != "fast_tier":
            selected = "fast_tier"
            model_info = cls.MODELS[selected]
            estimated_cost = (prompt_len / 4000) * model_info["cost_per_1k"]
            
        return {
            "selected_tier": selected,
            "model_name": model_info["name"],
            "expected_latency_ms": model_info["latency_ms"],
            "estimated_cost_usd": round(estimated_cost, 6),
            "routing_reason": f"Routed to {selected} based on semantic intent and budget boundary."
        }
