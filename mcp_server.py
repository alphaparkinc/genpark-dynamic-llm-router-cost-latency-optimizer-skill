"""MCP server for Dynamic LLM Router."""
import sys
import json
from client import DynamicLLMRouter

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "route_llm_request",
                "description": "Selects optimal LLM endpoint balancing cost, latency, and capability",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string"},
                        "max_budget_usd": {"type": "number"},
                        "require_deep_reasoning": {"type": "boolean"}
                    },
                    "required": ["prompt"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "route_llm_request":
            args = params.get("arguments", {})
            res = DynamicLLMRouter.route_request(
                args.get("prompt", ""),
                args.get("max_budget_usd", 0.01),
                args.get("require_deep_reasoning", False)
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
