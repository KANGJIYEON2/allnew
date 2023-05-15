import pandas as pd

mystorefile = 'store.csv'
mystore = pd.read_csv(mystorefile, encoding='utf-8', index_col=0, header=0)
print('\n매장 테이블')
print(mystore)

disctrictfile = 'store.csv'
district = pd.read_csv(disctrictfile, encoding='utf-8', index_col=0, header=0)
print('\n행정구역 테이블')
print(district)

result = pd.merge(mystore, district)

result = pd.merge(mystore, district, on=['sido', 'gungu'], how='outer', suffixes=['', ' '], indicator=True)
print('\nMerge Result')
print(result)

m_result = result.query('_merge == "left_only"')
print('\n좌측에만 있는 행')
print(m_result)

gungufile = open('./gungufile.txt', encoding='utf-8')
gungu_list = gungufile.readlines()

gungu_dict = {}
for onegu in gungu_list:
    mydata = onegu.replace('\n', '').split(':')
    gungu_dict[mydata[0]] = mydata[1]

print('\n군구 사전 내용')
print(gungu_dict)

print('\n수정된 기계정보 출력')
print(mystore)