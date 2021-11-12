import time
import numpy as np
import ray

start = time.time()

ray.init(num_cpus=4)


@ray.remote
def no_work(a):
    return


a = np.zeros((5000, 5000))
result_ids = [no_work.remote(a) for x in range(10)]
results = ray.get(result_ids)
print(f"{results=}")
print("duration =", time.time() - start)
# duration = 1.0837509632110596
