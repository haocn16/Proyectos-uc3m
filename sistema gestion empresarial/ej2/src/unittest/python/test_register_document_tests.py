'''This module will check the register_document_test method with syntax testing method'''
import unittest
import os
import hashlib
import re
import json
from datetime import datetime,timezone
from freezegun import freeze_time
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class TestRegisterDocument(unittest.TestCase):
    '''docstring for the class'''

    @classmethod
    def setUpClass(cls):
        """Loads all test cases from f2_tests.txt.txt into a list"""
        current_dir= os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.normpath(os.path.join(current_dir, "../../../"))
        store_path=os.path.join(project_root,"src/data/all_documents.json")
        #if all_documents.json is there already, we can remove it and recreate it, so we never repeat content
        if os.path.isfile(store_path):
            os.remove(store_path)
        tests_file_path= os.path.join(project_root,"src/data/f2_tests.txt")
        lines=[]
        try:
            with open(tests_file_path,encoding="utf-8") as file:
                for line in file:
                    lines.append(line.strip())
        except FileNotFoundError as fnfe:
            raise EnterpriseManagementException("Wrong file or path") from fnfe
        cls._f2_test_data=lines

    def _generate_tmp_test_data_file(self,input_data):
        """Generates an individual test file with one entry to test"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.normpath(os.path.join(current_dir, "../../../"))
        tmp_file_path = os.path.join(project_root, "src/data/f2_tmp_test.json")
        try:
            with open(tmp_file_path,encoding="utf-8",mode="w") as file:
                file.write(input_data)
            return tmp_file_path
        except (FileNotFoundError,PermissionError,OSError) as e:
            raise EnterpriseManagementException("I/O error or System error while accessing file") from e

    def _get_store_hash(self):
        """Gets md5 hash for the store to check it hasn't been modified by bad tests"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.normpath(os.path.join(current_dir, "../../../"))
        store_path = os.path.join(project_root, "src/data/all_documents.json")
        try:
            with open(store_path,"rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except FileNotFoundError:
            return ""

    @freeze_time("2026-03-11")
    def test_valid_cases(self):
        '''method to check the valid cases'''
        for index,input_data in enumerate(self._f2_test_data):
            if index + 1 in [1,2,3]:
                test_id="TC"+str(index+1)
                with self.subTest(test_id=test_id):
                    print("Executing: "+test_id+" with data: "+input_data)
                    tmp_file_path=self._generate_tmp_test_data_file(input_data)
                    manager=EnterpriseManager()
                    #generate hash
                    generated_hash=manager.register_document(tmp_file_path)
                    #get expected hash
                    data=json.loads(input_data)
                    proj_id=data["PROJECT_ID"]
                    file_name= data["FILENAME"]
                    test_date = str(datetime.now(timezone.utc).timestamp())
                    expected_str = "{alg:SHA-256,typ:DEPOSIT,project_id:" + proj_id + ",file_name:" + file_name + ",register_date:" + test_date + "}"
                    expected_hash= hashlib.sha256(expected_str.encode()).hexdigest()
                    #check asserts
                    self.assertEqual(len(generated_hash),64)
                    self.assertTrue(re.match(r"^[a-f0-9]{64}$", generated_hash.lower()))
                    self.assertEqual(generated_hash,expected_hash)

    def test_invalid_cases(self):
        '''the function to check all invalid cases'''
        original_hash=self._get_store_hash()
        for index, input_data in enumerate(self._f2_test_data):
            if index+1>3:
                test_id="TC"+str(index+1)
                with self.subTest(test_id=test_id):
                    print("Executing: " + test_id + " with data: " + input_data)
                    tmp_file_path=self._generate_tmp_test_data_file(input_data)
                    manager=EnterpriseManager()
                    with self.assertRaises(EnterpriseManagementException) as result:
                        manager.register_document(tmp_file_path)

                    if test_id in ["TC50","TC51","TC54","TC55","TC56","TC57","TC58","TC59","TC75","TC76"]:
                        self.assertEqual(result.exception.message,"KO(Not a valid FILENAME)")
                    if test_id in ["TC4","TC5","TC6","TC7","TC9","TC10","TC11","TC12","TC13","TC14","TC15",
                                   "TC16","TC17","TC18","TC19","TC20","TC21","TC22","TC23","TC24","TC25","TC26","TC27","TC28","TC29","TC30","TC31",
                                   "TC34","TC35","TC36","TC37","TC40","TC41","TC42","TC43","TC46","TC47","TC48",
                                   "TC49","TC52","TC53","TC60","TC61","TC62","TC64","TC65","TC66","TC68","TC69","TC70",
                        "TC72","TC73","TC74","TC77"]:
                        self.assertEqual(result.exception.message,"KO(JsonDecodeError)")
                    if test_id in ["TC8","TC32","TC33","TC44","TC45","TC63","TC71"]:
                        self.assertEqual(result.exception.message,"KO(KeyError)")
                    if test_id in ["TC38","TC39","TC67"]:
                        self.assertEqual(result.exception.message,"KO(Not a valid Project ID)")
        final_hash=self._get_store_hash()
        self.assertEqual(final_hash,original_hash)
if __name__ == '__main__':
    unittest.main()
