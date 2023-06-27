import numpy as np

a = np.array([-1, 3, 2, -6])
b = np.array([3, 6, 1, 2])
A = np.reshape(a, [2, 2])
B = np.reshape(b, [2, 2])
print(A)
print(B)

resuLt3_1 = np.matmul(A, B)
resuLt3_2 = np.matmul(B, A)
print(resuLt3_1)
print(resuLt3_2)

a = np.reshape(a, [1, 4])
b = np.reshape(b, [1, 4])
b2 = np.transpose(b)
print(b2)

result4 = np.matmul(a, b2)
print("\nsol4-1")
print(result4)