# Rigorous Evaluation of ChatGPT on the AMC 10 and 12 Exams
Recent large language models such as GPT-4 and Gemini have shown impressive near human-level results on several human knowledge and reasoning benchmarks such as the SATs and GSM8k. 
However, on more challenging exams, such as the [American Math Competition (AMC) exams](https://maa.org/math-competitions), they fare significantly worse, answering a majority of questions incorrectly.

However, current evaluation reporting for these small and challenging multiple-choice question datasets is quite flawed. They tend to report the score of a single trial run (presumably on low-temperature sampling). However, because the exam is both small and challenging enough that the model is potentially guessing on a vast majority of the problems, there is a very large variance in a model's performance on these exams across trial runs. Thus, reporting the mean score across many trial runs is imperative to obtaining rigorous and conclusive evaluations on this dataset.

For example, Gemini reports solving 32% of 150 AMC problems curated from the 2022 and 2023 contests, beating GPT-4's 30\%. This equates to an improvement of only three questions. We observed a standard deviation of 4.6 correctly answered questions between trial runs, so a single reported three-question improvement gives little information about whether Gemini is indeed better than GPT-4 on this benchmark.

This repository aims to lower the amount of friction required to engage in rigorous evaluation of LLMs on challenging mathematical reasoning tasks by providing:
* A collection of 153 questions from the 2022 and 2023 AMC exams in convenient JSON format
* A codebase to evaluate the ChatGPT models on these exams. It can be adapted to accomodate the chat-completion capabilities of other models as well. 
* Rigorous evaluations of GPT-3.5 on the AMC exams that re-affirm the inadequacy of current reporting metrics for the AMC exams and the failure of curent LLMs to do quality mathematical reasoning.


## Dataset

We take the questions and answers from the [Art of Problem Solving website](https://artofproblemsolving.com/wiki/index.php/AMC_12_Problems_and_Solutions) of the 2022 and 2023 AMC 10A, 10B, 12A, and 12B and store them as json files in `data/`. Questions that appeared in both the AMC 10 and AMC 12 exams are only included in the AMC 10 file. In total there are 153 questions. The `data/` directory also includes the High School Math and College Math tests in [MMLU](https://paperswithcode.com/dataset/mmlu), but we don't provide experimental results for those datasets as they don't involve as much reasoning (as evidenced by the fact that they elicit responses that are roughly half the number of tokens as AMC responses) and the results are not as high-variance as AMC.

Despite its limited size, the AMC exams are an interesting and useful dataset for evaluation because:
* The AMC exam series is significantly more challenging than the SATs and MMLU as measured by LLM (and student) performance and thus represents a large gap in the mathematical reasoning in existing LLMs.
* LLMs do quite poorly even though no specialized knowledge is required and previous exams are in the training data. Chain of Thought prompting is thus already baked into the model, so the model already knows the correct format of step-by-step solutions for responses (as evidenced by the fact that its responses often include as sign-off by the usernames of those who have historically written up solutions on the Art of Problem Solving website). Thus LLMs' poor performance on these exams are a reflection of their poor mathematical reasoning capabilities rather than a lack of knowledge or data.
* The high variance in the model's responses to these exam questions may make it useful for investigations on reliability
 

## Codebase
You can run the code by running `python main.py --file-names all`. This will solve and score all the AMC exams.


### Saved Solvers
Note that, once an exam is solved, we save the results in a pkl file in an output directory. By default, when solving an exam, the code first checks the output directory and loads up all previously solved answers instead of solving the exam again. Since these pkl files are included in the code, running `python main.py` will load up the pkl file and report our reported results of 100 trial runs on the 2023 AMC 10A (or whichever AMC exam you select).

### Prompting
Note that the prompt we use encourages the model to make its best guess if it cannot find the correct answer, but a prompt that tells the model to abstain will naturally abstain more often (this may result in lower final scores though).

The `--num-iterations` command line argument allows you to also do iterative prompting, in which the model looks at both the question and the model's previous response and outputs a new response.

We were unable to prompt engineer out way into better performance or reliability, but better prompts may exist.
You can edit the prompts by modifying `exams/prompts.py`.

## Rigorous Evaluations
### Experimental Details
For each question, we ask the model to answer the question and write its final answer in the format "Final Answer: A". If the model fails to format the answer correctly (quite often), then we pass the question and response into a chat completion and prompt it to format the answer correctly. If the model is still unable to format the answer correctly at this point, we mark the answer as "abstain."

The AMC exams offer the option to abstain from answering. It rewards 6 points for a correct answer and 1.5 points for an abstained answer, so abstaining has better expected value than complete random guessing. We prompt the model to always make its best guess when possible, but you can also prompt it to abstain more often. We follow the same scoring convention as AMC.

We run rigorous baselines on the AMC exams using OpenAI's `gpt-3.5-turbo` API from January 14-15, 2024. We do not present results to GPT-4 due to cost, but feel free to generate them yourself. 
We solve the exams once with 0-temperature sampling and run 100 trials with 0.7-temperature sampling. We also calculate results for majority-vote based ensemble voting (if there is a tie, we randomly choose one of the tied answers). We can group our trials into either one large ensemble or 10 groups of 10 ensembles.

### Results

Results are shown below. We also include baselines of always randomly guessing and always abstaining and Gemini's reported results of itself (32% correct) and GPT-4 (30% correct) (although, as argued above, single-score reporting isn't particularly reliable). For models with multiple trials, we include mean, standard deviation, and the min/max score across the trials. Results on individual exams and questions can be seen by running the code using our pre-solved checkpoints.



| **Method**             | **# of Trials** | **# Correct**             | **# Abstain**            | **Score**                      |
|------------------------|-----------------|---------------------------|--------------------------|--------------------------------|
| Random Guessing        | N/A             | 30.6 &plusmn; 4.9         | 0                        | 183.6 &plusmn; 29.7            |
| Always Abstain         | N/A             | 0                         | 153                      | 229.5                          |
| Gemini (Reported)      | ???             | 49                        | 0                        | 294                            |
| GPT-4 (Reported)       | ???             | 46                        | 0                        | 276                            |
| GPT-3.5 (0 temperature)| 1               | 31                        | 20                       | 216                            |
| GPT-3.5                | 100             | 38.7 &plusmn; 4.6 (26-50) | 10.3 &plusmn; 2.9 (4-18) | 247.9 &plusmn; 27.6 (169.5-315)|
| GPT-3.5 (10 ensemble)  | 10              | 48.4 &plusmn; 5.3 (37-54) | 5.0 &plusmn; 2.0 (2-9)   | 297.9 &plusmn; 31.2 (229.5-330)|
| GPT-3.5 (100 ensemble) | 1               | 59.5                      | 4                        | 363                            |
| Max Score              | N/A             | 153                       | 0                        | 918                            |

We hi-light the following observations:
* There is extremely high variance in the results of the model. We cannot skirt around this problem with 0-temperature sampling either, as it does not give a good estimate of the model's mean capability. In order to reduce the standard deviation to be around the half-question mark, taking the mean result over 100 samples (thereby reducing the standard deviation by 10) is quite necessary.
* GPT-3.5 is very bad at this task, on average marginally outperforming a weak student who abstains from answering every question. 
* Ensemble voting is particularly helpful, even exceeding the single reported GPT-4 run by multiple standard deviations. While it is conveient that ensembling is so helpful, this raises the question of whether the model can be trained to more reliably output the correct knowledge that it appears to have access to so that single-run performance has lower variance than it currently does  and similar performance as ensembling.

## Citation
If you found this repository helpful, please cite the following:

```
@misc{gptamceval,
  author       = Ronald Yu,
  title        = {Rigorous Evaluations of ChatGPT on the AMC 10 and 12 Exams},
  year         = 2024,
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ronald-yu/gpt-amc-eval}},
}
```

The views in this repository are my personal views and do not reflect those of my employer.
