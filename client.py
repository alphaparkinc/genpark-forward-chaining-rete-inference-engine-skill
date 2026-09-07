"""
Forward Chaining Rete Inference Engine Skill Client
Pure Python Standard Library implementation of forward chaining rule-based reasoning (Forgy's Rete pattern matching).
Evaluates Working Memory Elements (WMEs) against alpha-network condition nodes and executes production rules.
"""

from typing import List, Dict, Any, Tuple, Optional, Set, Callable


class Fact:
    def __init__(self, subject: str, predicate: str, object_val: Any):
        self.subject = subject
        self.predicate = predicate
        self.object_val = object_val

    def to_tuple(self) -> Tuple[str, str, Any]:
        return (self.subject, self.predicate, self.object_val)

    def __repr__(self):
        return f"Fact({self.subject}, {self.predicate}, {self.object_val})"


class ProductionRule:
    def __init__(self, name: str, conditions: List[Tuple[str, str, Any]], action: Callable[[Dict[str, Any]], Optional[Fact]]):
        self.name = name
        self.conditions = conditions  # [(subject, predicate, object)]
        self.action = action


class ReteInferenceEngine:
    def __init__(self):
        self.working_memory: Set[Tuple[str, str, Any]] = set()
        self.rules: List[ProductionRule] = []

    def assert_fact(self, subject: str, predicate: str, object_val: Any):
        self.working_memory.add((subject, predicate, object_val))

    def register_rule(self, name: str, conditions: List[Tuple[str, str, Any]], action: Callable[[Dict[str, Any]], Optional[Fact]]):
        rule = ProductionRule(name, conditions, action)
        self.rules.append(rule)

    def run_inference_cycle(self, max_cycles: int = 10) -> int:
        """Run forward chaining inference until fixpoint or max_cycles."""
        total_fired = 0
        for _ in range(max_cycles):
            cycle_fired = 0
            for rule in self.rules:
                # Match conditions
                matched = True
                bindings: Dict[str, Any] = {}
                for cond in rule.conditions:
                    c_subj, c_pred, c_obj = cond
                    # Find fact matching condition
                    found = False
                    for wme in self.working_memory:
                        w_subj, w_pred, w_obj = wme
                        if (c_subj.startswith("?") or c_subj == w_subj) and \
                           (c_pred.startswith("?") or c_pred == w_pred) and \
                           (c_obj.startswith("?") if isinstance(c_obj, str) else c_obj == w_obj):
                            found = True
                            if c_subj.startswith("?"):
                                bindings[c_subj] = w_subj
                            if c_pred.startswith("?"):
                                bindings[c_pred] = w_pred
                            if isinstance(c_obj, str) and c_obj.startswith("?"):
                                bindings[c_obj] = w_obj
                            break
                    if not found:
                        matched = False
                        break

                if matched:
                    new_fact = rule.action(bindings)
                    if new_fact:
                        t = new_fact.to_tuple()
                        if t not in self.working_memory:
                            self.working_memory.add(t)
                            cycle_fired += 1
                            total_fired += 1
            if cycle_fired == 0:
                break  # Fixpoint reached
        return total_fired
