# HTTP YoloV3 Object Recognizer - HTTPYOR
-------------------------------------------------------

>> A aplica��o consiste na identifica��o de objetos a partir da aplica��o de uma rede neural do tipo YoloV3 e de imagens de webcam. A rede e a c�mera s�o controladas por requests HTTP.

## Instala��o

Use [pip](https://pip.pypa.io/en/stable/) para instalar as dependencias e rodar a aplica��o:

```bash
pip install -r requirements.txt
python app.py
```

ou utilize o Docker (� preciso configurar o xhost para dar acesso a camera):

```bash
sudo docker build -t yolov3cv .
sudo docker run --privileged --device=/dev/video0:/dev/video0 -p 8081:8081 yolov3cv
```

## Configura��o
As configura��es da rede est�o contidas na pasta cfg. O arquivo yolov3.cfg cont�m os parametros para o funcionamento da rede e o arquivo net_config.cfg os parametros para as configura��es o tratamento das imagens de entrada e dos resultados da rede. Alguns deles:

threshold: Limite de confian�a para atribuir uma classe a uma previs�o.
size_net_input: dimens�es da entrada do arquivo blob (deve ser multiplo de 32)
ratios: raz�o das dimens�es da imagem (para redimensionamento)

## Uso

H� dois tipos de servi�os dispon�veis: webcam e modelo. Ambos s�o controlados por seus respectivos endpoints.
As imagens do modelo s�o armazenadas na pasta mock_db/images com o timestamp como nome. O delay para grava��o � de 5seg.
Os exemplos a seguir s�o para uso local.

### Camera

#### Ativa��o
Endpoint: http://0.0.0.0:8081/webcam/ativar
Method: POST
Content-Type: application/json ou ausente
Body: ausente ou {
    "preview": str: 1 ou 0
}

Response:
    200: {
            "message": "200 OK",
            "success": true
        }

#### Desativa��o
Endpoint: http://0.0.0.0:8081/webcam/desativar
Method: POST
Content-Type: N�o aplic�vel
Body: N�o aplic�vel
Response:
    200: {
            "message": "200 OK",
            "success": true
        }

#### Configura��o
Endpoint: http://0.0.0.0:8081/webcam/config
Method: POST
Content-Type: application/json
Body: {
    "preview": str: 1 ou 0,
    "exposicao": str,
    "foco": str,
    "fps": str,
    "brilho": str
} 

Response:
    200: {
            "message": "200 OK",
            "success": true
        }

### Modelo

#### Ativa��o
Endpoint: http://0.0.0.0:8081/model/ativar
Method: POST
Content-Type: N�o aplic�vel
Body: N�o aplic�vel
Response:
    200: {
            "message": "200 OK",
            "success": true
        }

#### Desativa��o
Endpoint: http://0.0.0.0:8081/model/desativar
Method: POST
Content-Type: N�o aplic�vel
Body: N�o aplic�vel
Response:
    200: {
            "message": "200 OK",
            "success": true
        }

#### Consultar
Endpoint: http://0.0.0.0:8081/model/consultar/{{timestamp}}
    Timetamp no formato "%m_%d_%YT%H_%M_%S"
    
    Exemplos:
        Tempo exato: http://0.0.0.0:8081/model/consultar/12_10_1989T14_40_34
        Por dia: http://0.0.0.0:8081/model/consultar/06-10
        Por ano: http://0.0.0.0:8081/model/consultar/2020 

Method: GET
Content-Type: N�o aplic�vel
Body: N�o aplic�vel
Response:
    200: {
            "data": [{
                "classes": [
                    {
                    "coordenadas": [
                        53,
                        133,
                        169,
                        188
                    ],
                    "nome": "person"
                    }
                ],
                "date": "02-02-2020T19:23:11",
                "id": "437a6709-32cd-4d17-837e-6c209b019862",
                "url": "http://localhost:8081/model/images/12_10_1989T14_40_34.jpg"
                },
                {
                "classes": [
                    {
                    "coordenadas": [
                        51,
                        131,
                        169,
                        188
                    ],
                    "nome": "person"
                    }
                ],
                "date": "02-02-2020T19:23:16",
                "id": "a350f0dd-69f1-46f2-98d2-dfb50e4a89c0",
                "url": "http://localhost:8081/model/images/12_10_1989T14_40_34.jpg"
            }]
            "message": "200 OK",
            "success": true
        }
