from flask import Flask, json, Response, jsonify, request

def getStatusCheck(request):
    client_ip = request.remote_addr
    message ={
        'status':"Working " + client_ip,
        'reponse_code':'200',
    }
    responsemessage = jsonify(message)
    responsemessage.status_code= 200
    return jsonify(message),200