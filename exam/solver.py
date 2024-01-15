from utils.openai import chat_completion, num_tokens
import os
import re
import pickle
from typing import List, Dict, Tuple
from exam.question import ExamQuestion
from exam.prompts import prompts

class ExamSolver:
    """
        Loads exam questions and then solves them.
    """
    def __init__(self, exam_name: str, questions: List[Dict[str, str]], model: str, temperature: float, save_dir = ""):
        self.exam_name = exam_name
        self.temperature = temperature
        self.model = model
        self.questions: List[ExamQuestion] = []
        for idx, question in enumerate(questions):
            self.questions.append(ExamQuestion(idx, question["question"], question["answer"]))
        self.solver_name = f"examsolver_{self.exam_name}_{self.model}_temperature{self.temperature}"
        self.save_dir = save_dir

    def get_prev_answer(self, question:ExamQuestion, iteration: int):
        sample_id = len(question.answers[iteration])

        if True or self.iteration_type == "baseline":
            return question.answers[iteration-1][sample_id][0]
        
        group_idx = sample_id // 2

        ret = "Here are three separate responses:"
        for i in range(2):
            ret+=f"\nResponse {i}: {question.answers[iteration-1][group_idx*3 + i][0]}\n"
        print(ret)
        return ret
        

    def construct_prompt(self, question:ExamQuestion, iteration:int) -> List[Dict[str,str]]:
        question_prompt = prompts["baseline"].format(question=question.question)
        messages =  [{"role":"user", "content":question_prompt}]
        if iteration > 0:
            sample_id = len(question.answers[iteration]) 
            prev_answer = question.answers[iteration-1][sample_id][0]
            prev_answer = self.get_prev_answer(question, iteration)
            if self.model == "gpt-3.5-turbo" and num_tokens(prev_answer) + num_tokens(question_prompt) + num_tokens (prompts["iterative"]) >= 4050:
                return messages
            messages.append({"role":"assistant", "content":prev_answer})
            messages.append({"role":"user", "content":prompts["iterative"]})
        return messages

    def construct_final_answer_prompt(self, question:ExamQuestion, iteration:int, answer_idx:int) -> List[Dict[str, str]]:
        answer,_ = question.answers[iteration][answer_idx]
        prompt = prompts["final_answer"].format(question=question.question, answer=answer)
        if self.model == 'gpt-3.5-turbo' and num_tokens(prompt) >= 4050:
            return None
        return  [{"role":"user", "content":prompt}]
        
    
    def solve(self, num_iterations:int, num_questions: int, num_answers: int, skip_questions: int) -> None:
        """
            Solve first ${num_questions} questions in the exam. Sample enough answers to that every question has at least ${num_answers} answers. 
        """
        # solve the questions
        for iteration in range(num_iterations):
            print(f"  Iteration {iteration+1}")
            messages_list = []
            for idx, question in enumerate(self.questions):
                if idx < skip_questions:
                    continue
                if idx == num_questions:
                    break
                if len(question.answers) == iteration:
                    question.add_iteration() 
                #if iteration == 0:
                #    while len(question.answers[iteration]) < num_answers:
                #        answer = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

#Final Answer: abstain
#"""
                #        question.add_answer(answer, iteration)
                #    continue
                num_samples = num_answers - len(question.answers[iteration])
                if num_samples <= 0:
                    continue
                messages = self.construct_prompt(question, iteration)
                for i in range(num_samples):
                    messages_list.append((idx,messages))
            batch_size = 1 if self.model == "gpt-4" else 125
            for i in range(0, len(messages_list), batch_size):
                print(f"Completed {i} of {len(messages_list)} API Calls")
                answers = chat_completion(model=self.model, messages_list=messages_list[i:i+batch_size], temperature=self.temperature)
                for idx, answer in answers:
                    self.questions[idx].add_answer(answer, iteration)
                self.save()

        # extract the final answers
        iteration = num_iterations - 1
        for question in self.questions:
            question.extract_final_answers(iteration = iteration)

        messages_list = []
        for idx, question in enumerate(self.questions):
            for answer_idx, (answer, final_answer) in enumerate(question.answers[iteration]):
                if final_answer == "":
                    messages = self.construct_final_answer_prompt(question, iteration, answer_idx)
                    if messages is None:
                        question.set_final_answer("abstain", iteration, answer_idx)
                        continue
                    success = messages_list.append(((idx, answer_idx), messages))

        print("Extracting Final Answers")
        for i in range(0, len(messages_list), batch_size):
            print(f"Completed {i} of {len(messages_list)} API Calls")
            final_answers = chat_completion(model=self.model, messages_list=messages_list[i:i+batch_size], temperature=self.temperature)
            for (idx,answer_idx), final_answer in final_answers:
                self.questions[idx].set_final_answer(ExamQuestion.extract_final_answer(final_answer, True), iteration, answer_idx)
            self.save()

    def print_answers(self, num_questions:int, iteration: int) -> None:
        """
            Print the results
        """
        for idx, question in enumerate(self.questions):
            if idx == num_questions:
                break
            question.print_answers(iteration)

    def save(self):
        """
            Saves the exam to a pkl file in self.save_dir
        """
        
        file_name = os.path.join(self.save_dir, f"{self.solver_name}.pkl")
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)
