# coding=utf-8
from zenvia.humansms.bean.SimpleMessage import SimpleMessage
from zenvia.humansms.config.mainConfig import MainConfig
from zenvia.humansms.service.base.HumanBaseService import HumanBaseService
from zenvia.humansms.util.HumanConnectionHelper import HumanConnectionHelper

# Classe de envio multiplo, classe filha de HumanBaseService
# responsavel por montar a requisição 
class SimpleMessageService(HumanBaseService):
    # Tipos de Layout de mensagem, consultar o manual

    response = HumanConnectionHelper()
    config = MainConfig()    
    
    def __init__(self, accountPar, codePar):
        # Construtor que seta na classe pai HumanBaseService a conta e o código de acesso
        HumanBaseService.__init__(self, accountPar, codePar)

    def sendSimpleMsg(self, msg_txt, to, fromPar="", id="", schedule="", callback=0):
        msg = SimpleMessage()
        msg.setAccount(self.getAccount())
        msg.setCode(self.getCode())
        msg.setMessage("%s" % msg_txt)
        msg.setFrom(fromPar)
        msg.setMobile(to)
        msg.setId(id)
        msg.setCallBack(callback)
        msg.setSchedule(schedule)
        
        return self.response.getResponse(self.sendSimple(msg))
    
    def cancelSMS(self, id):
        msg = SimpleMessage()
        msg.setAccount(self.getAccount())
        msg.setCode(self.getCode())
        msg.setDispatch(self.config.cancelConfig()["dispatch"])
        msg.setId(id)
        return self.response.getResponse(self.cancelSimple(msg));        
        
        