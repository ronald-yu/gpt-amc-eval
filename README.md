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
