# coding=utf-8
from zenvia.humansms.bean.QueryStatus import QueryStatus
from zenvia.humansms.config.mainConfig import MainConfig

class SimpleQuery(QueryStatus):
    DISTPACH_STATUS_SIMPLE = ""
    ID = ""

    def __init__(self):
        config = MainConfig()
        self.DISTPACH_STATUS_SIMPLE = config.querySimpleConfig()["dispatch"]
        self.setDispatch(self.DISTPACH_STATUS_SIMPLE)
        
    def setId(self, id):
        self.ID = id
    
    def getId(self):
        return self.ID

    def getAsArray(self):
        param = {}
        param["account"] = self.getAccount()
        param["code"] = self.getCode()
        param["dispatch"] = self.getDispatch()
        param["id"] = self.getId()
        return param