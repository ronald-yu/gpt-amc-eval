import json
from typing import List
from exam import ExamSolver

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
        pickle.dump(self, file)

def load_exam_solver(exam_name:str, questions: List[Dict[str, str]], save_dir: str) -> ExamSolver:
    """
        Loads exam questions from the json file. If an exam solver corresponding to the exam and model hyper-parameters has already been saved, we load that exam so that we don't need to solve the exam again
    """
    exam = ExamSolver(exam_name, questions, model = args.model, temperature = args.temperature)
    exam_file_name = os.path.join(save_dir, f"{self.solver_name}.pkl")
    if os.path.exists(exam_file_name):
            with open(exam_file_name, 'rb') as file:
                    return pickle.load(file)
    else:
            return exam

def load_exam_solvers(file_names: List[str], data_dir="data", save_dir = "solvers") -> List[ExamSolver]:
    """
        Loads a list of exams from a list of file names and relevant data and save directories.
    """
    ret = []    
    for exam_name in file_names:
        questions = read_json(os.path.join(data_dir, exam_name)))
        exam_solver = load_exam_solver(exam_name, questions, save_dir)
        ret.append(exam_solver)
    return ret
