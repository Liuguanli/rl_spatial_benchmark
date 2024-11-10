import numpy as np

n_query = 10000

w = np.random.uniform(0.0001, 0.001, n_query)
h = np.random.uniform(0.0001, 0.001, n_query)

n = 100000000
data = np.load('./data/data_india_{}.npy'.format(n))
n_sample = 10000
idxList = np.random.choice(n, n_sample, replace=False)
dataSample = data[idxList]
x = dataSample[:, 0]
y = dataSample[:, 1]

x_low = x - w/2
x_high = x + w/2
y_low = y - h/2
y_high = y + h/2

query = np.stack([x_low, y_low, x_high, y_high]).T
print(query.shape)

np.save("./query/query_india_0.0001_0.001_{}.npy".format(n_sample), query)