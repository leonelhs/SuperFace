import json
from abc import abstractmethod

import PIL.Image as Image
import numpy as np
import urllib3

endpoint = 'http://127.0.0.1:{0}/{1}'
port = 5000


def decodeJson(resp):
    return json.loads(resp.data.decode('utf-8'))


def decodeArray(ndarray):
    return np.uint8(ndarray)


def decodeImage(ndarray):
    ndarray = decodeArray(ndarray)
    return Image.fromarray(ndarray).convert('RGB')


def openfile(file):
    with open(file, 'rb') as fp:
        file_data = fp.read()
    return file_data


class RemoteTask:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.resource = None

    def endpoint(self):
        return endpoint.format(port, self.resource)

    def request(self, data):
        resp = self.http.request(
            'POST', self.endpoint(),
            fields={'file': ('data', data)})
        return decodeJson(resp)

    @abstractmethod
    def runRemoteTask(self, image_path):
        pass
