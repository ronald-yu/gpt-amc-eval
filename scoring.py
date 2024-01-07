# Helper functions for scoring the test and aggregating statistics
from typing import Tuple, List

def score_exam_solver(exam_solver) -> Tuple[List[Tuple[int,int]], int, int]:
    """
        Aggregate the score of the exam solver
    """
    individual_stats = []
    exam_num_correct = 0
    exam_num_abstained = 0
    exam_num_answers = 0 # this includes abstains

    number_full_exams = max([len(question.answers) for question in exam_solver.questions])
    total_exam_scores = [0] * number_full_exams
    for question in exam_solver.questions:
        num_correct = 0
        num_abstained = 0
        num_answers = len(question.answers)
        for idx,(_, correct) in enumerate(question.answers):
            score = 0
            if correct == "correct":
                num_correct+=1
                score = 6
            if correct == "abstain":
                num_abstained+=1
                score = 1.5
            if idx < number_full_exams:
                total_exam_scores[idx]+=score
        exam_num_correct += num_correct
        exam_num_abstained += num_abstained
        exam_num_answers += num_answers
        individual_stats.append((num_correct, num_abstained, num_answers))
    return individual_stats, total_exam_scores, (exam_num_correct, exam_num_abstained, exam_num_answers)

def print_scores(exam_solver) -> None:
    """
        Print scores for a single exam_solver 
    """
    print(f"Final Scores for {exam_solver.solver_name}")
    individual_stats, total_exam_scores, (exam_num_correct, exam_num_abstained, exam_num_answers) = score_exam_solver(exam_solver)
    for idx, (num_correct, num_abstained, num_answers) in enumerate(individual_stats):
        if num_answers > 0:
            print(f"Problem {idx+1}: {num_correct}/{num_answers} correct. {num_abstained} abstained.")
    print(f"Total Results: {exam_num_correct}/{exam_num_answers} correct. {exam_num_abstained} abstained.")
    print(f"Total Exam Scores: {total_exam_scores}")

def regrade_abstains(exam_solver) -> None:
    """
       Manually regrade all answers that are marked as abstained since the GPT-3.5 grader sometimes mistakenly belives the model abstains when the formatting of the answer is off due to poor/insufficient prompt engineering (i.e. the bad formatting is likely not due to bad reasoning abilities).
    """
    for question in exam_solver.questions:
        regraded_answers = []
        for (answer, correct) in question.answers:
            if correct== "abstain":
                print("Question:", question.question)
                print("Solution:", question.solution)
                print("Answer:", answer)
                manual_correct = input("Is this correct? Yes (y), No (n), or abstained (a).")
                if manual_correct == "y":
                    correct = "correct"
                elif manual_correct == "n":
                    correct = "incorrect"
                elif manual_correct == "a":
                    correct = "abstain"
            regraded_answers.append((answer, correct))
        question.answers = regraded_answers

