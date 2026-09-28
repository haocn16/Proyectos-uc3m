"""department class"""
from attributes.attribute import Attribute

class Department(Attribute):
    """manage validation of department"""
    def __init__(self,department):
        """init"""
        super().__init__()
        self._validation_pattern=r"(HR|FINANCE|LEGAL|LOGISTICS)"
        self._error_message="Invalid department"
        self._attr_value=self._validate(department)
