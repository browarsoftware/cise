import json
from pathlib import Path
file_name = 'd:/data/credo/json_100-199/export_1679574802409_1679649447803.json'

"""
file_path = Path(file_name)
file_content = file_path.read_text()
y = json.loads(file_name)
"""
def append_one_file(file_name, all_data_dic):
    with open(file_name, 'r') as j:
        contents = json.loads(j.read())
        lista = contents['detections']
        for l in lista:
            all_data_dic[l['id']] = {'lat':l['latitude'], 'lon':l['longitude']}
            #print(str(l['id']) + "," + str(l['latitude']) + "," + str(l["longitude"]))
            #print(all_data_dic[l['id']])

import glob
all_files = glob.glob("d:/data/credo/json-0.99/*.json")
all_files += glob.glob("d:/data/credo/json_100-199/*.json")
all_data_dic = {}

for l in all_files:
    append_one_file(l, all_data_dic)

import pickle
with open('data/all_data_dic.pickle', 'wb') as handle:
    pickle.dump(all_data_dic, handle, protocol=pickle.HIGHEST_PROTOCOL)