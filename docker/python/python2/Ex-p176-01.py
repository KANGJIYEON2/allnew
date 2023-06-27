import numpy as np
from pandas import Series


mylist = [200, 300, 400, 100]
mySeries = Series(data=mylist, index=['손오공', '저팔계', '사오정', '삼장법사'])


mySeries.index.name = '실적 현황'
print('\n# 시리즈의 색인 이름')
print(mySeries.index.name)

mySeries.index.name = '직원 실정'
print('\n# 시리즈의 이름')
print(mySeries.name)

print('\n# 반복하여 출력해보기')
for idx in mySeries.index:
    print('색인 : ' + idx + ',값:' + str(mySeries[idx]))