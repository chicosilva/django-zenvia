# coding=utf-8
from humansms.service.QueryService import QueryService

id = "001"

send = QueryService('conta.integracao', 'senha.integracao')
res = send.querySimpleStatus(id)

for msgResponse in res:
    print msgResponse.getCode() + " - " + msgResponse.getDescription()