from flask import Blueprint, request
from os import environ, getenv
import threading

from .model import CamControl
from globals.resources import Resource 

cam_ctrl = Blueprint('cam_controller',__name__, url_prefix='/webcam')

@cam_ctrl.route('/ativar', methods=['POST'])
def ativar():
    ''' Ativa camera '''
    try:
        if request.json:
            cfg = request.json
            environ['PREV'] = cfg.get('preview') or ''

        environ['READ_CAM'] = "1"
        return Resource.ok()

    except Exception as e:
        return Resource.internal_error(
            mensagem=f"500 Internal Server Error. Nao foi possível ativar o serviço. {e}")

@cam_ctrl.route('/desativar', methods=['POST'])
def desativar():
    ''' Desativa camera '''
    try:
        if getenv('READ_CAM') == "0":
            return Resource.ok(mensagem="Camera já está desativada.")
        
        environ['READ_CAM'] = "0"
        return Resource.ok()
    except Exception as e:
        return Resource.internal_error(
            mensagem=f"500 Internal Server Error. Nao foi possível ativar o serviço. {e}")

@cam_ctrl.route('/config', methods=['POST'])
def config():   
    ''' Configura camera '''
    try:
        if request.json:
            
            cfg = request.json
            if cfg.get('preview'):
                environ['PREV'] = cfg.get('preview') or ''
            elif cfg.get('exposicao'):
                environ['EXPOSURE'] = cfg.get('exposicao')
            elif cfg.get('foco'):
                environ['FOCUS'] = cfg.get('foco')
            elif cfg.get('fps'):
                environ['FPS'] = cfg.get('fps')
            elif cfg.get('brilho'):
                environ['BRIGHT'] = cfg.get('brilho')

        return Resource.ok()
    except Exception as e:
        return Resource.internal_error(
            mensagem=f"500 Internal Server Error. Nao foi possível ativar o serviço. {e}")
