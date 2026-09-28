"""This is a module to test the register_project method"""
import json
import unittest
import os
import sys
from freezegun import freeze_time
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterProject(unittest.TestCase):
    """This class collects all tests for register_project method"""
    @freeze_time("2026-03-11")
    def test_valid_cases(self):
        """Loops through all valid cases in JSON file"""
        #list with valid tests
        valid_ids=["TC1","TC2","TC3","TC4","TC5"]

        for data in self.register_project_inputs:
            if data["idTest"] in valid_ids:
                with self.subTest(i=data["idTest"]):
                    manager=EnterpriseManager()
                    generated=manager.register_project(data["companyCIF"],
                                             data["projectAcronym"],
                                             data["operationName"],
                                             data["department"],
                                             data["date"],
                                             data["budget"])
                    #result is correct 32 char MD5 string
                    self.assertEqual(len(generated),32)
                    md5_pattern=r"^[a-f0-9]{32}"
                    # self.assertRegexpMatches(generated.lower(), md5_pattern)no longer exists
                    # in modern versions of Python.
                    self.assertRegex(generated.lower(), md5_pattern)

    def test_invalid_cases(self):
        """Loops through all invalid cases in JSON file"""
        #list with invalid tests
        invalid_ids=["TC6","TC7","TC8","TC9","TC10","TC11","TC12","TC13","TC14",
                     "TC15","TC16","TC17","TC18","TC19","TC20","TC21","TC22",
                     "TC23","TC24","TC25","TC26","TC27","TC28","TC29","TC30",
                     "TC31","TC32"]

        for data in self.register_project_inputs:
            if data["idTest"] in invalid_ids:
                with self.subTest(i=data["idTest"]):
                    manager=EnterpriseManager()
                    with self.assertRaises(EnterpriseManagementException) as result:
                        manager.register_project(data["companyCIF"],
                                                 data["projectAcronym"],
                                                 data["operationName"],
                                                 data["department"],
                                                 data["date"],
                                                 data["budget"])
                        self.assertEqual(result.exception.message, data["expectedError"])

    @classmethod
    def setUpClass(cls):
        """Opens and returns a variable with the JSON file test data"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.normpath(os.path.join(current_dir, "../../../"))
        python_path = os.path.join(project_root, "main/python")
        sys.path.append(python_path)

        base_path = os.path.join(project_root, "src/data")

        store_file = os.path.join(base_path, "corporate_operations.json")
        if os.path.isfile(store_file):
            os.remove(store_file)

        json_path =os.path.join(base_path, "register_project_inputs.json")
        try:
            with open(json_path,encoding="UTF-8",mode="r") as json_file:
                register_project_inputs = json.load(json_file)
                print ("Data read is: " + str(register_project_inputs))
        except FileNotFoundError as exc:
            raise EnterpriseManagementException("Wrong file or path") from exc
        except json.JSONDecodeError:
            register_project_inputs = []
        cls.register_project_inputs = register_project_inputs
if __name__ == '__main__':
    unittest.main()
