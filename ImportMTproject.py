import json
import csv
from elasticsearch import Elasticsearch

es = Elasticsearch();

# with open('./data_minimalMTprojekt.json', 'r') as filet:
#     proracun_mappings = json.loads(filet.read())
#     es.indices.create(index='proracun1', body=proracun_mappings)



def read_csv(filename, root_key='BLC_ID', as_list=False):

    with open(filename, 'r') as f:
        #print(f.read())
        reader = csv.DictReader((l.replace('\0', '') for l in f), delimiter='\t')
        print(reader)
        for row in reader:
            print(row)

    with open(filename, 'r') as f:
        c = list(csv.DictReader(f, dialect=csv.excel, delimiter='\t'))
        keys, c = c[0], c[1:]

        root_key_index = keys.index(root_key)
        if root_key_index == -1: raise

        data = {}

        for line in c:
            d = {}
            for i in range(len(keys)):
                d[keys[i]] = line[i]

            if as_list:
                if line[root_key_index] in data:
                    data[line[root_key_index]].append(d)
                else:
                    data[line[root_key_index]] = [d]
            else:
                data[line[root_key_index]] = d

        return data


TEST_FILENAME = 'C:\ElasticSearch\MT_Projekt\MT_projekt\Podatki\POSEBNI\SSP2019_POS.csv'
test = read_csv(TEST_FILENAME)


msg = "Hello World"
print(msg)