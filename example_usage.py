"""
Demonstration of Forward Chaining Rete Inference Engine Skill
"""

from client import ReteInferenceEngine, Fact

def main():
    print("=== Forward Chaining Rete Rule Inference Demonstration ===")
    engine = ReteInferenceEngine()

    # Rule: IF (?agent, "detected_anomaly", "SQL_INJECTION") THEN (?agent, "trigger_action", "ISOLATE_SESSION")
    def action_isolate(bindings):
        agent = bindings.get("?agent", "unknown")
        return Fact(agent, "trigger_action", "ISOLATE_SESSION")

    engine.register_rule(
        name="isolate_on_sql_injection",
        conditions=[("?agent", "detected_anomaly", "SQL_INJECTION")],
        action=action_isolate
    )

    # Populate Working Memory
    print("Asserting initial observation: agent_guard_01 detected SQL_INJECTION...")
    engine.assert_fact("agent_guard_01", "detected_anomaly", "SQL_INJECTION")

    fired = engine.run_inference_cycle()
    print(f"Inference complete: {fired} rules fired.")

    print("\nUpdated Working Memory Contents:")
    for wme in sorted(engine.working_memory):
        print(f"  - {wme}")

    assert ("agent_guard_01", "trigger_action", "ISOLATE_SESSION") in engine.working_memory
    print("\nRete Inference Engine Verification PASS!")

if __name__ == "__main__":
    main()
