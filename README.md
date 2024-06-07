# Evaluating Causal Reasoning in Large Language Models: Do LLMs understand causality?

**Authors**: Aseem Dandgaval, Dinesh Karthikeyan, Nandita Sanjivi, Prathish Murugan

---

This study assesses the ability of Large Language Models (LLMs) to perform formal causal reasoning, employing the comprehensive CLadder dataset as a testbed. Despite their extensive application across various domains of natural language processing, LLMs' competence in handling formal causal queries has not been thoroughly explored. Our research aims to determine whether LLMs can interpret and respond to complex causal inquiries in a manner consistent with human reasoning paradigms.

We systematically evaluate LLMs' performance by analyzing their responses to a broad spectrum of causal questions, including associational, interventional, and counterfactual scenarios. This evaluation focuses on the accuracy with which these models generate responses that are not only correct but also demonstrate coherent and logical reasoning steps that mirror formal reasoning patterns expected in human cognition.

The findings from this study provide valuable insights into the capabilities and limitations of current LLMs regarding causal reasoning. These insights pave the way for targeted improvements in model training and can significantly influence the deployment of LLMs in real-world applications where accurate causal inference is essential.

---


### Data Usage

You can download the data either from huggingface (https://huggingface.co/datasets/causalnlp/CLadder), or [cladder-v1.zip](https://github.com/causalNLP/cladder/raw/main/data/cladder-v1.zip). 

In the data, each sample represents a single question. Each question has the following fields:

- `question_id`: a unique (for the file) identifier for the question
- `desc_id`: a more descriptive identifier for the question (generally not needed)
- `given_info`: natural language supplementary information that should be given to the model to answer the question.
- `question`: the question itself, in natural language
- `answer`: the answer to the question {yes, no}
- `reasoning`: a step-by-step explanation of the causal reasoning used to answer the question
- `meta`: metadata about the question, including the following fields:
  - `query_type`: the type of question, one of {ATE, marginal, correlation, ETT, NDE, NIE, etc.}
  - `rung`: the rung of the ladder of causation that the question corresponds to
  - `story_id`: the id of the story used to verbalize the question
  - `graph_id`: the id of the causal graph structure used to verbalize the question
  - `model_id`: the id of the underlying model used to generate the question (corresponding to a model in `cladder-v1-meta-models.json`)
  - `groundtruth`: the groundtruth value of what the question is asking about

#### Prompting the Model

When evaluating a language model, it is recommended that the prompt includes 3 components:

1. The `background` field of the model corresponding to the question (found in `cladder-v1-meta-models.json` using the `model_id` field of the question's metadata).
2. The `given_info` field of the question.
3. The `question` field of the question.


#### Example

For example, the prompt corresponding to question 16825 (which asks about the average treatment effect for a simple instrumental variable setting) in `cladder-v1-balanced.json` could be:


> Imagine a self-contained, hypothetical world with only the following conditions, and without any unmentioned factors or causal relationships: Unobserved confounders has a direct effect on education level and salary. Proximity to a college has a direct effect on education level. Education level has a direct effect on salary. Unobserved confounders is unobserved.
>
> For people living far from a college, the probability of high salary is 35%. For people living close to a college, the probability of high salary is 53%. For people living far from a college, the probability of college degree or higher is 40%. For people living close to a college, the probability of college degree or higher is 73%.
>
> Will college degree or higher decrease the chance of high salary?

Here the correct answer is `no`. The associated reasoning steps found in the `reasoning` field are:
    

> Step 0: Let V2 = proximity to a college; V1 = unobserved confounders; X = education level; Y = salary. 
>
> Step 1: V1->X,V2->X,V1->Y,X->Y 
>
> Step 2: E[Y | do(X = 1)] - E[Y | do(X = 0)]
>
> Step 3: [P(Y=1|V2=1)-P(Y=1|V2=0)]/[P(X=1|V2=1)-P(X=1|V2=0)]
>
> Step 4: P(Y=1 | V2=0) = 0.35; P(Y=1 | V2=1) = 0.53; P(X=1 | V2=0) = 0.40; P(X=1 | V2=1) = 0.73
>
> Step 5: (0.53 - 0.35) / (0.73 - 0.40) = 0.55
>
> Solution: 0.55 > 0


Note that in addition to the `background` field, the model information found in `cladder-v1-meta-models.json` contains sufficient information to fully reconstruct the underlying causal model used to generate this question (and 59 others).

### Dataset Statistics

Here are some basic statistics for the main dataset (`cladder-v1-balanced.json`).

Number of questions: 10,112
Answers: {"yes": 5,056, "no": 5,056}

Query Types:

| Query Type                             | Rung | Code               | Number | Percent |
| -------------------------------------- | ---- | ------------------ | ------ | ------- |
| Correlation                            | 1    | correlation        | 1422   | 14.1%   |
| Marginal Distribution                  | 1    | marginal           | 1580   | 15.6%   |
| Expaining Away Effect                  | 1    | exp_away           | 158    | 1.6%    |
| Average Treatment Effect               | 2    | ate                | 1422   | 14.1%   |
| Backdoor Adjustment Set                | 2    | backadj            | 1580   | 15.6%   |
| Collider Bias                          | 2    | collider_bias      | 158    | 1.6%    |
| Effect of the Treatment on the Treated | 3    | ett                | 1264   | 12.5%   |
| Natural Direct Effect                  | 3    | nde                | 316    | 3.1%    |
| Natural Indirect Effect                | 3    | nie                | 790    | 7.8%    |
| Counterfactual (deterministic)         | 3    | det-counterfactual | 1422   | 14.1%   |


Graph Types:

| Graph Type  | Number | Percent |
| ----------- | ------ | ------- |
| IV          | 790    | 7.8%    |
| arrowhead   | 1264   | 12.5%   |
| chain       | 1106   | 10.9%   |
| collision   | 632    | 6.2%    |
| confounding | 948    | 9.4%    |
| diamond     | 1106   | 10.9%   |
| diamondcut  | 948    | 9.4%    |
| fork        | 948    | 9.4%    |
| frontdoor   | 1106   | 10.9%   |
| mediation   | 1264   | 12.5%   |


