import numpy as np
import matplotlib.pyplot as plt
import filtering
plt.ion()


class BurstDetectHighlighter(object):
    def __init__(self, y, my_df_f, fig, canvas, segments=None):
        if segments is None:
            segments = []
        y = y-y.min()
        y /= y.max()
        self.fig = fig
        self.canvas = canvas
        self.ax = self.fig.add_subplot(111)

        self.x_down = False
        self.last_x = None
        self.current_x = None

        self.segments_updated = True

        self.segments = segments

        self.N = len(y)

        self.ax.plot(y, label='signal')
        df_f = classic_df_f(y)
        self.ax.plot(df_f, label='classic_df_f')
        self.ax.plot(my_df_f, label='my_df_f')
        self.ax.fill_between([], 0, 0, alpha=0.5, color='b', label="bursts")

        self.max = max((max(y), max(df_f)))
        self.min = min((0, min(y), min(df_f)))

        self.fills = list()
        self.do_fills()

        self.fig.legend()


        self.canvas.draw()
        self.init_plt_events()

    def init_plt_events(self):
        self.canvas.mpl_connect('button_press_event', self.on_mouse_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('key_release_event', self.on_key_release)

    def do_fills(self):
        fills = []
        if self.last_x is not None:
            segment = sorted([self.last_x, self.current_x])
            fills.append(self.ax.fill_between(np.arange(*segment), self.min, self.max, alpha=0.5, color='b'))

        if self.segments_updated:
            for segment in self.segments:
                fills.append(self.ax.fill_between(np.arange(*segment), self.min, self.max, alpha=0.5, color='b'))
        self.fills = fills

    def clean_fills(self):
        for fill in self.fills:
            fill.remove()

    def on_mouse_click(self, event):
        ix, iy = event.xdata, event.ydata
        if ix is not None:
            if self.x_down:
                self.remove_segment_under(ix)
                self.clean_fills()
                self.do_fills()
                self.canvas.draw()
                return
            self.last_x = max(min(int(ix), self.N), 0)
            self.current_x = max(min(int(ix), self.N), 0)

    def on_mouse_move(self, event):
        ix, iy = event.xdata, event.ydata
        if ix is not None:
            self.current_x = max(min(int(ix), self.N), 0)
        self.clean_fills()
        self.do_fills()
        self.canvas.draw()

    def on_mouse_release(self, event):
        if self.last_x is not None:
            if self.x_down:
                return

            if self.last_x != self.current_x:
                self.segments.append(sorted([self.last_x, self.current_x]))
                self.segments_updated = True
            self.last_x = None

    def on_key_press(self, event):
        if event.key == 'x':
            self.x_down = True

    def on_key_release(self, event):
        if event.key == 'x':
            self.x_down = False

    def remove_segment_under(self, ix):
        index = next((i for i in range(len(self.segments)) if self.segments[i][1] >= ix >= self.segments[i][0]), -1)
        if index >= 0:
            self.segments.pop(index)
            self.segments_updated = True


class BurstDetectShower:
    def __init__(self, y, fig, canvas, segmentsA, my_df_f, threshold=0.1, min_length=15):
        _, self.segmentsB = filtering.burst_detect(y, threshold=threshold, min_length=min_length)

        y = y-y.min()
        y /= y.max()
        self.fig = fig
        self.canvas = canvas
        self.ax = self.fig.add_subplot(111)

        self.playing = None
        self.return_msg = None

        self.segmentsA = segmentsA


        self.N = len(y)

        self.ax.plot(y, label='signal')
        df_f = classic_df_f(y)
        self.ax.plot(df_f, label='classic_df_f')
        self.ax.fill_between([], 0, 0, alpha=0.5, color='b', label="your_bursts")
        self.ax.fill_between([], 0, 0, alpha=0.5, color='r', label="my_bursts")
        self.ax.plot(my_df_f, label='my_df_f')

        self.max = max((max(y), max(df_f), max(my_df_f)))
        self.min = min((0, min(y), min(df_f), min(my_df_f)))

        self.fig.legend()

        self.do_fills()
        self.canvas.draw()

    def do_fills(self):
        for segment in self.segmentsA:
            self.ax.fill_between(np.arange(*segment), self.min, self.max, alpha=0.5, color='b')

        for segment in self.segmentsB:
            self.ax.fill_between(np.arange(*segment), self.min, self.max, alpha=0.5, color='r')


def classic_df_f(signal):
    mean = np.mean(signal[0:20])
    return (signal-mean)