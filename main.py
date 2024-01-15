from utils.io import load_exams
from utils.config import get_command_line_args

def main():
    args = get_command_line_args()
    if args.file_names == ["all"]:
        args.file_names = ["amc10a_2023", "amc10b_2023", "amc10a_2022", "amc10b_2022", "amc12a_2023", "amc12b_2023", "amc12a_2022", "amc12b_2022"]
    exam_solvers, exam_scorer = load_exams(args)

    for exam_solver in exam_solvers:
        exam_solver.solve(skip_questions = args.skip_questions, num_iterations = args.num_iterations, num_questions = args.num_questions, num_answers = args.num_answers)

        if not args.hide_answers:
            exam_solver.print_answers(iteration=args.num_iterations-1, num_questions = args.num_questions)

    if not args.hide_scores:
        exam_scorer.calculate_and_print_results()
 
        

if __name__ == "__main__":
    main()
