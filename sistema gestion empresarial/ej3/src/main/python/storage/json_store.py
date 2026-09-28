"""Json class"""
import json

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class JsonStore:
    """manage json operations"""
    _file_name=""
    _data_list=[]

    def __init__(self):
        pass

    def find_item(self,item):
        """finds the json file"""
        for candidate in self._data_list:
            if candidate == item:
                return item
        return None

    def add_item(self,item):
        """appends the json file and saves it"""
        self._data_list.append(item.to_json())
        self.save_store()

    def load_store(self):
        """load json file"""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def save_store(self):
        """save and store json file"""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
