import pickle
import math

from pylab import *
from numpy import *


def plot_graph(v1, v2, xl, yl, dot="k.", grid_type=True):
    plot(v1, v2, dot)
    xlabel(xl)
    ylabel(yl)
    grid(grid_type)
    file_name = yl.replace(r"/", "_").replace(" ", "_") + ".png"
    savefig(file_name)

def plot_case(v1, v2, yl_1, yl_2, xl= r"Log10(Network size, n)"):
    sf = [float(x) for x in summary[v1]]
    n = [math.log10(float(x)) for x in summary['nsize']]
    #plot_graph(n, sf, xl=xl, yl=yl_1)

    r_sf = [float(x) for x in summary[v2]]
    div = list()
    for index, i in enumerate(r_sf):
        if i != 0:
            div.append(float(sf[index])/float(i))
        else:
            div.append(0.0)
    plot_graph(n, div, xl=xl, yl=yl_2)

if __name__=="__main__":
    f = open("PS3_4.pik")
    summary = pickle.load(f)

    # 1. Student/Faculty
    yl_1 = "Student/Faculty status Q"
    yl_2 = "Student/Faculty status Q/Qrand"
    v1 = "stu_fac"
    v2 = "stu_fac_rand_mean"
    plot_case(v1, v2, yl_1, yl_2)

    # 2. Major
    yl_1 = "Major Q"
    yl_2 = "Major Q/Qrand"
    v1 = "major"
    v2 = "major_rand_mean"
    plot_case(v1, v2, yl_1, yl_2)

    # 3. Degree
    yl_1 = "Degree Q"
    yl_2 = "Degree Q/Qrand"
    v1 = "degree"
    v2 = "degree_rand_mean"
    plot_case(v1, v2, yl_1, yl_2)
