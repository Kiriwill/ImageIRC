FROM python:3.7.2

LABEL Author="Willian Pacheco"
LABEL Version="0.1"

RUN DISPLAY=$DISPLAY

RUN mkdir /YoloCv

WORKDIR /YoloCv

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8081

CMD ["python", "app.py"]
