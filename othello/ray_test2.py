import ray
import time
import random


class Lists:
    def __init__(self):
        self.list = []

    def add(self, item):
        self.list.append(item)


@ray.remote
def f(lists):
    for i in range(10):
        lists.add(random.randint(0, 100))
    return lists.list


if __name__ == "__main__":
    start_time = time.time()
    lists = Lists()
    ray.init(num_cpus=2)
    f_ids = [f.remote(lists) for i in range(2)]
    returned = ray.get(f_ids)
    concat = [item for sublist in returned for item in sublist]
    print(concat)
    print(returned)

    print("--- %s seconds ---" % (time.time() - start_time))

