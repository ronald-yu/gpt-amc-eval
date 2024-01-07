from openai_api import chat_completion
from termcolor import colored
import re
import pickle
from typing import List, Dict


class ExamQuestion:
    def __init__(self, idx:int, question: str, solution: str):
        self.idx = idx
        self.question = question
        self.solution = solution
        self.model = model
        self.temperature = temperature
        self.answers = []
    
    def grade_answer(self, answer) -> bool:
        """
            Using GPT-3.5 to self-grade is relatively cheap and easier/more reliable than trying to prompt engineer the output into a format that from which we can easily extract the answer.
        """
        messages = []
        messages = [{"role":"user", "content":self.question}]
        messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content": f"The correct answer is {self.solution}. Did you get it correct? Answer with one word: yes or no."})
        result = chat_completion(model='gpt-3.5-turbo', messages=messages, temperature=0.0)
        correct = re.sub(r'[^a-zA-Z0-9]', '', result.choices[0].message.content).lower()
        if correct == 'yes':
            return True
        return False # if the chat completion responds something other than "yes" or "no", that means the model's solution was complete garbage, which counts as a wrong answer

    def print(self) -> None: 
        print(colored(f"{self.idx+1}) {self.question}", "black"))
        print(colored(f"Solution: {self.solution}","blue"))
        for i, (answer, correct) in enumerate(self.answers):
            if correct is None:
                color = "yellow"
            elif correct:
                color = "green"
            else:
                color = "red"
            print(colored( f"Model Answer #{i+1}: {answer}", color))

class ExamSolver:
    def __init__(self, exam_name:str, questions:List[Dict[str, str]], model = 'gpt-3.5-turbo', temperature = 0.0):
        self.temperature = temperature
        self.model = model
        self.prompt = '''{question}'''
        self.questions: List[ExamQuestion] = []
        for idx, q in enumerate(questions):
            self.questions.append(ExamQuestion(idx, question["question"], question["answer"])
        self.solver_name = f"examsolver_{self.exam_name}_{self.model}_temperature{self.temperature}"
    
    def solve_question(self, question: ExamQuestion, num_answers, grade_answer=True) -> None:
        """
            Call the OpenAI API to solve a question. Sample different answers until you have at least ${num_answers} answers.
        """
        messages = [{"role":"user", "content":self.prompt.format(question = question.question)}]
        while len(question.answers) < num_answers:
            answer = chat_completion(model=self.model, messages=messages, temperature=self.temperature).choices[0].message.content
            if grade_answer:
                self.answers.append((answer, question.grade_answer(answer)))
            else:
                self.answers.append((answer, None))
    
    def solve(self, num_questions = 25, num_answers = 1) -> None:
        """
            Solve first ${num_questions} questions in the exam. Sample enough answers to that every question has at least ${num_answers} answers. 
        """
        for idx, q in self.questions:
            if idx == num_questions:
                break
            self.solve_question(q, num_answers)
            q.print()
