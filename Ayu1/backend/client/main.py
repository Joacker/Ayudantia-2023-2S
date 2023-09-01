from flask import Flask, request, jsonify
from flask_cors import CORS
import grpc, json
from google.protobuf.json_format import MessageToJson
import examples_pb2
import examples_pb2_grpc

app = Flask(__name__)
CORS(app)

class DataClient(object):
    def __init__(self):
        
        self.host = 'server'
        self.server_port = '50051'
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))
        self.stub = examples_pb2_grpc.DataStub(self.channel)

    def GetTemperature(self):
        request = examples_pb2.Empty()
        return self.stub.GetWeatherData(request)
    
    def GetCoins(self):
        request = examples_pb2.Empty()
        return self.stub.GetCoinsData(request)


# ROUTES
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello world"})

@app.route('/temperature', methods=['GET'])
def getTemperatura():
    client = DataClient()
    response = client.GetTemperature()
    response = MessageToJson(response)
    response = json.loads(response)
    print(response)
    return jsonify(response)


@app.route('/cash', methods=['GET'])
def getCoins():
    client = DataClient()
    response = client.GetCoins()
    response = MessageToJson(response)
    response = json.loads(response)
    print(response)
    return jsonify(response)    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)