from openai_api import chat_completion
from termcolor import colored
import re
import pickle
from typing import List, Dict, Tuple


class ExamQuestion:
    def __init__(self, idx: int, question: str, solution: str):
        self.idx = idx
        self.question = question
        self.solution = solution
        self.answers = []
    
    def print(self) -> None: 
        print(colored(f"{self.idx+1}) {self.question}", "black"))
        print(colored(f"Solution: {self.solution}","blue"))
        for i, (answer, correct) in enumerate(self.answers):
            if correct is None:
                color = "black"
            elif correct == "abstain":
                color = "yellow"
            elif correct == "correct":
                color = "green"
            else:
                color = "red"
            print(colored( f"Model Answer #{i+1}: {answer}", color))

class ExamSolver:
    def __init__(self, exam_name: str, questions: List[Dict[str, str]], model: str, temperature: float):
        self.exam_name = exam_name
        self.temperature = temperature
        self.model = model
        self.prompt = '''
            {question}

            Answer the question, then start a new line and say "Final Answer:" and indicate the letter choice of your final answer. If you think none of the options are correct, then write "Final Answer: abstain" instead.
        '''
        self.questions: List[ExamQuestion] = []
        for idx, question in enumerate(questions):
            self.questions.append(ExamQuestion(idx, question["question"], question["answer"]))
        self.solver_name = f"examsolver_{self.exam_name}_{self.model}_temperature{self.temperature}"
    
    def solve_question(self, question: ExamQuestion, num_answers, grade_answer=True) -> None:
        """
            Call the OpenAI API to solve a question. Sample different answers until you have at least ${num_answers} answers.
        """
        messages = [{"role":"user", "content":self.prompt.format(question = question.question)}]
        while len(question.answers) < num_answers:
            answer = chat_completion(model=self.model, messages=messages, temperature=self.temperature).choices[0].message.content
            if grade_answer:
                question.answers.append((answer, self.grade_answer(question, answer)))
            else:
                question.answers.append((answer, None))

    def grade_answer(self, question: ExamQuestion, answer: str) -> str:
        """
            Using GPT-3.5 to self-grade is relatively cheap and easier/more reliable than trying to prompt engineer the output into a format that from which we can easily extract the answer.
        """
        messages = []
        messages = [{"role":"user", "content":question.question}]
        if self.model == "gpt-3.5-turbo":
            # gpt-3.5 can't format the answers well so we pass in the whole solution
            messages.append({"role": "assistant", "content": answer})
        elif self.model == "gpt-4":
            # for gpt-4 we extract the final answer only and pass it to GPT-3.5 since the answers may be too long for GPT-3.5's context window
            index = answer.find("Final Answer:")
            # if there's no final answer, then we abstain
            if index == -1:
                return "abstain"
            answer = answer[index:].strip()
            if "abstain" in answer: # if the final answer says we abstained, then we return abstain. The option to obstain is an emergent quality only present in GPT-4
                return "abstain"
            messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content": f"The correct answer is {question.solution}. Did you get the answer correct? Answer with one word: yes or no."})
        result = chat_completion(model='gpt-3.5-turbo', messages=messages, temperature=0.0)
        correct = re.sub(r'[^a-zA-Z0-9]', '', result.choices[0].message.content).lower()
        if correct == "yes":
            return "correct"
        elif correct == "abstain":
            return "abstain"
        return "incorrect" # if the chat completion responds something other than "yes" or "no", that means the model's solution was complete garbage, which counts as a wrong answer

    
    def solve(self, num_questions = 25, num_answers = 1) -> None:
        """
            Solve first ${num_questions} questions in the exam. Sample enough answers to that every question has at least ${num_answers} answers. 
        """
        for idx, question in enumerate(self.questions):
            if idx == num_questions:
                break
            self.solve_question(question, num_answers)
            question.print()

