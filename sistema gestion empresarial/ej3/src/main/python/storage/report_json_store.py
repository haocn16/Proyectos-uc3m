"""report json store class, or also known as num_docs"""
from storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE

class ReportJsonStore(JsonStore):
    """outer class"""
    class __ReportJsonStore(JsonStore):
        """inner class"""
        def __init__(self):
            super().__init__()
            self._file_name= TEST_NUMDOCS_STORE_FILE
            self.load_store()

        def add_item(self, item):
            self._data_list.append(item)
            self.save_store()

    __instance=None
    def __new__(cls):
        if not ReportJsonStore.__instance:
            ReportJsonStore.__instance=ReportJsonStore.__ReportJsonStore()
        return ReportJsonStore.__instance
