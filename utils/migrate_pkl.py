import io
import pickle


class RenameUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        renamed_module = module
        if module == "exam":
            renamed_module = "exam.solver"

        return super(RenameUnpickler, self).find_class(renamed_module, name)


def renamed_load(file_obj):
    return RenameUnpickler(file_obj).load()

fn = "examsolver_amc10a_2023_gpt-4_temperature0.7.pkl"
with open(f"saved_solversbk/{fn}", "rb") as f:
    temp = renamed_load(f)

with open(f"saved_solvers/{fn}", "wb") as f:
    pickle.dump(temp, f) 
