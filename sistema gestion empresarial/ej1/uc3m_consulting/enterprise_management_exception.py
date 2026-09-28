"""Module defining the exceptions for the enterprise management system"""

class EnterpriseManagementException(Exception):
    """Exception class to handle specific errors"""
    def __init__(self, message):
        """Initialize the exception with a specific error message"""
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        """Gets the exception message"""
        return self.__message

    @message.setter
    def message(self,value):
        """Sets the exception message"""
        self.__message = value
