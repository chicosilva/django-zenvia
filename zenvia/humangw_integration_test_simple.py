# coding=utf-8
from zenvia.humansms.service.SimpleMessageService import SimpleMessageService

send = SimpleMessageService('conta.integracao', 'senha.integracao')

msg = "teste"
fromPar = "550093259507"
to = "550081458552"
id = "333"
schedule = "29/05/2011 18:00:00"

res = send.sendSimpleMsg(msg, to, fromPar, id, schedule)
for msgResponse in res:
    print msgResponse.getCode() + " - " + msgResponse.getDescription()
