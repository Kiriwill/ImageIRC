from flask import Flask, g
from threading import Thread
import os

from dotenv import load_dotenv
from services.cam_control.routes import cam_ctrl
from services.yolo_model.routes import yolov3

from services.cam_control.model import CamControl
from services.yolo_model import YoloModel
from globals.resources import Resource

# Inicia aplicação
app = Flask(__name__, static_folder='mock_db/images', template_folder='mock_db/templates')
load_dotenv()

app.register_blueprint(cam_ctrl)
app.register_blueprint(yolov3)

@app.before_first_request
def thread():
    Resource(CamControl(YoloModel, 'cfg/net_config.cfg')).process()

app.run(port=8081, host='0.0.0.0', threaded=True)







