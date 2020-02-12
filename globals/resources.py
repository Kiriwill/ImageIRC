import logging as logger    
from flask import jsonify

class Resource():
    def __init__(self, service):
        self.__logger = logger
        self.__service = service

    def process(self, **args):
        try:
            service = self.__service.thread()
    
            return service.ok()
        except Exception as e:
            return e

    @staticmethod
    def ok(data = {}, mensagem="200 OK"):
        """Retorna um response 200 OK."""
        return Resource.response(True, data, mensagem, 200)

    @staticmethod
    def not_found(data = {}, mensagem="404 Not Found"):
        """Retorna um response 200 OK."""
        return Resource.response(False, data, mensagem, 200)

    @staticmethod
    def bad_request(data = {}, mensagem="400 Bad Request"):
        """Retorna um response 400 Bad Request."""
        return Resource.response(False, data, mensagem, 400)

    @staticmethod
    def internal_error(data = {}, mensagem="500 Internal Server Error"):
        """Retorna um response 500 Internal Server Error"""
        return Resource.response(False, data, mensagem, 500)

    @staticmethod
    def response(sucesso, data, msg, codigo):
        """Retorna um :class:`~flask.Flask.response_class`"""
        if data:
            return jsonify({
                'success': sucesso,
                'message': msg,
                'data': data
            }), codigo
        
        return jsonify({
                'success': sucesso,
                'message': msg,
            }), codigo
        