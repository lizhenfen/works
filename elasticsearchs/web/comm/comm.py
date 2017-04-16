import time
import functools

def outer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start_time = time.time()
        res = func(*args,**kwargs)
        end_time = time.time()
        if isinstance(res,dict):
            res["time"] = '{:.2f}'.format(end_time-start_time)
        return res
    return inner

@outer
def test(a):
    time.sleep(1)
    return a+2

if __name__ == "__main__":
   t =  test(3)
   print(t)