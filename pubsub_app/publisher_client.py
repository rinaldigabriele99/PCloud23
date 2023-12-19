from google.cloud import pubsub_v1
from secret import project_id, topic_name
from google.auth import jwt
import time
import csv
import json

#meccanismo di autenticazione con pubsub service account
service_account_info = json.load(open("credentials_pubsub.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=audience)

#oggetto che ci consentirà di inviare messaggi al pubsub
publisher = pubsub_v1.PublisherClient(credentials=credentials)

#canale in cui uno pubblica e uno riceve informazioni
topic_path = publisher.topic_path(project_id, topic_name)
try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(e)


#leggi file e pubblica
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
        json_data = json.dumps(row_dict, indent=2) 
        #r = post(f'{base_url}/sensors/{sensor}', data = row_dict)
        r = publisher.publish(topic_path, data=str(json_data).encode())
        print(r.result())
        print(str(json_data))
        print('invio..')
        time.sleep(1)
        conta +=1

#r = publisher.publish(topic_path,b'message 1',key1='val1',key2='val2')
print(r.result())


