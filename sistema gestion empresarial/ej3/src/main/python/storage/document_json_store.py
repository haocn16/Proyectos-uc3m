"""DocumentJsonStore class"""
from storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import TEST_DOCUMENTS_STORE_FILE
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class DocumentJsonStore(JsonStore):
    """Outer class"""
    class __DocumentJsonStore(JsonStore):
        """Inner class"""
        def __init__(self):
            """init"""
            super().__init__()
            self._file_name = TEST_DOCUMENTS_STORE_FILE
            self.load_store()
            if self._data_list == []:
                raise EnterpriseManagementException("Wrong file  or file path")

    __instance = None

    def __new__(cls):
        if not DocumentJsonStore.__instance:
            DocumentJsonStore.__instance = DocumentJsonStore.__DocumentJsonStore()
        return DocumentJsonStore.__instance
