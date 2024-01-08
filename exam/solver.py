from utils.openai import chat_completion
import os
import re
import pickle
from typing import List, Dict, Tuple
from exam.question import ExamQuestion

class ExamSolver:
    """
        Loads exam questions and then solves them.
    """
    def __init__(self, exam_name: str, questions: List[Dict[str, str]], model: str, temperature: float, save_dir = ""):
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
        self.save_dir = save_dir
    
    def solve_question(self, question: ExamQuestion, num_answers) -> None:
        """
            Call the OpenAI API to solve a question. Sample different answers until you have at least ${num_answers} answers.
        """
        messages = [{"role":"user", "content":self.prompt.format(question = question.question)}]
        while len(question.answers) < num_answers:
            answer = chat_completion(model=self.model, messages=messages, temperature=self.temperature).choices[0].message.content
            question.answers.append((answer, ""))

    def solve(self, num_questions: int, num_answers: int, save_every: int) -> None:
        """
            Solve first ${num_questions} questions in the exam. Sample enough answers to that every question has at least ${num_answers} answers. 
        """
        # solve the questions
        for idx, question in enumerate(self.questions):
            if idx == num_questions:
                break
            print(f"Solving Question {idx+1}")
            self.solve_question(question, num_answers)

            if idx % save_every == 0:
                self.save()
        self.save()

    def grade_and_print(self, num_questions:int, regrade: bool, save_every: int) -> None:
        """
            Grade and print the results
        """
        for idx, question in enumerate(self.questions):
            if idx == num_questions:
                break
            if regrade:
                question.extract_final_answers(regrade=True)
            question.grade_and_print()
            if idx % save_every == 0:
                self.save()
        self.save()

    def save(self):
        """
            Saves the exam to a pkl file in self.save_dir
        """
        
        file_name = os.path.join(self.save_dir, f"{self.solver_name}.pkl")
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)
