
import random
import pandas as pd

result = []
myColumns = ('번호', '이름', '나이')
myencoding = 'utf-8'

for idx in range(1, 3):
    sublist = []
    sublist.append(100 * idx)
    sublist.append('김철수' + str(idx))
    sublist.append((random.randint(1, 10)))
    result.append(sublist)

myframe = pd.DataFrame(result, columns=myColumns)

m,