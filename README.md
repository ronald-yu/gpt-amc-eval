# Rigorous Evaluation of ChatGPT on the AMC 10 and 12 Exams

## Dataset

We take the questions and answers from the [Art of Problem Solving website](https://artofproblemsolving.com/wiki/index.php/AMC_12_Problems_and_Solutions) of the 2022 and 2023 AMC 10A, 10B, 12A, and 12B and store them as json files in `data/`. Questions that appeared in both the AMC 10 and AMC 12 exams are only included in the AMC 10 file. In total there are 153 questions. The `data/` directory also includes the High School Math and College Math tests in [MMLU](https://paperswithcode.com/dataset/mmlu), but we don't provide experimental results for those datasets as they don't involve as much reasoning and the results are not as high-variance as AMC.

## Experimental Details

The AMC exams offer the option to abstain from answering. It rewards 6 points for a correct answer and 1.5 points for an abstained answer, so abstaining has better expected value than complete random guessing. We prompt the model to always make its best guess when possible, but you can also prompt it to abstain more often.

For each question, we ask it to answer the question and write its final answer in the format "Final Answer: A". If the model fails to format the answer correctly (quite often), then we pass the question and response into a chat completion and prompt it to format the answer correctly. If the model is still unable to format the answer correctly at this point, we mark the answer as "abstain."


We run rigorous baselines on the AMC exams using OpenAI's `gpt-3.5-turbo` API from January 14-15, 2024. We do not present results to GPT-4 due to cost, but feel free to generate them yourself. 
We solve the exams once with 0-temperature sampling and run 100 trials with 0.7-temperature sampling. We also calculate results for majority-vote based ensemble voting (if there is a tie, we randomly choose one of the tied answers). We can group our trials into either one large ensemble or 10 groups of 10 ensembles.

## Results

Results are shown below. We also include baselines of always randomly guessing and always abstaining and Gemini's reported results of itself and GPT-4 (although, as argued above, single-score reporting isn't particularly reliable). For models with multiple trials, we include mean, standard deviation, and the min/max score across the trials. Results on individual exams and questions can be seen by running the code using our pre-solved checkpoints.



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




## Codebase
You can run the code by running `python main.py --file-names all`. This will solve and score all the AMC exams.


### Saved Solvers
Note that, once an exam is solved, we save the results in a pkl file in an output directory. By default, when solving an exam, the code first checks the output directory and loads up all previously solved answers instead of solving the exam again. Since these pkl files are included in the code, running `python main.py` will load up the pkl file and report our reported results of 100 trial runs on the 2023 AMC 10A (or whichever AMC exam you select).

### Prompting
Note that results may vary based on the prompt. For example, the prompt we use encourages the model to make its best guess if it cannot find the correct answer, but a prompt that tells the model to abstain will naturally abstain more often.
You can edit the prompts by modifying `exams/prompts.py`.

The `--num-iterations` command line argument allows you to do iterative prompting, in which the model looks at both the question and the model's previous response and outputs a new response. Empirically, iterative prompting functions similarly to low-temperature sampling as it lowers the diversity of responses (with more iterations resulting in less diversity), but we did not notice any improvements in performance (and it suffers from the same ambiguous evaluation as zero-temperature sampling). Hence, we do not report any rigorous results here.
