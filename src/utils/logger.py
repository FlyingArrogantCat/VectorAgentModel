from pathlib2 import Path
from matplotlib import pyplot as plt
import numpy as np
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
        self.path.mkdir(parents=True)
        
        self.log_file_path = self.path / "log.txt"
        self.error_file_path = self.path / "std_log.err"
        self.indx = 0

        self.history = []
        self.time = []
        self.list_colors = ['green', 'tan', 'cyan', 'purple', 'black', 'red', 'blue', 'orange']

    def check_obj_picklable(self, obj):
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

    def save_data(self, data, data_name=""):
        with open(str(self.path/(data_name + ".data")), "ab" ) as file:
            file.write(pickle.dumps(data))

    def draw_pics(self, agents_set, cultures_set, epoch):
        gen_amt = np.zeros(len(cultures_set))

        for agent in agents_set:
            gen_amt[agent.culture_indx] += 1
        self.history.append(gen_amt)
        self.time.append(epoch)

        plt.rcParams.update({'font.size': 16})
        fig = plt.figure(1, figsize=(15, 12))

        history = np.array(self.history)
        for indx in range(len(cultures_set)):
            plt.plot(self.time, 
                     history[:, indx], 
                     label=f"Culture {indx}", 
                     color=self.list_colors[indx],
                     #linestyle='dashed', 
                     linewidth=3)

        plt.title("Численность культур")
        plt.xlabel("Число итераций")
        plt.ylabel("Численность")
        plt.grid(visible=True)
        fig.legend()

        plt.savefig(str(self.path / f"numbers_{epoch}.png"))
        plt.close()

