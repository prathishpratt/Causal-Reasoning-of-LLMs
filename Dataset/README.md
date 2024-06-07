## Dataset Statistics

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


