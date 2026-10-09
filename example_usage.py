"""Example usage for Dynamic LLM Router."""
from client import DynamicLLMRouter

if __name__ == "__main__":
    code_prompt = "def optimize_query(sql_text): pass"
    decision = DynamicLLMRouter.route_request(code_prompt, max_budget_usd=0.005)
    print("Selected Model:", decision["model_name"])
    print("Latency Target:", decision["expected_latency_ms"], "ms")
