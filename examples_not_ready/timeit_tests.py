
import timeit

ex1 = 'from examples_not_ready.py_video_with_recorder_advance import example_entry_point as ex1; ex1()'
ex1_th = 'from examples_not_ready.py_video_with_recorder_advance_threaded import example_entry_point as ex1_th; ex1_th()'


t1 = timeit.timeit(ex1, number=4)
t2 = timeit.timeit(ex1_th, number=4)


print(t1)
print(t2)
x = 1
