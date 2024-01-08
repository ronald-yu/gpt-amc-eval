from termcolor import colored
import tiktoken

def remove_non_uppercase(input_string):
    return ''.join(char for char in input_string if char.isupper())

class ExamQuestion:
    """
        This class stores the question, solution, and a list of answers provided by the solver. It also grades the answers by extracting final answers from the solver's chat completions and comparing them with the solution.
    """
    def __init__(self, idx: int, question: str, solution: str):
        self.idx = idx
        self.question = question
        self.solution = solution
        self.answers: List[Tuple[str, str]] = [] # each answer is a tuple of the chat response and the extracted final answer

    def grade_final_answer(self, final_answer: str) -> str:
        if final_answer == "abstain":
            return "abstain"
        elif final_answer == self.solution:
            return "correct"
        else:
            return "incorrect"

    def manual_review_final_answer(self, answer: str) -> str:
        print("\n------\n")
        print(colored("Please review ambiguous answer.", "red"))
        print(colored(f"{self.idx+1}) {self.question}", "black"))
        print(colored( f"Answer: {answer}", "yellow"))
        final_answer = ""
        while final_answer not in ["A", "B", "C", "D", "E", "abstain"]:
            final_answer = input("What is the final answer? Choose 'A', 'B', 'C', 'D', 'E', or 'abstain'. Or 'x' to exit.")
            if final_answer == "x":
                exit(0)
        return final_answer

    def extract_final_answer(self, answer: str) -> str:
        """
            Extract final answer from a chat completion. If we are unable to match the proper regular expression, then trigger manual review. GPT-3.5 does a poor job formatting its responses, so virtually all of its responses will need to undergo manual review.
        """
        index = answer.find("Final Answer:")
        # if there's no final answer (e.g. due to poor formatting or the model getting stuck in an endless loop), then we submit it for manual review later
        if index == -1:
            return self.manual_review_final_answer(answer)
        answer = answer[index + len("Final Answer:"):].strip()
        if "abstain" in answer: # if the final answer says we abstained, then we return abstain.
            return "abstain"
        answer = remove_non_uppercase(answer)
        if len(answer)==1:
            return answer
        else:
            return self.manual_review_final_answer(answer)

    def extract_final_answers(self, regrade=False) -> None:
        """
            Extract final answers from the answers and trigger a manual review if necessary.
            If regrade is activated, then we clear all our memory of previous final answers so that we can manually review ambiguous answers again.
        """
        extracted_answers = []
        for (answer, final_answer) in self.answers:
            if regrade or final_answer == "":
                final_answer = self.extract_final_answer(answer)
            extracted_answers.append((answer, final_answer))
        self.answers = extracted_answers

    def grade_and_print(self) -> None: 
        """
            Grade the answers and then colored print the question, solution, and the list of answers and final answers.
        """
        # make sure we have up-to-date final answers
        self.extract_final_answers()

        # grade and print the answers
        print(colored(f"{self.idx+1}) {self.question}", "black"))
        print(colored(f"Solution: {self.solution}","blue"))
        for i, (answer, final_answer) in enumerate(self.answers):
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
