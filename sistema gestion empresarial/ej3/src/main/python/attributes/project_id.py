"""project_id attribute in project_documents"""
from attributes.attribute import Attribute

class ProjectID(Attribute):
    """project_id class"""
    def __init__(self,project_id):
        """init"""
        super().__init__()
        self._validation_pattern=r"^[a-fA-F0-9]{32}$"    #check if it is in MD5
        self._error_message= "Invalid project id"
        self._attr_value= self._validate(project_id)
