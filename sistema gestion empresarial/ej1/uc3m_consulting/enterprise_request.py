'''Module that store the class enterprise request.'''
import json
from datetime import datetime


class EnterpriseRequest:
    '''Useful data class to store the enterprise information'''
    def __init__(self, cif, phone, ename):
        self.__enterprise_name = ename
        self.__cif = cif
        self.__phone = phone
        justnow = datetime.utcnow()
        self._time_stamp = datetime.timestamp(justnow)

    def __str__(self):
        return "Enterprise:" + json.dumps(self.__dict__)

    @property
    def enterprise_cif(self):
        '''Define the enterprise CIF'''
        return self.__cif
    @enterprise_cif.setter
    def enterprise_cif(self, value):
        self.__cif = value

    @property
    def phone_number(self):
        '''Define the enterprise phone number'''
        return self.__phone
    @phone_number.setter
    def phone_number(self, value):
        self.__phone = value

    @property
    def enterprise_name(self):
        ''' Define the enterprise name'''
        return self.__enterprise_name
    @enterprise_name.setter
    def enterprise_name(self, value):
        self.__enterprise_name = value
