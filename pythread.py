import sys
import threading
import time

lock = threading.Lock()
sharedA = 0;
sharedB = 0;

def produceData(lock) :
	global sharedA
	global sharedB
	while (sharedA < 1000000) :
		lock.acquire()
		print(">produce")
		count = 0
		while (count < 145631) :
			sharedA += 1
			sharedA %= 1024
			count += 1
		sharedB = sharedA
		print("<produce")
		lock.release()

thread = threading.Thread(target=produceData,args=(lock,))
thread.daemon = True
thread.start()

while True :
	lock.acquire()
	print(">consume")
	if (sharedA != sharedB) :
		print("FAIL")
	print("<consume")
	lock.release()
	time.sleep(0.2)

