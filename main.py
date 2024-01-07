import argparse
from io import load_exam_solvers, save_exam

def main():
    parser = argparse.ArgumentParser(description="Arguments for OpenAI API")

    # IO arguments    
    parser.add_argument('--file-names',nargs='+', type=str, help='Specify list of input files', default = ['amc10a_2023'])
    parser.add_argument('--data-dir', type=str, help='Directory to save the exam results in', default = 'data')
    parser.add_argument('--save-dir', type=str, help='Directory to save the exam results in', default = 'solvers')

    # Solver Hyperparameters
    parser.add_argument('--model', type=str, help='Specify which OpenAI model to use', default = 'gpt-3.5-turbo', choices=['gpt-3.5-turbo', 'gpt-4'])
    parser.add_argument('--temperature', type=float, help='Specify temperature of the model', default = '1.0')


    # Solve configurations
    parser.add_argument('--num-answers', type=int, help='Number of answers to sample for each question', default = 1)
    parser.add_argument('--num-questions', type=int, help='Number of questions to solve. By default, solve the whole exam.', default = 25)
    
    args = parser.parse_args()

    exam_solvers = load_exam_solvers(args.file_names, data_dir = args.data_dir, save_dir = args.save_dir)

    for exam_solver in exam_solvers:
        exam_solver.solve(num_questions = args.num_questions, num_answers = args.num_answers)
        save_exam_solver(exam_solver, args.data_dir)
 
        

if __name__ == "__main__":
    main()
