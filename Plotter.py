# pylint: disable=C
import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy as np

class Plotter(object):

    def __init__(self):
        self.x_pts = []
        self.y_pts = []
        self.min_y = 0
        self.max_y = 0

    def addPoint(self, x, y):
        self.x_pts.append(x)
        self.y_pts.append(y)

        if y < self.min_y:
            self.min_y = y
        elif y > self.max_y:
            self.max_y = y

    def clearPoints(self):
        self.x_pts = []
        self.y_pts = []
        self.min_y = 0
        self.max_y = 0

    def showPlot(self, title="Generic Plot", save_to_file=False):
        plt.xlim(self.x_pts[0], self.x_pts[-1])
        plt.ylim(self.min_y, self.max_y)

        plt.xticks(range(self.x_pts[0], self.x_pts[-1]))
        plt.yticks(np.arange(-6, 3, 0.5))
        plt.title(title)
        plt.plot(self.x_pts, self.y_pts, linestyle="solid", marker="o", color="blue")
        if save_to_file:
            text = open(title + '.txt', 'w')
            text.write(str(self.x_pts) + '\n')
            text.write(str(self.y_pts) + '\n')

            plt.savefig(title + '.png')
        else:
            plt.show()
