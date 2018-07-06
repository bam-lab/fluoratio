#!/usr/local/bin/python3

# You can run the following only in Python 3. It has been tested in 3.6.5.

import multiprocessing as mp
import time


def square(x):
    return x*x


# You can edit trials and square_range to change testing parameters
trials = 10
square_range = 10000000

times = []*trials
cpu_num = int(mp.cpu_count())
cpu_avgs = []*cpu_num

for j in range(cpu_num):
    for i in range(trials):
        start = time.time()
        # Worker pool
        if __name__ == '__main__':
            # "with" will close the pool once the task is complete
            with mp.Pool(processes=(j+1)) as pool:
                pool.map(square, range(square_range))
        end = time.time()
        print("Trial {}:".format(i+1), str(end-start), "seconds")
        times.append(end-start)
    avg = sum(times)/len(times)
    print("{} cpu avg:".format(j+1), avg, "seconds")
    cpu_avgs.append(avg)

print("Optimum cpu count:", (cpu_avgs.index(min(cpu_avgs)))+1)
