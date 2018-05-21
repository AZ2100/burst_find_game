import burst_displayer
import util
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import time
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

plt.ion()


class GamePlayer:
    def __init__(self, root_file="../game_data"):
        self.data = util.load_data(root_file)
        self.current_index = 0
        self.indexes = range(len(self.data))
        np.random.seed(0)
        np.random.shuffle(self.indexes)

        self.playing = True

        self.root = Tk.Tk()
        self.root.wm_title("Burst Detect Game")
        self.root.bind('<Return>', self._jump)
        self.fig = Figure(figsize=(15, 6), dpi=100, tight_layout=False)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.root)

        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        current_data = self.data[self.indexes[self.current_index]]
        self.current_game = burst_displayer.BurstDetectHighlighter(current_data["signal"], current_data["df_f"],
                                                                   self.fig, self.canvas)
        self.current_segments = []

        self.number_template = "Current Signal Index = {} and Name = {}"
        self.number_label = None
        self.jump_input = None
        self.setup_labels()
        Tk.mainloop()

    def setup_labels(self):
        jump_label = Tk.Label(master=self.root, text="Jump to")
        self.jump_input = Tk.Entry(master=self.root)
        jump_button = Tk.Button(master=self.root, text="Jump", command=self._jump)

        jump_button.pack(side=Tk.RIGHT)
        self.jump_input.pack(side=Tk.RIGHT)
        jump_label.pack(side=Tk.RIGHT)

        current_data = self.data[self.indexes[self.current_index]]
        self.number_label = Tk.Label(master=self.root, text=self.number_template.format(current_data["global_n"],
                                                                                        current_data["title"]))
        self.number_label.place(relx=0.5, rely=0.01, anchor=Tk.CENTER)

        p_button = Tk.Button(master=self.root, text='Previous', command=self._prev)
        q_button = Tk.Button(master=self.root, text='Quit', command=self._quit)
        n_button = Tk.Button(master=self.root, text='Next', command=self._next)

        p_button.place(relx=0.4, rely=0.9, anchor=Tk.CENTER)
        q_button.place(relx=0.5, rely=0.9, anchor=Tk.CENTER)
        n_button.place(relx=0.6, rely=0.9, anchor=Tk.CENTER)

    def _prev(self):
        if self.playing and self.current_index > 0:
            self.current_index -= 1
            self.fig.clf()
            current_data = self.data[self.indexes[self.current_index]]
            self.current_segments = []
            self.current_game = burst_displayer.BurstDetectHighlighter(current_data["signal"], current_data["df_f"],
                                                                       self.fig, self.canvas)
            self.number_label["text"] = self.number_template.format(current_data["global_n"],
                                                                    current_data["title"])

        elif not self.playing:
            self.fig.clf()
            self.playing = True
            current_data = self.data[self.indexes[self.current_index]]
            self.current_game = burst_displayer.BurstDetectHighlighter(current_data["signal"], current_data["df_f"],
                                                                       self.fig, self.canvas,
                                                                       self.current_segments)

    def _next(self):
        current_data = self.data[self.indexes[self.current_index]]
        if self.playing:
            self.current_segments = self.current_game.segments
            self.playing = False
            self.fig.clf()
            self.current_game = burst_displayer.BurstDetectShower(current_data["signal"], self.fig, self.canvas,
                                                                  self.current_segments,
                                                                  current_data['df_f'])
        else:
            if len(self.current_segments) > 0:
                save_path = os.path.join(current_data["out_path"], str(int(time.time())))
                util.csv_save(self.current_segments, save_path+"-gold-segments.csv")

            self.playing = True
            self.fig.clf()
            self.current_index += 1
            current_data = self.data[self.indexes[self.current_index]]
            self.current_segments = []
            self.current_game = burst_displayer.BurstDetectHighlighter(current_data["signal"], current_data["df_f"],
                                                                       self.fig, self.canvas)
            self.number_label["text"] = self.number_template.format(current_data["global_n"],
                                                                    current_data["title"])

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _jump(self, event=None):
        self.canvas._tkcanvas.focus_set()
        a = str(self.jump_input.get())
        if a.isdigit():
            index = next((i for i in range(len(self.data)) if self.indexes[i] == int(a)), -1)
            if index != -1:
                self.current_index = index
                current_data = self.data[self.indexes[self.current_index]]
                self.playing = True
                self.current_segments = []
                self.fig.clf()
                self.current_game = burst_displayer.BurstDetectHighlighter(current_data["signal"], current_data["df_f"],
                                                                           self.fig, self.canvas)
                self.number_label["text"] = self.number_template.format(current_data["global_n"],
                                                                        current_data["title"])
                return

        print("please only give integers from 0 - N")
