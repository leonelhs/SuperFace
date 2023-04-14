from PySide6 import QtNetwork
from PySide6.QtNetwork import QNetworkRequest, QHttpMultiPart


def makeMultipart(data):
    multiPart = QtNetwork.QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)
    file_data = QtNetwork.QHttpPart()
    file_data.setHeader(QNetworkRequest.ContentDispositionHeader, 'form-data; name="file"; filename="data"')
    file_data.setHeader(QNetworkRequest.ContentTypeHeader, 'application/octet-stream')
    file_data.setBody(data)
    multiPart.append(file_data)
    return multiPart
