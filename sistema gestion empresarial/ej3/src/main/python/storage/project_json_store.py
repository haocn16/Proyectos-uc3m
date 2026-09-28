"""project json store class"""
from storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class ProjectJsonStore(JsonStore):
    """outer class"""
    class __ProjectJsonStore(JsonStore):
        """inner class"""
        def __init__(self):
            super().__init__()
            self._file_name=PROJECTS_STORE_FILE
            self.load_store()

        def add_item(self, item):
            if self.find_item(item.to_json()) is not None:
                raise EnterpriseManagementException("Duplicated project in projects list")
            super().add_item(item)

    __instance=None
    def __new__(cls):
        if not ProjectJsonStore.__instance:
            ProjectJsonStore.__instance=ProjectJsonStore.__ProjectJsonStore()
        return ProjectJsonStore.__instance
