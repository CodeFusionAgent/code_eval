# Eval code and dataset 

Contains evaluation code, results, dataset for the CodeFusion project.



# Metrics

 It is critical for any LLM Agentic system to have high quality evals which are the guidance system for gauging performance, quality and robustness.

### Overall quality metric:

####  Architecture-Level Reasoning Measure:
  Definition: Measures success in answering higher-level questions about the system's design, module interactions, or architectural decisions.

#### Reasoning consistency:
Is the reasoning consistent ? Is it logical ? (self consistency).
The degree to which the agent's reasoning steps (e.g., in CoT) are internally coherent and syntactically/semantically valid in code logic terms.

#### Code Reasoning Tiers:
Categorize questions into tiers (e.g., performance-related, runtime-related, inter-module, architectural), and evaluate accuracy per tier.

#### Grounding score:
Accuracy of answers from a factual perspective.

#### Human eval (optional):
Human perception of whether the answer was sufficient, accurate and helpful.
