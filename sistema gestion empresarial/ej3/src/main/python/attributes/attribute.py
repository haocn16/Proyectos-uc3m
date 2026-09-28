"""class to handle validations of attributes"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class Attribute():
    """Attribute class"""
    def __init__(self):
        """init class"""
        self._attr_value=""
        self._validation_pattern=""
        self._error_message=""

    def _validate(self,value):
        """general validation"""
        regex=re.compile(self._validation_pattern)
        match=regex.fullmatch(value)
        if not match:
            raise EnterpriseManagementException(self._error_message)
        return value
    @property
    def attr_value(self):
        """property"""
        return self._attr_value
    @attr_value.setter
    def attr_value(self,value):
        """setter"""
        self._attr_value=value
