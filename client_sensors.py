from requests import get, post
import time
import csv
import json
import pandas as pd

base_url = 'http://localhost:8080'
#base_url = 'https://mamei-test2-382313.appspot.com'

'''
for i in range(10):
    print(sensor,'invio....')
    r = post(f'{base_url}/sensors/{sensor}',data={'val': i})
    time.sleep(1)

'''

with open('MiningProcess_Flotation_Plant_Database.csv', 'r') as file_csv:
    csv_reader = csv.reader(file_csv)   
    #data = []
    conta = 0
    chiavi = ['date', '%IronFeed', '%SilicaFeed', 'StarchFlow', 'AminaFlow', 'OrePulpFlow'
              , 'OrePulppH', 'OrePulpDensity', 'FlotationColumn01AirFlow', 'FlotationColumn02AirFlow'
              , 'FlotationColumn03AirFlow', 'FlotationColumn04AirFlow', 'FlotationColumn05AirFlow'
              , 'FlotationColumn06AirFlow', 'FlotationColumn07AirFlow', 'FlotationColumn01Level'
              , 'FlotationColumn02Level', 'FlotationColumn03Level', 'FlotationColumn04Level'
              , 'FlotationColumn05Level', 'FlotationColumn06Level', 'FlotationColumn07Level', '%IronConcentrate'
              , '%SilicaConcentrate']
    for row in csv_reader:  
        if conta == 0:
            conta += 1
            continue
        sensor = 's' + str(conta)
        row_dict = {}
        for ind,chiave in enumerate(chiavi):
            row_dict[chiave] = row[ind]
        #data.append(row_dict)       
        #json_data = json.dumps(row_dict, indent=2) 
        r = post(f'{base_url}/sensors/{sensor}', data = row_dict)
        print('invio..')
        time.sleep(1)
        conta +=1
        #if conta == 10:
        #    break


# Converti la lista di dizionari in formato JSON
#json_data = json.dumps(data, indent=2)

# Stampa il risultato

print('done')