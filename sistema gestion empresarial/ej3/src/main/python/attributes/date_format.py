"""attribute date_format to check date_format in find_docs"""
import re
from datetime import datetime
from attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class DateFormat(Attribute):
    """child class"""
    def __init__(self,date_str:str):
        """Init"""
        super().__init__()
        self._validation_pattern= r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._error_message="Invalid date format"
        self._attr_value=self._validate(date_str)

    def _validate(self, value):
        """validation algorithm"""
        date_pattern = re.compile(self._validation_pattern)
        result_pattern = date_pattern.fullmatch(value)
        if not result_pattern:
            raise EnterpriseManagementException("Invalid date format")
        try:
            datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex
        return value
