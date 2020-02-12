from uuid import uuid4
import json
import os

class DbProcessing:
    ''' Serviço mock para controle de banco de dados

    Methods:
        save(path=str, boxes=list, labels=list): salva os resultados do modelo 
    ''' 

    def __init__(self):
        items = open('mock_db/items/items.json', 'r+')
        self.content = json.load(items)

    def save(self, path:str, boxes:list, labels:list):
        """salva os resultados de um modelo (Mock)

        Args:
            path (str): caminho para o arquivo final
            boxes (list): caixas delimitadoras minimas
            labels (list): rótulos das classes encontradas

        Returns:
            None
        """

        data = {}
        img = path.split('/')[2]
        data.update(classes=[{"nome": label, "coordenadas":boxes[i]} for i, label in enumerate(labels)])
        data.update(date=img.strip('.jpg'))
        data.update(url=f'http://localhost:8081/model/images/{img}')
        data.update(id=str(uuid4()))

        self.content.append(data)
        data = json.dumps(self.content)
        with open('mock_db/items/items.json', 'w') as f:
            f.write(data)



