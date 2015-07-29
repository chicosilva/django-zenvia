# coding=utf-8
from humansms.service.SimpleMessageService import SimpleMessageService

id = ""

send = SimpleMessageService('conta.integracao', 'senha.integracao')
res = send.cancelSMS(id)

for msgResponse in res:
    print msgResponse.getCode() + " - " + msgResponse.getDescription()
    