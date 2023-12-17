import matplotlib.pyplot as plt
import math
import statistics
import argparse


parser = argparse.ArgumentParser(description="Рассчет угловой скорости по файлу данных")
parser.add_argument("-w", "--window", type=int, default=10, help="Размер окна для вычисления среднего скользящего")
parser.add_argument("-s", "--step",type=int, default=100, help="Размер шага для вычисления скорости")
parser.add_argument("-f", "--file", default="data.txt", help="Название файла")

def remove_duplicate(time_list, value_list):
    new_time_list = []
    new_value_list = []
    for time, value in zip(time_list, value_list):
        if value not in new_value_list:
            new_time_list.append(time)
            new_value_list.append(value)

    return new_time_list, new_value_list

def get_wt(t, w, step=1):
    last_w = w[0]
    last_t = t[0]
    wt_list = []

    for time, value in zip(t[1::step], w[1::step]):
        wt = ((value - last_w) * math.pi/180)  / ((time - last_t)/1000)
        wt_list.append(wt)
        last_t = time
        last_w = value

    return wt_list


def mean_array(arr, win=10):
    win = win // 2
    new_arr = []
    len_arr = len(arr)
    for index in range(len_arr):

        if index - win < 0:
            l_arr = [0] * win
        else:
            l_arr = arr[index-win: index]

        if index + win >= len_arr:
            r_arr = [0]
        else:
            r_arr = arr[index+1: index+win+1]

        val = statistics.mean(l_arr + [arr[index]] + r_arr)
        new_arr.append(val)

    return new_arr

def main():
    args = parser.parse_args()
    with open(args.file, 'r', encoding='utf8') as file:
        lines = list(map(lambda s: s.replace(' \n', ''), file.readlines()))
        lines[-1] = lines[-1][:-1]
        w = []
        t = []

        for line in lines:
            values = list(map(float, line.split(' ')))
            t.append(values[0])
            w.append(values[1])

        t, w = remove_duplicate(t, w)

        f, (ax1, ax2, ax3) = plt.subplots(1, 3)
        f.set_figheight(4)
        f.set_figwidth(13)

        wt_list = get_wt(t, w)

        ax1.plot(t[1:], wt_list)
        ax1.set_title("График без дубликатов")
        ax1.grid()

        mean_w = mean_array(wt_list, args.window)

        ax2.plot(t[1:], mean_w)
        ax2.set_title("График с средним скользящим")
        ax2.set_ylim([0, 10])
        ax2.grid()

        step = args.step

        wt_list = get_wt(t, w, step)

        ax3.plot(t[1::step], wt_list)
        ax3.set_title("График с шагом")
        ax3.grid()
       
        # for i in range(130,220, 30):
        #     step = i
        #     wt_list = get_wt(t, w, step)
        #     plt.plot(t[1::step], wt_list)

        # step = 200
        # wt_list = get_wt(t, w, step)
        # plt.plot(t[1::step], wt_list)
        # plt.title("График с шагом")
        # plt.grid()

        plt.show()

if __name__ == '__main__':
    main()