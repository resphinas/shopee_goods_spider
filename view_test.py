import time
#
# main_time = time.time()
#
# while True:
#     temp_bar_time = time.time()
#     all_time = int(temp_bar_time - main_time)
#     h = int(all_time / 3600)
#     m = int((int(all_time) % 3600) / 60)
#     s = int(int(all_time) % 60)
#     print(h,m,s)
# -*- encoding: utf-8 -*-
# @Time   : 2023/1/13 13:48
# @Author : Vic
import threading
import time
from multiprocessing.dummy import Pool
import ctypes
import multiprocessing

# _print = print
# mutex = threading.Lock()


# def print(text, *args, **kw):
#     with mutex:
#         _print(text, *args, **kw)




class TestPool:

    def __init__(self):
        self.ip = None
        self.mutex = threading.Lock()
        self.flag = flag
    def update_ip(self, i):
        # time.sleep(1)

        self.mutex.locked()
        if self.flag.get():
            self.flag.set(value=False)
            print("come on", i)
            self.mutex.release()
            return "192.168.1.1"
        print(self.flag.get())


        print("坦克====", i)
        return "123.123.123.123"

    def get_ip(self, i):
        ip = "127.0.0.1"
        try:
            1 / 0
        except Exception as e:
            ip = self.update_ip(i)

        # time.sleep(1)
        print(ip, ":", i, "\n", end='')

    def run(self):
        # flag = multiprocessing.Manager().Value(ctypes.c_bool, True)
        # task_list = [{"a": 1, "s": flag}, {"a": 2, "s": flag}, {"a": 3, "s": flag}, {"a": 4, "s": flag},
        #              {"a": 5, "s": flag}]
        task_list = [1, 2, 3, 4, 5]
        pool = Pool(3)
        results = pool.map_async(self.get_ip, task_list, callback=None)
        # results = pool.apply_async(self.star_spider, task_lists[:20])
        pool.close()  # 关闭线程池，不再接受新的线程任务
        pool.join()  # 让主线程阻塞，等待所有子线程执行结束
        results.wait()  # 等待线程函数执行完毕


if __name__ == '__main__':

    multiprocessing.freeze_support()
    _print = print
    mutex = threading.Lock()
    flag = multiprocessing.Manager().Value(ctypes.c_bool, True)


    tp = TestPool()
    tp.run()