import json
import csv
from elasticsearch import Elasticsearch, helpers
from _codecs import *
from pathlib import Path
from datetime import datetime

es = Elasticsearch();

# with open('./data_minimalMTprojekt.json', 'r') as filet:
#     proracun_mappings = json.loads(filet.read())
#     es.indices.create(index='proracun1', body=proracun_mappings)

elastic_id = 1

def read_csv(filename, root_key='BLC_ID', as_list=False):
    temp = es.indices.exists(index="posebni1")
    if temp is False:
        with open('indexPodatkov.json', 'r') as f:
            es_mappings = json.loads(f.read())
            es.indices.create(index='posebni1', body=es_mappings)

    leto, number = str(Path(filename).stem).split("_")
    global elastic_id
    with open(filename, 'r', encoding="utf-8-sig") as f:
            #print(f.read())
            
            c = list(csv.DictReader(f, delimiter=';'))
            for row in c:
                #row['Leto'] = int(number)

                row['Leto'] = datetime.strptime(number, '%Y').year
                row['Znesek'] = float(row['Znesek'].replace(",", "."))
                row['NADSKUPINA_ID'] = int(row['NADSKUPINA_ID'])
                row['SPU_ID'] = int(row['SPU_ID'])
                row['PU_ID'] = int(row['PU_ID'])
                row['POL_ID'] = int(row['POL_ID'])
                row['PRG_ID'] = int(row['PRG_ID'])
                row['POD_ID'] = int(row['POD_ID'])

                row['_index'] = "posebni1"
                row['_type'] = "_doc"
                row['_id'] = int(elastic_id)
                elastic_id+=1

                #print(row)
                actions.append(row)
            # helpers.bulk(es, c, index='test_index3')
    print("KONEC branja " + number)


actions = []

#primer iskanja : http://localhost:9200/test_index3/_search?pretty=true&q=PU_ID:1213
#http://localhost:9200/posebni/_search?pretty=true&q=Leto:2019

    # with open('index.json', 'r') as f:
    #     es_mappings = json.loads(f.read())
    #     es.indices.create(index='testni_index_2', body=es_mappings)

    # with open(filename, 'r', encoding="utf-8-sig") as f:
    #     #print(f.read())
        
    #     c = list(csv.DictReader(f, delimiter=';'))
    #     #print(c)
    #     for row in c:
    #         row['Leto'] = 2015
    #         row['Znesek'] = float(row['Znesek'].replace(",", "."))
    #         #print(row)
    #     helpers.bulk(es, c, index='testni_index_2')

TEST_FILENAME1 = 'F:\desktop\FAX 3\MT\MT_projekt\Podatki\POSEBNI\leto_2015.csv'
read_csv(TEST_FILENAME1)
TEST_FILENAME2 = 'F:\desktop\FAX 3\MT\MT_projekt\Podatki\POSEBNI\leto_2016.csv'
read_csv(TEST_FILENAME2)
TEST_FILENAME3 = 'F:\desktop\FAX 3\MT\MT_projekt\Podatki\POSEBNI\leto_2017.csv'
read_csv(TEST_FILENAME3)
TEST_FILENAME4 = 'F:\desktop\FAX 3\MT\MT_projekt\Podatki\POSEBNI\leto_2018.csv'
read_csv(TEST_FILENAME4)
TEST_FILENAME5 = 'F:\desktop\FAX 3\MT\MT_projekt\Podatki\POSEBNI\leto_2019.csv'
read_csv(TEST_FILENAME5)

# for row in actions:
#     print(row)

helpers.bulk(es, actions, index='posebni1')


#OLD
# def read_csv(filename, root_key='BLC_ID', as_list=False):
#     #filename.encode('utf-8').decode('cp1252', errors='backslashreplace')

#     # with open(filename, 'r', encoding="utf-8-sig") as f:
#     #     r = csv.DictReader(f)
#     #     helpers.bulk(es, r, index='test_index1', doc_type='doc_type')

#     with open('index.json', 'r') as f:
#         es_mappings = json.loads(f.read())
#         es.indices.create(index='testni_index_2', body=es_mappings)

#     with open(filename, 'r', encoding="utf-8-sig") as f:
#         #print(f.read())
        
#         c = list(csv.DictReader(f, delimiter=';'))
#         #print(c)
#         for row in c:
#             row['Leto'] = 2015
#             row['Znesek'] = float(row['Znesek'].replace(",", "."))
#             #print(row)
#         helpers.bulk(es, c, index='testni_index_2')

# TEST_FILENAME = 'C:\ElasticSearch\MT_Projekt\MT_projekt\Podatki\POSEBNI\leto2015.csv'
# test = read_csv(TEST_FILENAME)