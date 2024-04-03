import time
import json
row = column = 24
start = time.time()
bits =  [[[]for _ in range(column)] for _ in range(row)]    

for j in range(row):
                for i in range(column):

                    bits[i][j].append((i,j))
                    bits[i][j].append(False)
                    bits[i][j].append(0)
end = time. time()
duration = end - start
print(duration)
with open('./Tests/Dic.py','w') as f:
    json.dump(bits,f,indent=4)


start = time.time()
a = bin(2**(row*column))

with open('./Tests/Bin.py','w') as f:
    json.dump(a,f,indent=4)
end = time. time()
duration = end - start
print(duration)
# result mor or less same time but more storing space...
# i just want to something with bitmanipulation
