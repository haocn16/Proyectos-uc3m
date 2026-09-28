'''Module to manage the enterprise reading the test data that is taken
from the json file and validating the CIF'''

import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_request import EnterpriseRequest

class EnterpriseManager:
    '''Class that contain all the method to manage the enterprise'''
    def __init__(self):
        pass

    def validateCif(self, cif:str):
        '''Necessary method to validate the CIF value '''
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
        i = 1
        addition = 0
        multiplication = 0
        while i <= 7:
            if i % 2 == 0:
                addition = addition + int(cif[i])
                i += 1
            else:
                aux = int(cif[i]) * 2
                if aux >= 10:  # 2 digits
                    multiplication = multiplication + (aux // 10) + (aux % 10)
                else:
                    multiplication = multiplication + aux
                i += 1

        result = str(addition + multiplication)
        unit = result[-1]
        letters = "JABCDEFGHI"

        if unit == '0':
            base_digit = 0
        else:
            base_digit = 10 - int(unit)

        if cif[0] in "ABEH" and cif[8] == str(base_digit):
            return True
        if cif[0] in "KPQS" and cif[8] == letters[base_digit]:
            return True
        return False

    def readProductCodeFromJson(self, fi):
        '''Method to read the information that is store in the json file'''

        try:
            with open(fi, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from e


        try:
            t_cif = data["cif"]
            t_phone = data["phone"]
            e_name = data["enterprise_name"]
            req = EnterpriseRequest(t_cif, t_phone,e_name)
        except KeyError as e:
            raise EnterpriseManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.validateCif(t_cif) :
            raise EnterpriseManagementException("Invalid FROM IBAN")
        return req
