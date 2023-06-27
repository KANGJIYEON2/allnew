from pandas import DataFrame

sdata = {
    '국어' : [40, 60, 80, 50, 30],
    '영어' : [55, 65, 75, 85, 30],
    '수학' : [30, 40, 50, 60, 70],
}

myindex = ['강감찬', '이순신', '김유신', '김구','안중근']
myframe = DataFrame(sdata, index=myindex)
print(myframe)

print('\n짝수 행만 읽어보세요')
result = myframe.iloc[0::2]
print(result)

