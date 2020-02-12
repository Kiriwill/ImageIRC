
import cv2 as cv
import numpy as np

class ImageProcessing:
    ''' 
    Serviço de processamento de imagens 

    Args:
        img (object): objeto opencv
    Methods:
        get_shape(): obtém dimensões da imagem
        resize(ratios=tuple): muda dimensões da imagem
        to_blob(size=tuple): converte imagem em dados binarios
        draw(boxes=list, box_index=list, classes=list, class_ids=list): 
            desenha sobre a imagem caixas delimitadoras obtidas
    ''' 
    def __init__(self, img:object):
        ''' 
        Serviço de processamento de imagens 

        Args:
            img (object): objeto opencv
        ''' 
        self.__img = img
    
    def get_shape(self):
        """ 
        Obtém dimensões da imagem

        Returns:
            tuple: dimensões da imagem
        """
        return self.__img.shape
        
    def resize(self, ratios:tuple = None): 
        """
        Muda dimensões da imagem

        Args:
            ratios (tuple): medidas (w,h)da razão para altura e largura
        Returns:
            object: objeto opencv com dimensões alteradas
        """
        # Define razões de dimensões da imagem
        fx = ratios[0] if ratios and isinstance(ratios, tuple) and len(ratios) == 2 else 0.5
        fy = ratios[1] if ratios and isinstance(ratios, tuple) and len(ratios) == 2 else 0.5
        
        self.__img = cv.resize(self.__img, None, fx=fx or 0.5, fy=fy)
    
    def to_blob(self, size:tuple = None):
        """
        Converte imagem em dados binarios

        Args:
            size (tuple): dimensões (w,h) da entrada do modelo
                (default=416x416)
        Returns:
            object: imagem em formato binário
        """
        
        # Define largura e altura da entrada dos dados 
        w = size[0] if isinstance(size, tuple) and len(size) == 2 else 416
        h = size[1] if isinstance(size, tuple) and len(size) == 2 else 416

        blob_img = cv.dnn.blobFromImage(self.__img, 0.00392, size=(h,w), swapRB=True)
        return blob_img

    def draw(self, boxes:list, box_index:list, classes:list, class_ids:list):
        """
        Desenha sobre a imagem caixas delimitadoras obtidas de um modelo Yolo

        Args:
            boxes (list): caixas delimitadoras minimimas (CDM) após aplicacação do threshold.
            box_index (list): indices de CDM suprimidos. Resultante de supressão não-maxima.
            classes (list): classes de objecto detectáveis.
            class_ids (list): indices de classes após aplicação do threshold.
        Returns:
            tuple: imagem alterada, CDMs e rótulos encontrados
        """
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        font = cv.FONT_HERSHEY_COMPLEX_SMALL
                   
        r_boxes = []
        labels = []
        for i in range(len(boxes)):
            if i in box_index:
                x_axis, y_axis, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]
                cv.rectangle(self.__img, (x_axis, y_axis), (x_axis + w, y_axis + h), color, 2)
                cv.putText(self.__img, label, (x_axis, y_axis-10), font, 1, color, 0)
                r_boxes.append(boxes[i])
                labels.append(label)

        img = self.__img
        return img, r_boxes, labels
