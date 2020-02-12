import cv2 as cv
import numpy as np
import configparser as parser
from services.img_process import ImageProcessing

class YoloModel(ImageProcessing):
    ''' 
    Serviço de execução da rede YoloV3

    Args:
        img (object): objeto opencv
        cfg_path (str): caminho para o arquivo de configurações do modelo
    Methods:
        run(): executa modelo
        predict(img_dim=tuple, outputs=list, thold=float, nms_thold=float): 
            preve objetos na imagem a partir da saida de um modelo
    ''' 
    def __init__(self, img:object, cfg_path:str):
        '''
        Serviço de execução da rede YoloV3

        Args:
            img (object): objeto opencv
            cfg_path (str): caminho para o arquivo de configurações do modelo
        '''

        # Inicia configurações da rede
        super().__init__(img)
        cfg = parser.ConfigParser()
        cfg.read(cfg_path)
        weights = cfg['weights']['path']
        classes = cfg['classes']['path']
        path = cfg['yolo']['path']
        self.thold = float(cfg['yolo']['threshold'])
        self.nm_thold = float(cfg['yolo']['name_threshold'])
        self.ratios = eval(cfg['yolo'].get('ratios'))
        self.size = cfg['yolo'].get('size_net_input')

        # Inicia rede
        self.__net = cv.dnn.readNet(weights, path)
        self.__classes = []
        with open(classes, 'r') as names:
            self.__classes = [name.strip() for name in names.readlines()]
        self.__output = self.__net.getUnconnectedOutLayersNames()

        # Imagem objeto da análise
        self.__img = img

    def predict(self, img_dim, outputs, thold:float, nms_thold:float):
        ''' 
        Preve objetos na imagem a partir da saida de um modelo

        Args:
            img_dim (tuple): medidas da imagem (L,A)
            outputs (list): saidas do modelo
            thold (float): limite minimo de confiança para aplicar classificação
            nms_thold (float): limite minimo para aplicação da classe
        Returns:
            object: caixas delimitadoras minimas, posição após NMS, ids da classes
            Ex: [[55, 109, 164, 215]] [[0]] [0]
        '''
        
        cls_ids = []
        boxes = []
        confidences = []
        
        # Percorre objetos de saida
        for obj in outputs:
            for classes_d in obj:
                # Obtém o indice e confiança do valor mais alto
                scores = classes_d[5:]
                class_id = np.argmax(scores) 
                confidence = scores[class_id]
                
                # Verifica a confiança
                if confidence > thold:
                    center_x = int(classes_d[0] * img_dim[0])
                    center_y = int(classes_d[1] * img_dim[1])

                    # Define caixa delimitadora minima
                    w = int(classes_d[2] * img_dim[0])
                    h = int(classes_d[3] * img_dim[1])
                    left = int(center_x - w / 2)
                    top = int(center_y - h / 2)

                    # Armazena resultados
                    cls_ids.append(class_id)
                    boxes.append([left, top, w, h])
                    confidences.append(float(confidence))

        # Aplica 'non-max suppression'
        b_indices = cv.dnn.NMSBoxes(boxes, confidences, thold, nms_thold)

        return boxes, b_indices, cls_ids

    def run(self):
        ''' 
        Executa modelo
        Returns:
            tuple: previsões, caixas delimitadoras minimas, nome da classe encontra
        '''
        
        # Executa tratamento da imagem
        super().resize(self.ratios)
        img_dim = super().get_shape()[:2]
        b_img = super().to_blob(self.size)
        
        # Executa rede
        self.__net.setInput(b_img)
        outs = self.__net.forward(self.__output)

        # Obtém previsões
        boxes, b_indices, cls_ids = self.predict(img_dim, outs, self.thold, self.nm_thold)
        prediction, r_boxes, labels = super().draw(boxes, b_indices, self.__classes, cls_ids)
        
        return prediction, r_boxes, labels