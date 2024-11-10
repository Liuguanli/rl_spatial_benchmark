import numpy as np

# f = open("../data/india_locations_shuffle.txt")

# dataList = []
# x = f.readline()
# while(x):
#     y = f.readline()
#     dataList.append([float(x), float(y), float(x), float(y)])
#     x = f.readline()

# data = np.array(dataList)
# print(data.shape)
# np.save("./data/data_india_100000000.npy", data)

n = 100000000
data = np.load('./data/data_india_{}.npy'.format(n))
n_sample = 75000000
idxList = np.random.choice(n, n_sample, replace=False)
dataSample = data[idxList]
print(dataSample.shape)
np.save("./data/data_india_{}.npy".format(n_sample), dataSample)