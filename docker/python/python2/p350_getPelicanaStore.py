from itertools import count
from p340_ChickenUtil import ChickenStore

brandName = "pelicana"
base_url = "https://www.pelicana.co.kr/store/stroe_search.html"


def getData():
    savedData = []

    for page_idx in count():
        url = base_url + "?page=" + str(page_idx + 1)
        chknStore = ChickenStore(brandName, url)
        soup = chknStore.getSoup()

        mytable = soup.find("table", attrs={"class": "table mt20"})
        mytbody = mytable.find("tbody")

        shopExists = False
        for mytr in mytbody.findAll("tr"):
            shopExists = True
            mylist = list(mytr.stripped_strings)
            print(mylist)

            imsiphone = mytr.select_one("td:nth-of-type(3)").string
            phone = imsiphone.strip() if imsiphone else ""

            store = mylist[1]
            address = mylist[3]

            if len(address.split()) >= 2:
                imsi = address.split()
                sido = imsi[0]
                gungu = imsi[1]
            else:
                sido = address
                gungu = ""

            mydata = [brandName, store, sido, gungu, address, phone]
            savedData.append(mydata)

        if not shopExists:
            chknStore.save2Csv(savedData)
            break


print(brandName + " 매장 크롤링 시작")
getData()
print(brandName + " 매장 크롤링 끝")
