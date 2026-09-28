"""starting_date attribute"""
from datetime import datetime, timezone
from attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException



class StartingDate(Attribute):
    """starting_date class"""
    def __init__(self,date):
        """init"""
        super().__init__()
        self._validation_pattern=r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._error_message="Invalid date format"
        self._attr_value=self._validate(date)

    def _validate(self, value):
        """validation algorithm"""
        super()._validate(value)
        #rest of the logic
        try:
            my_date = datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
        return value
