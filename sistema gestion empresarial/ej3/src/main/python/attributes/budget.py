"""Budget attribute class"""
from attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class Budget(Attribute):
    """management of budget"""
    def __init__(self,project_budget):
        """init class"""
        super().__init__()
        self._validation_pattern=r".*"
        self._error_message="Invalid budget amount"
        self._attr_value=self._validate(project_budget)

    def _validate(self, value):
        """validation algorithm"""
        try:
            budget_float = float(value)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc
        budget_string = str(budget_float)
        if '.' in budget_string:
            decimales = len(budget_string.split('.')[1])
            if decimales > 2:
                raise EnterpriseManagementException("Invalid budget amount")
        if budget_float < 50000 or budget_float > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")
        return budget_float
