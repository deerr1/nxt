import matplotlib.pyplot as plt
import numpy as np
import math


class Integrator:

    def __init__(self, delta_t=0.0001):
        self._delta_t = delta_t
        self._last_value = 0

    def integrate(self, value):
        value = value * self._delta_t + self._last_value
        self._last_value = value
        return value
    

def main():
    w = 7
    k_p = 20
    k_m = 1.02603739996293e-2
    k_e = 0.011208503
    L = 4.7e-3
    R = 7.7
    M_fr = 0
    J = 1.03e-6
    n = 48
    delta_t = 1e-4
    integrator1 = Integrator(delta_t)
    integrator2 = Integrator(delta_t)
    integrator3 = Integrator(delta_t)

    feedback_R = 0
    feedback_ke = 0
    feedback_w = 0

    data = [[], [], []]

    for _ in range(10**5):
        value = w - feedback_w
        value = value * k_p
        value = np.clip(value, -1, 1)

        value = value - feedback_R - feedback_ke
        value = value * 1/L
        value = integrator1.integrate(value)
        data[0].append(value)

        feedback_R = value * R
        value = value * k_m
        value = value + M_fr
        value = value * 1/J
        value = integrator2.integrate(value)
        feedback_w = value
        data[1].append(value)

        feedback_ke = value * k_e
        value = integrator3.integrate(value)
        value = value * 1/n
        data[2].append(value)

    time = np.arange(0, 10, 1e-4)

    f, (ax1, ax2, ax3) = plt.subplots(1, 3)
    f.set_figheight(4)
    f.set_figwidth(13)
    
    ax1.plot(time, data[0])
    ax1.grid()
    ax1.set_title("График зависимости\nсилы тока от времени")
    ax1.set_ylabel("I, A")
    ax1.set_xlabel("t, c")


    ax2.plot(time, data[1])
    ax2.grid()
    ax2.set_title("График зависимости\nугловой скорости от времени")
    ax2.set_ylabel("w_nls, рад/с")
    ax2.set_xlabel("t, c")
    

    ax3.plot(time, data[2])
    ax3.grid()
    ax3.set_title("График зависимости\nугла поворота от времени")
    ax3.set_ylabel("angle, рад/с")
    ax3.set_xlabel("t, c")

    plt.show()

if __name__ == '__main__':
    main()