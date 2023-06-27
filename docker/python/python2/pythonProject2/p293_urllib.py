import urllib.request


url = 'https://postfiles.pstatic.net/MjAyMjExMTZfMjMz/MDAxNjY4NTUzODQ5ODAy.8AejCAjIwjKGtNyCsaCaMsR24Z3yEr9-AV42UIIP_Qcg.TBtLqjYS1sdp-xG_CZ--ha9QbcqfCUgbnHpuZqm5ZZEg.JPEG.eoin0708/KakaoTalk_20221114_071220288_03.jpg?type=w966'

savename = 'urldownload03.png'

result = urllib.request.urlopen(url)

data = result.read()

print('# type(data) : ', type(data))

with open(savename, mode='wb') as f:
    f.write(data)
    print(savename + 'save....')