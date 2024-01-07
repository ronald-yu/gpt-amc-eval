import json
from typing import List, Dict
from exam import ExamSolver
import os
import pickle

def read_json(path: str):
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

def save_exam_solver(exam_solver: ExamSolver, save_dir: str):
    """
        Saves an exam to a pickle file in save_dir
    """
    file_name = os.path.join(save_dir, f"{exam_solver.solver_name}.pkl")
    with open(file_name, 'wb') as file:
        pickle.dump(exam_solver, file)

def load_exam_solver(exam_name:str, questions: List[Dict[str,str]], args) -> ExamSolver:
    """
        Loads exam questions into a solver. If an exam solver corresponding to the exam and model hyper-parameters has already been saved, we load that exam so that we don't need to solve the exam again
    """
    exam_solver = ExamSolver(exam_name, questions, model = args.model, temperature = args.temperature)
    file_name = os.path.join(args.save_dir, f"{exam_solver.solver_name}.pkl")
    if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                    return pickle.load(file)
    else:
            return exam_solver

def load_exam_solvers(args) -> List[ExamSolver]:
    """
        Loads a list of exam solvers based on the user input args
    """
    ret = []    
    for exam_name in args.file_names:
        questions = read_json(os.path.join(args.data_dir, f"{exam_name}.json"))
        exam_solver = load_exam_solver(exam_name, questions, args)
        ret.append(exam_solver)
    return ret
