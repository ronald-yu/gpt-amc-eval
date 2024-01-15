from exam.solver import ExamSlver

class IterativeExamSolver(ExamSolver):
    """
        A solver that iteratively asks the model to search for logical inconsistencies within its output
    """
    def __init__(self, exam_name: str, questions: List[Dict[str, str]], model: str, temperature: float, save_dir = "", prompt_type = "baseline", num_iterations=2):
        super().__init__(exam_name, questions, temperature, save_dir, prompt_type, num_iterations)
        self.num_iterations = num_iterations


    def solve_question(self, question: ExamQuestion, num_answers) -> None:
        """
            Call the OpenAI API to solve a question. Sample different answers until you have at least ${num_answers} answers.
        """
        while len(question.answers) < num_answers:
            messages = [{"role":"user", "content":prompts[self.prompt_type].format(question = question.question)}]
            answer = chat_completion(model=self.model, messages=messages, temperature=self.temperature).choices[0].message.content
            explanations = [answer]
            while len(explanations) < self.num_iterations:
                messages.append({"role": "assistant", "content": answer})
                messages.append({"role": "Explain any logical inconsistencies in your response. Then update your response."})
                answer = chat_completion(model=self.model, messages=messages, temperature=self.temperature).choices[0].message.content
                explanations.apend[answer]
            question.answers.append((answer, ""))
            question.explanations.append(explanations[:-1]) # don't include last message in list of explanations
            
