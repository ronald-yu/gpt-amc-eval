import json
from typing import List, Dict, Tuple
from exam.solver import ExamSolver
from exam.scorer import ExamScorer
import os
import pickle

def read_json(path: str) -> None:
    """
        Reads a json file corresponding to an exam
    """
    with open(path, 'r') as fh:
        ret = []
        for line in fh.readlines():
                line = line.replace('\\', '\\\\')
                d = json.loads(line.replace('\\', '\\\\'))
                for k in d:
                        d[k] = d[k].replace('\\\\','\\')
                ret.append(d)
        return ret


def load_exam_solver(exam_name:str, questions: List[Dict[str,str]], args) -> ExamSolver:
    """
        Loads exam questions into a solver. If an exam solver corresponding to the exam and model hyper-parameters has already been saved, we load that exam so that we don't need to solve the exam again.
        Also load an exam scorer that aggregates scores and statistics over all the exam solvers.
    """
    exam_solver = ExamSolver(exam_name, questions, model = args.model, temperature = args.temperature, prompt_type = args.prompt_type)
    file_name = os.path.join(args.save_dir, f"{exam_solver.solver_name}.pkl")
    if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                    exam_solver = pickle.load(file)
    # override the save_dir with the config
    exam_solver.save_dir = args.save_dir
    return exam_solver

def load_exams(args) -> Tuple[List[ExamSolver], ExamScorer]:
    """
        Loads a list of exam solvers based on the user input args
    """
    exam_solvers = []    
    for exam_name in args.file_names:
        questions = read_json(os.path.join(args.data_dir, f"{exam_name}.json"))
        exam_solver = load_exam_solver(exam_name, questions, args)
        exam_solvers.append(exam_solver)
    exam_scorer = ExamScorer( exam_solvers, abstain_score = args.abstain_score, ensemble_size = args.ensemble_size)
    return exam_solvers, exam_scorer
