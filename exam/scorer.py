from typing import Tuple, List
from exam.solver import ExamSolver, ExamQuestion
import numpy as np
from utils.misc import random_mode

class ExamScorer:
    """
        Aggregates scores and statistics for a list of solved exams
    """

    def __init__(self, exam_solvers: List[ExamSolver], abstain_score: float, ensemble_size: int):
        self.exam_solvers = exam_solvers
        self.abstain_score = abstain_score
        self.ensemble_size = ensemble_size

    def calculate_corectness_grid(self, questions: List[ExamQuestion], all_answers: List[List[str]]) -> np.ndarray:
        """
            Aggregate the corectness results from a list of questions and corresponding answers into a single grid.
        """

        num_questions = len(questions)
        num_runs = max([len(answer_list) for answer_list in all_answers])

        correctness_grid = np.full((num_questions, num_runs), "", dtype=str)

        for question_idx, (question, answer_list) in enumerate(zip(questions, all_answers)):
            for run_idx, final_answer in enumerate(answer_list):
                correctness_grid[question_idx][run_idx] = question.grade_final_answer(final_answer)[0]
        return correctness_grid 

    def print_correctness_grid( self, correctness_grid: np.ndarray, dim: int):
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
            if dim == 0:
                s += f" Score: {score[i]}"
            print(s)

        if dim == 0:
            print("Mean score: ", score.mean())
            print("Score standard deviations: ", score.std())
            print("Min score: ", score.min())
            print("Max score: ", score.max())

            print("Mean correct: ", correct.mean())
            print("Correct standard deviations: ", correct.std())
            print("Min correct: ", correct.min())
            print("Max correct: ", correct.max())

            print("Mean abstain: ", abstain.mean())
            print("Abstain standard deviations: ", abstain.std())
            print("Min abstain: ", abstain.min())
            print("Max abstain: ", abstain.max())

    def aggregate_final_answers(self, exam_solver) -> List[List[str]]:
        """
            Aggregate the final answers of multiple runs in an exam_solver via majority voting. Randomly select a choice if there is tie for the majority.
        """
        all_aggregated_answers = []
        for question in exam_solver.questions:
            answers = [ "x" if final_answer == "abstain" else final_answer for _, final_answer in question.answers ] # there's an issue with using >1 character strings in np sometimes
            answers = np.array(answers).reshape((-1, self.ensemble_size))
            aggregated_answers = np.apply_along_axis(random_mode, axis=1, arr=answers)
            aggregated_answers = ["abstain" if answer == "x" else answer for answer in aggregated_answers]
            all_aggregated_answers.append(aggregated_answers)
        return all_aggregated_answers

    def calculate_and_print_results(self) -> None:
        """
            Print scores for a single exam_solver 
        """
        for exam_solver in self.exam_solvers:
            aggregated_final_answers = self.aggregate_final_answers(exam_solver)

            print(f"Final Results for {exam_solver.solver_name}.")
            correctness_grid = self.calculate_corectness_grid(exam_solver.questions, aggregated_final_answers) 
            print("Per-Question Results:")
            self.print_correctness_grid(correctness_grid, dim=1)
            print("Per-Run Results:")
            self.print_correctness_grid(correctness_grid, dim=0)
            print("Total Results:")
            self.print_correctness_grid(correctness_grid, dim=(0,1))
