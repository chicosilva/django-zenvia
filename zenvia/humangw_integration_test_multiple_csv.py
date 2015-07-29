# coding=utf-8
from humansms.service.MultipleMessageService import MultipleMessageService

send = MultipleMessageService('conta.integracao', 'senha.integracao')

res = send.sendMultipleFileCSV("C:\Users\teste\Desktop\arquivo.csv")

for msgResponse in res:
    print msgResponse.getCode() + " - " + msgResponse.getDescription()