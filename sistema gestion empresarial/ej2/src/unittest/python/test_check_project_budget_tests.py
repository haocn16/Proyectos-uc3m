'''This module will check the check_project_budget method from enterprise_manager
using structural testing technique'''
import unittest
import os.path
import os
import json
import hashlib
from unittest.mock import patch
from freezegun import freeze_time
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from _io import open as real_open

class TestCheckProjectBudget(unittest.TestCase):
    """This class manages the budget of the projects"""
    @classmethod
    def setUpClass(cls):
        """loads all tests"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root = os.path.normpath(os.path.join(current_dir, "../../../"))
        cls.__path_tests = os.path.join(root, "src/data/")
        cls.__path_data = os.path.join(root, "src/data/")
        try:
            with open(cls.__path_tests + "f3_tests.json", encoding='UTF-8', mode="r") as f:
                test_data_f3 = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("file not found") from e
        except json.JSONDecodeError:
            test_data_f3 = []
        cls.__test_data_f3 = test_data_f3
        # Clear the output file from previous runs
        output_file = cls.__path_data + "/output_file.json"
        if os.path.isfile(output_file):
            os.remove(output_file)
        return True

    @freeze_time("2026-03-11")
    def test_valid(self):
        """Expected TRUE as result, ensuring output is stored to output_file.json"""
        for index, input_data in enumerate(self.__test_data_f3):
            if index+1 in [1,7,11,14,18,19,20]:
                test_id="TC"+str(index+1)
                with self.subTest(test_id=test_id):
                    #just to know which one we are executing
                    print("Executing: " + test_id)
                    manag=EnterpriseManager()
                    budg=manag.check_project_budget(input_data["projectID"])
                    self.assertTrue(budg)
                    try:
                        with open(self.__path_data + "output_file.json", encoding='UTF-8', mode="r") as f:
                            output_file = json.load(f)
                    except FileNotFoundError as exc:
                        raise EnterpriseManagementException("file not found") from exc
                    except json.JSONDecodeError:
                        self.fail("Invalid JSON format in output_file.json")
                    self.assertIsInstance(output_file, list)
                    output_found = False
                    for output in output_file:
                        if output["projectID"].strip().lower() == input_data["projectID"].strip().lower():
                            output_found = True
                            self.assertIn("expenses", output)
                            self.assertIn("date", output)

                            self.assertIsInstance(output["expenses"], float)
                            self.assertIsInstance(output["date"], float)

                    self.assertTrue(output_found, f"{test_id}: projectID not found in output file")

    def get_store_hash(self):
        """ Gets md5 hash"""
        try:
            with open(self.__path_data + "output_file.json", encoding='UTF-8', mode="r") as f:
                file_hash = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        except FileNotFoundError:
            file_hash = ""
        return file_hash

    def test_invalid(self):
        '''function to check all invalid cases that appear in the test table'''
        original_hash = self.get_store_hash()
        # Save the real flows.json content into memory before we start
        flows_file_path = os.path.join(self.__path_data, "flows.json")
        output_file = os.path.join(self.__path_data, "output_file.json")
        with open(flows_file_path, "r", encoding="utf-8") as f:
            real_flows_data = f.read()
        for index, input_data in enumerate(self.__test_data_f3):
            if index + 1 in [2,3,4,5,6,8,9,10,12,13,15,16,17,21,22]:  #ignore impossible cases
                test_id = "TC" + str(index + 1)
                with self.subTest(test_id):
                    #just to know which one we are executing
                    print("Executing: " + test_id)
                    manag = EnterpriseManager()
                    flows_bckp_file = os.path.join(self.__path_data, "flows_bckp.json")

                    #simulate some cases: TC3,TC4,TC5,TC13,TC16
                    try:
                        if test_id=="TC3":
                            if os.path.isfile(flows_bckp_file):
                                os.remove(flows_bckp_file)
                            if os.path.isfile(flows_file_path):
                                os.rename(flows_file_path, flows_bckp_file)
                        elif test_id=="TC4":
                            with open(flows_file_path, "w", encoding="utf-8") as f:
                                f.write('[{broken json')
                        elif test_id == "TC5":
                            # Empty database to trigger "project not found" immediately (0 iterations)
                            with open(flows_file_path, "w", encoding="utf-8") as f:
                                f.write("[]")
                        elif test_id in ["TC13", "TC16"]:
                            # Break output file to trigger JSONDecodeError on read
                            with open(output_file, "w", encoding="utf-8") as f:
                                f.write("[{broken")

                    #assertion phase
                        #special case: mock
                        if test_id in ["TC12", "TC15"]:
                            with patch('builtins.open') as mock_open:
                                def side_effect(*args, **kwargs):
                                    if len(args) > 0 and "output_file.json" in args[0] and (
                                            'w' in kwargs.get('mode', '') or (len(args) > 1 and 'w' in args[1])):
                                        raise FileNotFoundError
                                    return real_open(*args, **kwargs)
                                mock_open.side_effect = side_effect
                                with self.assertRaises(EnterpriseManagementException) as result:
                                    manag.check_project_budget(input_data["projectID"])
                        else:
                            # Standard execution for all other KO tests
                            with self.assertRaises(EnterpriseManagementException) as result:
                                manag.check_project_budget(input_data["projectID"])

                        #verification

                        #related to projectID
                        if test_id in ["TC2", "TC21", "TC22"]:
                            self.assertEqual(result.exception.message, "KO(Not a valid Project ID)")

                        # flows.json read errors
                        elif test_id == "TC3":
                            self.assertEqual(result.exception.message, "File not found")
                        elif test_id == "TC4":
                            self.assertEqual(result.exception.message, "invalid json format output")

                        # Project Not Found
                        elif test_id in ["TC5", "TC6", "TC10"]:
                            self.assertEqual(result.exception.message, "project not found in the input file flow.json")

                        # Values and Datatypes ("apple" and "-0.1")
                        elif test_id == "TC8":
                            self.assertEqual(result.exception.message, "invalid flow value")
                        elif test_id in ["TC9", "TC17"]:
                            self.assertEqual(result.exception.message, "flow value cannot be negative")

                        # output_file.json errors
                        elif test_id in ["TC12", "TC15"]:
                            self.assertEqual(result.exception.message, "File not found")
                        elif test_id in ["TC13", "TC16"]:
                            self.assertEqual(result.exception.message, "invalid json format output")
                    finally:
                        #restore everything
                        if test_id == "TC3":
                            if os.path.isfile(flows_file_path):
                                os.remove(flows_file_path)
                            if os.path.isfile(flows_bckp_file):
                                os.rename(flows_bckp_file, flows_file_path)
                        if test_id in ["TC4", "TC5"]:
                            with open(flows_file_path, "w", encoding="utf-8") as f:
                                f.write(real_flows_data)
                        elif test_id in ["TC13", "TC16"]:
                            if os.path.exists(output_file):
                                os.remove(output_file)

        final_hash=self.get_store_hash()
        self.assertEqual(final_hash,original_hash)
if __name__ == '__main__':
    unittest.main()
