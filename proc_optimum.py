import multiprocessing as mp
import time


def doer(x):
    return x*x


loops = 10
times = []*loops
cpu_num = int(mp.cpu_count())
cpu_avgs = []*cpu_num

for j in range(cpu_num):
    for i in range(loops):
        start = time.time()
        if __name__ == '__main__':
            with mp.Pool(processes=(j+1)) as pool:
                pool.map(doer, range(1000000000))
        end = time.time()
        print("Trial {}:".format(i+1), str(end-start), "seconds")
        times.append(end-start)
    avg = (sum(times))/len(times)
    print("{} cpu avg:".format(j+1), avg, "seconds")
    cpu_avgs.append(avg)

print("Optimum cpu count:", (cpu_avgs.index(min(cpu_avgs)))+1)
