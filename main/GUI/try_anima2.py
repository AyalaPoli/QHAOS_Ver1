import matplotlib
matplotlib.use('Qt5Agg') #use Qt5 as backend, comment this line for default backend
import PyQt5
from matplotlib import pyplot as plt
from matplotlib import animation
import random

def animate(i, x=[], y=[]):
    plt.cla()
    x.append(i)
    y.append(random.randint(0, 10))
    plt.plot(x, y)


if __name__ == "__main__":
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, animate, interval=700)
    plt.show()