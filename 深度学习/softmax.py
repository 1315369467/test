import torch
import torch.nn as nn
import numpy as np

a = np.asarray([[[[1,1,1],[2,2,2]],
                [[3,3,3],[4,10,10]]],

                [[[1,1,1], [2,2,2]],
                 [[3,3,3], [4,10,10]]]
                ],np.float32)
print(a.shape)  #(2, 2, 2, 3)

input = torch.from_numpy(a)
print("input: ",input)

m0 = nn.Softmax(dim=0)
output0 = m0(input)
print("output0: ",output0)

m1 = nn.Softmax(dim=1)
output1 = m1(input)
print("output1: ",output1)

m2 = nn.Softmax(dim=2)
output2 = m2(input)
print("output2: ",output2)

m3 = nn.Softmax(dim=3)
output3 = m3(input)
print("output3: ",output3)