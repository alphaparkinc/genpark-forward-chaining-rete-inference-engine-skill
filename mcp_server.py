"""
MCP Server for Forward Chaining Rete Inference Engine Skill
"""

import json
import sys
from client import ReteInferenceEngine, Fact

engine = ReteInferenceEngine()

def handle_call(name: str, args: dict) -> dict:
    if name == "assert_fact":
        s = args.get("subject")
        p = args.get("predicate")
        o = args.get("object")
        engine.assert_fact(s, p, o)
        return {"status": "asserted", "working_memory_size": len(engine.working_memory)}
    elif name == "query_memory":
        return {"facts": [list(f) for f in engine.working_memory]}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_call(req.get("method"), req.get("params", {}))
        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
