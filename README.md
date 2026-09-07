# GenPark Forward Chaining Rete Inference Engine Skill

Forward chaining rule engine with working memory element (WME) pattern matching and fixpoint deduction.

Explore more at [GenPark](https://genpark.ai) and the [GenPark MCP Catalog](https://genpark.ai/mcp).

```mermaid
graph LR
    A[Initial Working Memory Facts] --> B[Alpha Condition Matching]
    B --> C[Variable Binding Substitution]
    C --> D[Conflict Resolution & Rule Activation]
    D --> E[Execute Production RHS Actions]
    E -->|Assert New Facts| A
```

## Features
- Forward-chaining expert system with fixpoint termination.
- Pattern matching with variable binding.
- Pure Python standard library.
