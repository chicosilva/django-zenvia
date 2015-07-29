# coding=utf-8
from humansms.service.QueryService import QueryService

send = QueryService('conta.integracao', 'senha.integracao')
res = send.listReceivedSMS()

for msgResponse in res:
    print msgResponse.getCode() + " - " + msgResponse.getDescription()