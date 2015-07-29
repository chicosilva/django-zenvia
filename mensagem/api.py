# -*- coding: utf-8 -*-
import datetime
from financeiro.models import Credito, saldo_positivo
from keepconfig.models import KeepConfig
from zenvia.humansms.service.SimpleMessageService import SimpleMessageService
from zenvia.humansms.service.QueryService import QueryService
import socket
import requests
from random import randint
import json

if socket.gethostname() == 'chicosilva':
    URL_CLIENTE = ''
else:
    from keepsms.config.production_settings import URL_CLIENTE

CONTA_CORP = 'francisco.corp'
SENHA_CORP = 'CIfzyeLpY8'

CONTA_ENGAGE = 'engage.francisco'
SENHA_ENGAGE = '3cCAtaRHGo'

CODIGO_SALDO_NEGATIVO = "5000"

def consulta():

    send = QueryService(CONTA_ENGAGE, SENHA_ENGAGE)
    res = send.querySimpleStatus(44)

    for msgResponse in res:
        msgResponse.getCode(), msgResponse.getDescription()

def enviar_sms_api(mensagem):

    from autenticacao.models import Configuracao
    configuracao = Configuracao.objects.all().first()
    config_app   = KeepConfig.objects.all().first()

    send = SimpleMessageService(CONTA_CORP, SENHA_CORP)
    sair, link_confirmacao = '', ''

    if mensagem.enviar_link and mensagem.tipo.pk == 1:
        link_confirmacao = '%s/d/?i=%s' % (URL_CLIENTE, mensagem.pk)

    if int(mensagem.tipo_id) == 2:

        sair = 'P/ sair responda: nao'
        send = SimpleMessageService(CONTA_ENGAGE, SENHA_ENGAGE)

    if not saldo_positivo():
        atualiza_status(mensagem, CODIGO_SALDO_NEGATIVO, '')
        return False

    schedule = ''
    if mensagem.data_agendamento:
        schedule = mensagem.data_agendamento.strftime('%d/%m/%Y %H:%I:%S')

    assinatura = configuracao.assinatura_sms

    if not configuracao.assinatura_sms:
        assinatura = configuracao.nome

    texto = "%s - %s. %s %s" % (mensagem.texto, assinatura, sair, link_confirmacao)

    mensagem_id = "%sA%s" % (config_app.codigo_cliente, mensagem.pk)

    res = send.sendSimpleMsg(texto, u"55%s" % mensagem.usuario.celular, '', mensagem_id, schedule, callback=2)

    for msgResponse in res:
        atualiza_status(mensagem, msgResponse.getCode(), msgResponse.getDescription())

def efetua_cobranca(mensagem):

    if mensagem.status.tarifar and mensagem.status.codigo != CODIGO_SALDO_NEGATIVO:

        credito     = Credito.objects.all().first()
        config_app  = KeepConfig.objects.all().first()

        if credito.valor > 0 and not mensagem.valor:

            credito.valor = credito.valor - config_app.valor_sms

            if credito.valor < 0:
                credito.valor = 0

            credito.save()

        mensagem.valor = config_app.valor_sms
        mensagem.save()

def atualiza_status(mensagem, codigo, status_text=""):

        from mensagem.models import StatusMensagem

        if codigo == "000" or codigo == "00":
            codigo = "800"

        status = StatusMensagem.objects.get(codigo=codigo)

        mensagem.status = status
        if status_text:
            mensagem.status_text = status_text

        mensagem.save()

        if codigo == "13":
            mensagem.usuario.numero_invalido = True
            mensagem.usuario.save()

        efetua_cobranca(mensagem)

def cancelar_agendamento_api(mensagem):

    if not mensagem.data_agendamento: return False

    mensagem.data_cancelamento = datetime.datetime.now()
    mensagem.save()

    send = SimpleMessageService(CONTA_CORP, SENHA_CORP)

    if int(mensagem.tipo_id) == 2:
        send = SimpleMessageService(CONTA_ENGAGE, SENHA_ENGAGE)

    config_app  = KeepConfig.objects.all().first()
    mensagem_id = "%sA%s" % (config_app.codigo_cliente, mensagem.pk)

    res = send.cancelSMS(mensagem_id)

    for msgResponse in res:
        atualiza_status(mensagem, msgResponse.getCode(), msgResponse.getDescription())

