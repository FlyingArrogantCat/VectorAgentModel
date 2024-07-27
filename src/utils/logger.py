from pathlib2 import Path

import shutil
import datetime


class Logger:
    def __init__(self, path: str, name_experiment: str):
        date_now = str(datetime.datetime.now())[:19].replace(':', '_')
        date_now = date_now.replace('-', '_')
        date_now = date_now.replace(' ', '_')

        self.path = Path(path) / name_experiment / date_now

        if self.path.exists():
            shutil.rmtree(str(self.path))
            self.path.mkdir()
        
        self.indx = 0

    
    def save_data(self, data):
        pass