# -*- coding: utf-8 -*-
import os
import time
import logging
from concurrent import futures

from google.protobuf import json_format
import grpc

from api import api_pb2_grpc, api_pb2


DEFAULT_GRPC_PORT = '[::]:50051'

GRPC_PORT = os.getenv('GRPC_PORT', DEFAULT_GRPC_PORT)

parsers = {
    api_pb2.EN: None,
    api_pb2.ES: None,
    api_pb2.DE: None,
    api_pb2.FR: None,
    api_pb2.IT: None,
    api_pb2.NL: None
}

langCode = {
    api_pb2.EN: 'en',
    api_pb2.ES: 'es',
    api_pb2.DE: 'de',
    api_pb2.FR: 'fr',
    api_pb2.IT: 'it',
    api_pb2.NL: 'nl'
}


def getParser(lang):
    """
    Layz-load parsetree if available
    """
    if parsers[lang] is None:
        # Dynamic load
        logging.debug('Loading parsetree for %s...' % langCode[lang])
        parsers[lang] = __import__('pattern.' + langCode[lang], None, None,
                                   langCode[lang])
        logging.debug('loaded!')
    return parsers[lang].parsetree


class APIServicer(api_pb2_grpc.APIServicer):

    def parse(self, request, context):
        """
        Get the parsed tree of sentences
        """
        rl = request.language
        if rl != api_pb2.EN and rl != api_pb2.ES and rl != api_pb2.DE and \
                rl != api_pb2.FR and rl != api_pb2.IT and rl != api_pb2.NL:
            return api_pb2.ParseResponse(
                isOk=False,
                reason='Requested language is not implemented')
        parsetree = getParser(request.language)
        tree = parsetree(request.text, relations=True, lemmata=True)
        data = {'isOk': True, 'reason': None, 'sentences': []}
        for sentence in tree:
            words = []
            for word in sentence.words:
                words.append({'type': word.type, 'text': word.string})
            chunks = []
            for chunk in sentence.chunks:
                words = [{'text': w.string, 'type': w.type}
                         for w in chunk.words]
                chunk = {'type': chunk.type, 'words': words}
                chunks.append(chunk)
            data['sentences'].append({'words': words, 'chunks': chunks})
        ret = json_format.ParseDict(data, api_pb2.ParseResponse())
        return ret


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_APIServicer_to_server(APIServicer(), server)
    server.add_insecure_port(GRPC_PORT)
    logging.debug('Starting gRPC-Pattern service in %s...' % GRPC_PORT)
    server.start()
    while True:
        time.sleep(100)
