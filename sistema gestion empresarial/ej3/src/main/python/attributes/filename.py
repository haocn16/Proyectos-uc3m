"""attribute filename in project_document"""
from attributes.attribute import Attribute

class Filename(Attribute):
    """validation of filename"""
    def __init__(self,filename):
        """init"""
        super().__init__()
        #let's suppose pattern can be whatever
        self._validation_pattern=r".*"
        self._error_message="Invalid filename"
        self._attr_value=self._validate(filename)
