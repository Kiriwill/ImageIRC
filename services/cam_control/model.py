import cv2 as cv
import time
from os import getenv, environ

import threading
import datetime as dt
import numpy as np

from services.database.model import DbProcessing

class CamControl:
    ''' Serviço de execução do controle da camera 

    Args:
        model (object): modelo de rede de entrada
        model_cfg (str): arquivo de configurações para a rede
    Methods:
        thread(): inicia a Thread que executará o modelo
    ''' 
    def __init__(self, model:object = False, model_cfg:str = None):
        '''
        Args:
            model (object): modelo de rede de entrada
            model_cfg (str): arquivo de configurações para a rede
        ''' 
        cap = cv.VideoCapture(0)
        cap.set(38, 1)

        self.__model = model
        self.__model_cfg = model_cfg
        self.__cap = cap

    def __show(self, frame):
        # Executa preview da camera
        cv.imshow('frame', frame)
        cv.waitKey(1)

    def __delay(self, past:object, now:object) -> bool:
        # Define delay para salvamento
        future = (past+dt.timedelta(0,5)).strftime("%m_%d_%YT%H_%M_%S")
        if now == future:
            return True
        return False

    def __read(self):
        while True:
            # Define configurações da camera
            if getenv('SET') == "1":
                self.__cap.set(15, float(getenv('EXPOSURE') or self.__cap.get(15)))
                self.__cap.set(39, float(getenv('FOCUS') or self.__cap.get(39)))
                self.__cap.set(5, float(getenv('FPS') or self.__cap.get(5)))
                self.__cap.set(10, float(getenv('BRIGHTNESS') or self.__cap.get(10)))
                environ['SET'] = "0"

            if (self.__cap.isOpened()):
                # Define leitura da camera
                if getenv('READ_CAM') == "1":
                    check, frame = self.__cap.read()
                    now = dt.datetime.now().strftime("%m_%d_%YT%H_%M_%S")
                    
                    # Executa modelo
                    if self.__model and getenv('MODEL') == "1":
                        model = self.__model(frame, self.__model_cfg)
                        frame, boxes, labels  = model.run()

                        # Define delay de armazenamento da imagem
                        start = getenv('MD_START')
                        start = dt.datetime.strptime(start,"%m_%d_%YT%H_%M_%S")
                        if self.__delay(start, now):
                            environ['MD_START'] = now
                            path=f'mock_db/images/{now}.jpg'
                            cv.imwrite(filename=path, img=frame)

                            # Salva no Db
                            db = DbProcessing()
                            db.save(path, boxes, labels)
                    
                    # Define preview
                    if getenv('PREV') == "1":
                        self.__show(frame)
                    else:
                        cv.destroyAllWindows()
                
                elif getenv('READ_CAM') == "0":
                    self.__cap.release()
                    self.__cap.open(0)
                    cv.destroyAllWindows()

    def thread(self):
        # Inicia Thread de execução do modelo
        self.__thread = threading.Thread(target=self.__read)
        self.__thread.start()
    
if __name__ == "__main__":
    frame = cv.imread('saved_img.jpg')
    cv.imwrite(filename='cfg/image.jpg', img=frame)
