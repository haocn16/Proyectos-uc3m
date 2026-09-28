"""manage validation of description"""
from attributes.attribute import Attribute

class Description(Attribute):
    """description class"""
    def __init__(self,project_description):
        super().__init__()
        self._validation_pattern = r"^.{10,30}$"
        self._error_message= "Invalid description format"
        self._attr_value = self._validate(project_description)