def consulta_status_detalhado(mensagem):

    conta = CONTA_ENGAGE
    senha = SENHA_ENGAGE

    config_app  = KeepConfig.objects.all().first()
    mensagem_id = '111A8'

    payload = {'dispatch': 'check',}
    h = {'Accept': 'application/json'}
    response = requests.get('https://api-rest.zenvia360.com.br/services/get-sms-status/%s' % mensagem_id, auth=(conta, senha), headers=h, params=payload)
    print response.json()

    return response.json()

    try:

        conta = CONTA_CORP
        senha = SENHA_CORP

        if mensagem.tipo.pk == 2:

            conta = CONTA_ENGAGE
            senha = SENHA_ENGAGE

        config_app  = KeepConfig.objects.all().first()
        mensagem_id = "%sA%s" % (config_app.codigo_cliente, mensagem.pk)

        payload = {}
        h = {'Accept': 'application/json'}

        response = requests.post('https://api-rest.zenvia360.com.br/services/get-sms-status/%s' % mensagem_id, auth=(conta, senha), headers=h, params=payload)

        print response.json()

    except:
        return False

DADOS = {
    "receivedResponse": {
        "statusCode": "00",
        "statusDescription": "Ok",
        "detailCode": "300",
        "detailDescription": "Received messages found",
        "receivedMessages": [{
                                 "id": 23190501,
                                 "dateReceived": "2014-08-22T14:49:36",
                                 "mobile": "553491073655",
                                 "body": "nao",
                                 "shortcode": "30133",
                                 "mobileOperatorName": "Claro",
                                 "mtId": "hs863223748"
                             }]
    }
}

def consulta_sms_marketing_recebidos():

    from cadastro.models import Usuario
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.post('https://api-rest.zenvia360.com.br/services/received/list', auth=(CONTA_ENGAGE, SENHA_ENGAGE), headers=headers)

    result = response.json()

    detalhes = result['receivedResponse']

    if detalhes['detailCode'] == "300":

        for mensagem in detalhes['receivedMessages']:

            resposta = mensagem['body'].lower()

            if resposta == 'nao':

                try:
                    usuario = Usuario.objects.get(celular=mensagem['mobile'][2:])
                    usuario.notificacoes = False
                    usuario.save()
                except:
                    pass

    return response.json()

def consulta_sms(mensagem):

    if mensagem.status.codigo == CODIGO_SALDO_NEGATIVO:
            return False

    l = [3, 23, 37, 9, 11, 13, 17, 24, 25, 29, 30, 31, 32,33, 37, 34]
    if mensagem.status.pk in l:
        return False

    send = QueryService(CONTA_CORP, SENHA_CORP)

    if mensagem.tipo.pk == 2:
        send = QueryService(CONTA_ENGAGE, SENHA_ENGAGE)

    config_app  = KeepConfig.objects.all().first()
    mensagem_id = "%sA%s" % (config_app.codigo_cliente, mensagem.pk)

    res = send.querySimpleStatus(mensagem_id)

    for msgResponse in res:
        atualiza_status(mensagem, msgResponse.getCode(), msgResponse.getDescription())

    return False

def enviar_sms_teste(texto):

    from autenticacao.models import Configuracao
    configuracao = Configuracao.objects.all().first()

    send = SimpleMessageService(CONTA_ENGAGE, SENHA_ENGAGE)

    schedule = ''

    assinatura = configuracao.assinatura_sms

    if not configuracao.assinatura_sms:
        assinatura = configuracao.nome

    texto = "%s - %s." % (texto, assinatura)

    id = randint(5,20000)

    from cadastro.models import celular_to_int

    res = send.sendSimpleMsg(texto, u"55%s" % celular_to_int(configuracao.celular), '', 't%s' % id, schedule, callback=2)

    for msgResponse in res:
        return msgResponse.getCode()

def enviar_denuncia(noticia_id):

    from autenticacao.models import Configuracao
    configuracao = Configuracao.objects.all().first()

    send = SimpleMessageService(CONTA_ENGAGE, SENHA_ENGAGE)

    schedule = ''

    assinatura = configuracao.assinatura_sms

    if not configuracao.assinatura_sms: assinatura = configuracao.nome

    texto = u"Denúncia de Abuso: Notícia id: %s - %s." % (noticia_id, assinatura)

    id = randint(5,20000)

    celular = '3491073655'
    res = send.sendSimpleMsg(texto, u"55%s" % celular, '', 't%s' % id, schedule, callback=2)

    for msgResponse in res:
        return msgResponse.getCode()