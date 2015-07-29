# coding=utf-8
from humansms.service.QueryService import QueryService
 
msg_list = {"001","002","003","004","005","006","007","008","009","010"}

send = QueryService('conta.integracao', 'senha.integracao')
res = send.queryMultipleStatus(msg_list)

for msgResponse in res:
    print msgResponse.getCode() + " - " + msgResponse.getDescription()
