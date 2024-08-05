from pathlib2 import Path

import shutil
import datetime
import pickle

class Logger:
    def __init__(self, path: str, name_experiment: str):
        date_now = str(datetime.datetime.now())[:19].replace(':', '_')
        date_now = date_now.replace('-', '_')
        self.date_now = date_now.replace(' ', '_')

        self.path = Path(path) / name_experiment / self.date_now

        if self.path.exists():
            shutil.rmtree(str(self.path))
            self.path.mkdir()
        
        self.log_file_path = self.path / "log.txt"
        self.error_file_path = self.path / "std_log.err"
        self.indx = 0

    def check_obj_licklable(self, obj):
        is_pickable = True

        try:
            temp = pickle.dumps(obj)
            is_pickable = True
        except:
            is_pickable = False
        
        return is_pickable

    def log(self, string: str):
        with open(str(self.log_file_path), "a" ) as file:
            file.write(string)

    def error(self, string:str):
        with open(str(self.error_file_path), "a" ) as file:
            file.write(string)

        raise ValueError

    def save_data(self, data):
        pass