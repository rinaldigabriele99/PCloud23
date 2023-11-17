from requests import get, post
import time
import csv

base_url = 'http://localhost:8080'
#base_url = 'https://mamei-test2-382313.appspot.com'

sensor = 's8'

for i in range(10):
    print(sensor,'invio....')
    #r = post(f'{base_url}/sensors/{sensor}',data={'val': i})
    time.sleep(1)


with open("./mappa_monumenti_italia.csv", newline="", encoding="ISO-8859-1") as filecsv:
    lettore = csv.reader(filecsv,delimiter=";")
    header = next(lettore)
    print(header)

print('done')