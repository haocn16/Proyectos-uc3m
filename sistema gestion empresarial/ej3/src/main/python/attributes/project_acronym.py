"""acronym attribute"""
from attributes.attribute import Attribute

class ProjectAcronym(Attribute):
    """Acronym class"""
    def __init__(self,acronym):
        """init"""
        super().__init__()
        self._validation_pattern = r"^[a-zA-Z0-9]{5,10}"
        self._error_message= "Invalid acronym"
        self._attr_value = self._validate(acronym)
