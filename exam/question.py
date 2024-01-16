from termcolor import colored
from utils.misc import remove_non_uppercase
from utils.openai import num_tokens
from typing import Tuple

class ExamQuestion:
    """
        This class stores the question, solution, and a list of answers provided by the solver. 
    """

    def __init__(self, idx: int, question: str, solution: str):
        self.idx = idx
        self.question = question
        self.solution = solution
        self.answers: List[List[Tuple[str, str]]] = [[]] # A nested loop of answers. The outer list is per-iteration. The inner-list is per-exam run.
        # each answer is a tuple of the chat response and the extracted final answer

    def add_answer(self, answer:str, iteration:int) -> None:
        self.answers[iteration].append((answer,""))

    def set_final_answer(self, final_answer:str, iteration:int, answer_idx:int) -> None:
        answer, _ = self.answers[iteration][answer_idx]
        self.answers[iteration][answer_idx] = (answer, final_answer)

    def add_iteration(self) -> None:
        self.answers.append([])

    def grade_final_answer(self, final_answer: str) -> str:
        if final_answer == "abstain":
            return "abstain"
        elif final_answer == self.solution:
            return "correct"
        else:
            return "incorrect"

    @staticmethod
    def extract_final_answer( answer: str, abstain_bad_format = False) -> str:
        """
            Extract final answer from a properly formatted chat completion. If abstain_bad_format, then we return abstain if the answer is poorly formatted.
        """
        index = answer.find("Final Answer:")
        if index == -1:
            if abstain_bad_format:
                return "abstain"
            return ""
        final_answer = answer[index + len("Final Answer:"):].strip()
        if "abstain" in answer: # if the final answer says we abstained, then we return abstain.
            return "abstain"
        final_answer = remove_non_uppercase(final_answer)
        if len(final_answer)==1:
            return final_answer
        else:
            if abstain_bad_format:
                return "abstain"
            return ""

    def extract_final_answers(self, iteration: int) -> None:
        """
            Extract final answers from properly formatted answers.
        """
        answer_list = self.answers[iteration]
        extracted_answers = []
        for (answer, final_answer) in answer_list:
            if final_answer == "":
                final_answer = ExamQuestion.extract_final_answer(answer)
            extracted_answers.append((answer, final_answer))
        self.answers[iteration] = extracted_answers

    def print_answers(self, iteration: int) -> Tuple[int,int]: 
        """
            Grade the answers and then colored print the question, solution, and the list of answers and final answers.
        """
        if len(self.answers) <= iteration:
            return

        # grade and print the answers
        print(colored(f"{self.idx+1}) {self.question}", "black"))
        print(colored(f"Solution: {self.solution}","blue"))
        tot_tokens = 0
        num_answers = 0
        for i, (answer, final_answer) in enumerate(self.answers[iteration]):

            tot_tokens += num_tokens(answer)
            num_answers += 1

            for j in range(iteration):
                print(f"Prev Answer #{j+1}")
                color = "black" if j%2 == 0 else "blue"
                print(colored(self.answers[j][i], color))

            correct = self.grade_final_answer(final_answer)
            if correct == "abstain":
                color = "yellow"
            elif correct == "correct":
                color = "green"
            else:
                color = "red"
            print(colored( f"Model Final Answer #{i+1}: {final_answer}", color))
            print(colored( f"Model Answer #{i+1}: {answer}", color))
            print("\n----\n")
        return tot_tokens, num_answers
