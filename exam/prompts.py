baseline_prompt = """{question}

Answer the question, then start a new line and say "Final Answer:" and indicate the letter choice of your final answer. If you think none of the options are correct, make your best guess on which one of choices A, B, C, D, and E are correct."""

#baseline_prompt = """{question}
#
#Answer the question, then start a new line and say "Final Answer:" and indicate the letter choice of your final answer. If you think none of the options are correct, then write "Final Answer: abstain" instead."""


iterative_prompt = """
Can you explain your response but go more slowly and step-by-step and fix any logical inconsistencies? Then, provide a final answer.
"""

final_answer_prompt = """Question: {question}

Response: {answer}
        
What is the final answer of the response? Write "Final Answer:", and then the letter choice of your final answer ['A', 'B', 'C', 'D', 'E']. If no final answer is given, then put down your best guess.
"""

prompts = {"baseline": baseline_prompt, "iterative": iterative_prompt, "final_answer": final_answer_prompt}
