from utils.io import load_exams
from utils.config import get_command_line_args

def main():
    args = get_command_line_args()
    exam_solvers, exam_scorer = load_exams(args)

    for exam_solver in exam_solvers:
        exam_solver.solve(num_questions = args.num_questions, num_answers = args.num_answers, save_every = args.save_every)

        exam_solver.grade_and_print(num_questions = args.num_questions, regrade = args.regrade, save_every = args.save_every)


    exam_scorer.calculate_and_print_results()
 
        

if __name__ == "__main__":
    main()
