import json
import csv
from elasticsearch import Elasticsearch, helpers
from _codecs import *

es = Elasticsearch();

# with open('./data_minimalMTprojekt.json', 'r') as filet:
#     proracun_mappings = json.loads(filet.read())
#     es.indices.create(index='proracun1', body=proracun_mappings)



def read_csv(filename, root_key='BLC_ID', as_list=False):
    #filename.encode('utf-8').decode('cp1252', errors='backslashreplace')

    # with open(filename, 'r', encoding="utf-8-sig") as f:
    #     r = csv.DictReader(f)
    #     helpers.bulk(es, r, index='test_index1', doc_type='doc_type')

    with open('index.json', 'r') as f:
        es_mappings = json.loads(f.read())
        es.indices.create(index='testni_index_2', body=es_mappings)

    with open(filename, 'r', encoding="utf-8-sig") as f:
        #print(f.read())
        
        c = list(csv.DictReader(f, delimiter=';'))
        #print(c)
        for row in c:
            row['Leto'] = 2015
            row['Znesek'] = float(row['Znesek'].replace(",", "."))
            #print(row)
        helpers.bulk(es, c, index='testni_index_2')

TEST_FILENAME = 'C:\ElasticSearch\MT_Projekt\MT_projekt\Podatki\POSEBNI\leto2015.csv'
test = read_csv(TEST_FILENAME)
