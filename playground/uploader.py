import numpy as np
import urllib3
import json

file_path = "/home/leonel/goyo00.jpeg"

with open(file_path, 'rb') as fp:
    file_data = fp.read()

http = urllib3.PoolManager()

resp = http.request(
    'POST',
    'http://127.0.0.1:5000/segment',
    fields={
        'file': ('tosegment', file_data),
    })


resp = json.loads(resp.data.decodeJson('utf-8'))
mask = np.array(resp)

print(mask.shape)
