from enum import Enum
import json
import socket
from tkinter import N


class ResponseType(Enum):
    OK = 0
    BAD = 1


class Response:
    def __init__(self, data: bytes):

        self.type: ResponseType = None
        self.data: dict = None
        self.message: str = None

        data_string = data.decode("utf-8")
        json_data = json.loads(data_string)

        if json_data['Status'] == 0:
            self.type = ResponseType.OK
        else:
            self.type = ResponseType.BAD

        self.data = json_data['Data']
        self.message = json_data['Message']

    @staticmethod
    def timeout_response():
        return Response(b'{"Status": "BAD", "Message":"Could not connect to server", "Data":{}}')


class RequestType(Enum):
    ACCESS = 0
    TRANSFER = 1
    LOGOUT = 2


class Request:
    def __init__(self, type: RequestType, id: str, station: str):
        self.type = type.value
        self.id = id
        self.station = station

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class TCPClient:
    def __init__(self, host_ip: str, port: int, station: str) -> None:
        self.host_ip = host_ip
        self.port = port
        self.station = station

    def send_access(self, id: str) -> Response:
        response = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host_ip, self.port))
            s.settimeout(5)
            request = Request(RequestType.ACCESS, id, self.station)
            req_json = request.toJSON()

            s.sendall(bytes(req_json, "ASCII"))

            data = s.recv(1024)
            response = Response(data)
        except:
            response = Response.timeout_response()
        finally:
            s.close()

        return response

    def send_transfer(self, id: str) -> Response:
        response = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host_ip, self.port))
            s.settimeout(5)
            request = Request(RequestType.TRANSFER, id, self.station)
            req_json = request.toJSON()

            s.sendall(bytes(req_json, "ASCII"))

            data = s.recv(1024)
            response = Response(data)
        except:
            response = Response.timeout_response()
        finally:
            s.close()

        return response

    def send_logout(self, id: str) -> Response:
        response = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host_ip, self.port))
            s.settimeout(5)
            request = Request(RequestType.LOGOUT, id, self.station)
            req_json = request.toJSON()

            s.sendall(bytes(req_json, "ASCII"))

            data = s.recv(1024)
            response = Response(data)
        except:
            response = Response.timeout_response()
        finally:
            s.close()

        return response
