#YoloModel, 'cfg/net_config'
from flask import Blueprint, request, render_template
from os import environ, getenv, path, curdir
from datetime import datetime as dt

from .model import YoloModel
from ..database.model import DbProcessing
from globals.resources import Resource 


yolov3 = Blueprint('yolov3',__name__, url_prefix='/model')

@yolov3.route('/ativar', methods=['POST'])
def ativar():   
    ''' Ativa YoloV3 Model '''

    start = dt.now().strftime("%m_%d_%YT%H_%M_%S")
    environ['MD_START'] = start
    
    if getenv('READ_CAM') == "1":
        environ['MODEL'] = "1"
    else:
        return Resource.bad_request(mensagem="400 bad request. Camera não ativada.")
    return Resource.ok()

@yolov3.route('/desativar', methods=['POST'])
def desativar():   
    ''' Desativa YoloV3 Model '''

    if getenv('READ_CAM') == "1" and getenv('MODEL') == "1":
        environ['MODEL'] = "0"
    else:
        if getenv('READ_CAM') != "1":
            msg = "400 bad request. Camera não ativada."
        elif getenv('MODEL') == "1":
            msg = "400 bad request. Modelo não ativado."
        
        return Resource.bad_request(mensagem=msg)

    return Resource.ok()

@yolov3.route('/consultar/<timestamp>', methods=['GET'])
def consultar(timestamp):
    ''' Consulta imagens guardadas '''

    db = DbProcessing()
    ctn = db.content
    items = list(filter(lambda d: timestamp in d.get('date'), ctn))
    
    return Resource.ok(data=items)

@yolov3.route('/images/<name>', methods=['GET'])
def consultar_imagens(name):
    ''' Consulta imagens guardadas '''

    db = DbProcessing()
    ctn = db.content
    items = list(filter(lambda d: timestamp in d.get('date'), ctn))
    
    return render_template('index.html', filename=name)
    