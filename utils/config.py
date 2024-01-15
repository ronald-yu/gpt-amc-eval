import argparse

def get_command_line_args():
    parser = argparse.ArgumentParser(description="Arguments for OpenAI API")

    # IO arguments    
    parser.add_argument('--file-names',nargs='+', type=str, help='Specify list of input files', default = ['amc10a_2023'])
    parser.add_argument('--data-dir', type=str, help='Directory to save the exam results in', default = 'data')
    parser.add_argument('--save-dir', type=str, help='Directory to save the exam results in', default = 'saved_solvers')

    # Solver Hyperparameters
    parser.add_argument('--model', type=str, help='Specify which OpenAI model to use', default = 'gpt-3.5-turbo', choices=['gpt-3.5-turbo', 'gpt-4'])
    parser.add_argument('--temperature', type=float, help='Specify temperature of the model', default = '0.7')


    # Solving Configurations
    parser.add_argument('--num-answers', type=int, help='Number of answers to sample for each question', default = 1)
    parser.add_argument('--num-questions', type=int, help='Number of questions to solve. By default, -1 solves the whole exam.', default = -1)
    parser.add_argument('--skip-questions', type=int, help='How many questions to skip', default = 0)
    parser.add_argument('--regrade', action='store_true', help='Clear all saved final answer so that we can manually review them again')
    parser.add_argument('--num-iterations', type=int, help='Number of chat completion iterations to go through for every answer', default = 1)

    # Scorer Configurations
    parser.add_argument("--abstain-score", type=float, help="Spcify how many points to award for abstaining to answer. By default, use the AMC scoring method of awarding 1.5", default = '1.5')
    parser.add_argument("--ensemble-size", type=int, help="How large each ensemble should be when aggregating results from multiple runs.", default = '1')
    parser.add_argument("--hide-answers", action="store_true", help="Don't print any answers.")
    parser.add_argument("--hide-incomplete-runs", action="store_true", help="Hide results for incomplete exam runs.")
    parser.add_argument("--hide-scores", action="store_true", help="Don't print any scores at all.")
    
    return parser.parse_args()


