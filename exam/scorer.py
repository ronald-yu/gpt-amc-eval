from typing import Tuple, List
from exam.solver import ExamSolver, ExamQuestion
import numpy as np

class ExamScorer:
    """
        Aggregates scores and statistics for a list of solved exams
    """

    def __init__(self, exam_solvers: List[ExamSolver], abstain_score: float, ensemble_size: int):
        self.exam_solvers = exam_solvers
        self.abstain_score = abstain_score
        self.ensemble_size = ensemble_size

    def calculate_corectness_grid(self, questions: List[ExamQuestion], all_answers: List[List[Tuple[str,str]]] = None) -> np.ndarray:
        """
            Aggregate the corectness results from a list of questions and corresponding answers into a single grid.
        """
        if all_answers is None:
            all_answers = [ question.answers for question in questions ]

        num_questions = len(questions)
        num_runs = max([len(answer_list) for answer_list in all_answers])

        correctness_grid = np.full((num_questions, num_runs), "", dtype=str)

        for question_idx, (question, answer_list) in enumerate(zip(questions, all_answers)):
            for run_idx,(_, final_answer) in enumerate(answer_list):
                correctness_grid[question_idx][run_idx] = question.grade_final_answer(final_answer)[0]
        return correctness_grid 

    def print_correctness_grid( self, correctness_grid: np.ndarray, dim: int, print_scores=False):
        correct = np.sum(correctness_grid == "c", axis=dim)
        incorrect = np.sum(correctness_grid == "i", axis=dim)
        abstain = np.sum(correctness_grid == "a", axis=dim)

        total = correct + incorrect + abstain
        score = correct * 6 + abstain * self.abstain_score

        if not correct.shape:
            print(f"{correct}/{total} correct. {abstain} abstained.")
            return
        for i in range(len(correct)):
            s = f"#{i+1}: {correct[i]}/{total[i]} correct. {abstain[i]} abstained."
            if print_scores:
                s += f" Score: {score[i]}"
            print(s)

        if print_scores:
            print("Mean score: ", score.mean())
            print("Score standard deviations: ", score.std())
            print("Min score: ", score.min())
            print("Max score: ", score.max())

    def calculate_and_print_results(self) -> None:
        """
            Print scores for a single exam_solver 
        """
        for exam_solver in self.exam_solvers:
            print(f"Final Results for {exam_solver.solver_name}.")
            correctness_grid = self.calculate_corectness_grid(exam_solver.questions) 
            print("Per-Question Results:")
            self.print_correctness_grid(correctness_grid, dim=1)
            print("Per-Run Results:")
            self.print_correctness_grid(correctness_grid, dim=0, print_scores=True)
            print("Total Results:")
            self.print_correctness_grid(correctness_grid, dim=(0,1))
