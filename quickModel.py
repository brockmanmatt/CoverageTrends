import multiprocessing, time

def print_i():
    i = 0
    while True:
        print (i)
        i+=1
        time.sleep(1)

print("starting")
process = multiprocessing.Process(target=print_i)
process.start()

time.sleep(30)
process.terminate()
