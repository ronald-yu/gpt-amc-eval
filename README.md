# Rigorous Evaluation of ChatGPT on the AMC Dataset



Here are the results using the `gpt-3.5-turbo` API from January 14-15, 2024. We also include Gemini's reported results of itself and GPT-4. For models with multiple trials, we include mean, standard deviation, and the min/max score across the trials.

| **Method**             | **# of Trials** | **# Correct**             | **# Abstain**            | **Score**                      |
|------------------------|-----------------|---------------------------|--------------------------|--------------------------------|
| Random Guessing        | N/A             | 30.6 &plusmn; 4.9         | 0                        | 183.6 &plusmn; 29.7            |
| Always Abstain         | N/A             | 0                         | 153                      | 229.5                          |
| Gemini (Reported)      | ???             | 49                        | 0                        | 294                            |
| GPT-4 (Reported)       | ???             | 44                        | 0                        | 264                            |
| GPT-3.5 (0 temperature)| 1               | 31                        | 20                       | 216                            |
| GPT-3.5                | 100             | 38.7 &plusmn; 4.6 (26-50) | 10.3 &plusmn; 2.9 (4-18) | 247.9 &plusmn; 27.6 (169.5-315)|
| GPT-3.5 (10 ensemble)  | 10              | 48.4 &plusmn; 5.3 (37-54) | 5.0 &plusmn; 2.0 (2-9)   | 297.9 &plusmn; 31.2 (229.5-330)|
| GPT-3.5 (100 ensemble) | 1               | 59.5                      | 4                        | 363                            |
| Max Score              | N/A             | 153                       | 0                        | 918                            |


Note that results may vary based on the prompt. For example, the prompt we use encourages the model to make its best guess if it cannot find the correct answer, but a prompt that tells the model to abstain will naturally abstain more often.


## Codebase
You can run the code by running `python main.py`. This will by default solve and score the 2023 AMC 10a. You can edit the prompts by modifying `exams/prompts.py`.

### Saved Solvers
Once an exam is solved, we save the results in a pkl file in an output directory. By default, when solving an exam, the code first checks the output directory and loads up all previously solved answers.

### Iterative Prompting
The `--num-iterations` command line argument allows you to do iterative prompting, in which the model looks at both the question and the model's previous response and outputs a new response. Empirically, iterative prompting functions similarly to low-temperature sampling as it lowers the diversity of responses (with more iterations resulting in less diversity), but we did not notice any improvements in performance (and it suffers from the same ambiguous evaluation as zero-temperature sampling).
