# coding=utf-8
from humansms.service.MultipleMessageService import MultipleMessageService

send = MultipleMessageService('conta.integracao', 'senha.integracao')

list = "550092167288;teste0;300\n"
list+= "550081262695;teste1;301\n"
list+= "550081337773;teste2;302\n"
list+= "550093259507;teste3;384\n"
res = send.sendMultipleListMsg(list)

for msgResponse in res:
    print msgResponse.getCode() + " - " + msgResponse.getDescription()