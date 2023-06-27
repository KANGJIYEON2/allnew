import urllib.request

url = "https://comic.naver.com/webtoon/list?titleId=796152"

savename = input('저장할 파일 이름 입력 : ')
result = urllib.request.urlopen(url)

data = result.read()
print('# type(data : ' + type(data))

with open(savename, mode='wb') as f:
    f.write(data)
    print(savename + 'saved ...')