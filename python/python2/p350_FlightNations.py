from itertools import count
from p340_FlightUtil import FlightStore

Name = "AirportData"
base_url = "https://www.airport.kr/co/ko/cpr/statisticCategoryOfLocal.do"


def getData():
    savedData = []

    for page_idx in count():
        url = base_url + "?page=" + str(page_idx + 1)
        flightStore = FlightStore(Name, url)
        soup = flightStore.getSoup()

        mytable = soup.find("table", attrs={"class": "table mt20"})
        mytbody = mytable.find("tbody")

        dataExists = False
        for mytr in mytbody.findAll("tr"):
            dataExists = True
            mylist = list(mytr.stripped_strings)
            print(mylist)

            flight_num = mytr.select_one("td:nth-of-type(3)").string
            flight_num = flight_num.strip() if flight_num else ""

            origin = mylist[1]
            destination = mylist[3]

            if len(destination.split()) >= 2:
                imsi = destination.split()
                sido = imsi[0]
                gungu = imsi[1]
            else:
                sido = destination
                gungu = ""

            mydata = [Name, origin, sido, gungu, destination, flight_num]
            savedData.append(mydata)

        if not dataExists:
            flightStore.save2Csv(savedData)
            break


print(Name + " 데이터 크롤링 시작")
getData()
print(Name + " 데이터 크롤링 끝")
