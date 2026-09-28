"""Module """
import json
import os
from datetime import datetime,timezone
import re
from uc3m_consulting.enterprise_project import EnterpriseProject

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.project_document import ProjectDocument
class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self,company_cif:str,project_acronym:str,
                         operation_name:str,department:str,date:str,
                         budget:float):
        """Register process of a new project and returns its MD5 id"""
        # fix TC6
        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("incorrect CIF datatype")
        # fix TC7
        if len(company_cif) !=9 :
            raise EnterpriseManagementException("CIF must have length 9")

        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("cif doesn't meet validation algorithm")
        # fix TC11
        if not isinstance(project_acronym,str):
            raise EnterpriseManagementException("incorrect acronym datatype")
        # fix TC8
        if len(project_acronym) >10 :
            raise EnterpriseManagementException("acronym length is greater than 10")
        # fix TC9
        if len(project_acronym) <5 :
            raise EnterpriseManagementException("acronym length is shorter than 5")
        # fix TC10
        if not project_acronym.isalnum():
            raise EnterpriseManagementException("acronym contains other characters apart from numbers and letters")
        # fix TC14
        if not isinstance(operation_name,str):
            raise EnterpriseManagementException("incorrect project name datatype")
        # fix TC12
        if len(operation_name)<10:
            raise EnterpriseManagementException("project name length is less than 10")
        # fix TC13
        if len(operation_name)>30:
            raise EnterpriseManagementException("project name length is more than 30")
        # fix TC16 (check datatype before)
        if not isinstance(department, str):
            raise EnterpriseManagementException("incorrect department datatype")
        # fix TC15
        if department not in ("HR","FINANCE","LEGAL","LOGISTICS"):
            raise EnterpriseManagementException("department content not defined")
        # fix TC26 needed before split operation in TC17
        if not isinstance(date, str):
            # check if date is str to do the split operation
            raise EnterpriseManagementException("incorrect date datatype")
        # fix TC17
        date_parts=date.split("/")
        if len(date_parts)!=3:
            raise EnterpriseManagementException("incorrect date format")
        day=date_parts[0]
        month=date_parts[1]
        year=date_parts[2]
        #fix TC18
        day_int=int(day)
        if day_int<1:
            raise EnterpriseManagementException("day value is less than 1")
        #fix TC19
        if day_int>31:
            raise EnterpriseManagementException("day value is more than 31")
        #fix TC20
        month_int=int(month)
        if month_int<1:
            raise EnterpriseManagementException("month value is less than 1")
        #fix TC21
        if month_int>12:
            raise EnterpriseManagementException("month value is more than 12")
        #fix TC22
        year_int=int(year)
        if year_int<2025:
            raise EnterpriseManagementException("year value is less than 2025")
        #fix TC23
        if year_int>2027:
            raise EnterpriseManagementException("year value is more than 2027")
        #fix TC24
        if month_int==2 and day_int>28:
            raise EnterpriseManagementException("date entered is not valid")
        #fix TC25
        input_date=datetime(year_int,month_int,day_int).date()
        today=datetime.today().date()
        if input_date<today:
            raise EnterpriseManagementException("current date is before request to register date")
        #fix TC31 (datatype check, before checking the rest of budget issues)
        if not isinstance(budget, float):
            raise EnterpriseManagementException("incorrect budget datatype")
        #fix TC27
        if budget<50000.00:
            raise EnterpriseManagementException("budget amount is less than 50000.00")
        #fix TC28
        if budget>1000000.00:
            raise EnterpriseManagementException("budget amount is over 1000000.00")
        #fix TC29
        budget_str=str(budget)
        decimals =budget_str.split(".")[1]
        if  len(decimals)>2:
            raise EnterpriseManagementException("budget amount has more than 2 decimal places")
        #fix TC30
        if len(decimals)<2 and decimals !="0":
            raise EnterpriseManagementException("budget amount has less than 2 decimal places")

        #fix TC1 to TC5
        new_project = EnterpriseProject(
            company_cif=company_cif,
            project_acronym=project_acronym,
            project_description=operation_name,
            department=department,
            starting_date=date,
            project_budget=budget
        )
        project_info = new_project.to_json()
        project_id = new_project.project_id
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.normpath(os.path.join(current_dir, "../../../../"))
        store_path = os.path.join(project_root, "src/data/corporate_operations.json")
        operations_list=[]
        if os.path.isfile(store_path):
            with open(store_path,"r",encoding="utf-8") as file:
                try:
                    operations_list=json.load(file)
                except json.JSONDecodeError:
                    pass
        operations_list.append(project_info)
        with open(store_path,"w",encoding="utf-8") as file:
            json.dump(operations_list,file,indent=4)
        return project_id

    def register_document(self,input_file:str):
        '''This method consists in recording documentation associated with each project.'''

        try:
            with open(input_file,"r",encoding="utf-8")as f:
                data=json.load(f)
        except json.JSONDecodeError as exc:
            raise EnterpriseManagementException("KO(JsonDecodeError)") from exc
        except Exception as exc:
            raise EnterpriseManagementException("KO(JsonDecodeError)") from exc

        if not ("FILENAME" in data and "PROJECT_ID" in data):
            raise EnterpriseManagementException("KO(KeyError)")

        project_id_val = data["PROJECT_ID"]
        file_name_val = data["FILENAME"]
        if project_id_val is None:
            raise EnterpriseManagementException("KO(Not a valid Project ID)")
        if file_name_val is None:
            raise EnterpriseManagementException("KO(Not a valid FILENAME)")

        self.validate_filename(file_name_val)
        self.validate_project_id(project_id_val)

        new_doc=ProjectDocument(project_id_val,file_name_val)
        document_hash=new_doc.document_signature

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.normpath(os.path.join(current_dir, "../../../../"))
        store_path = os.path.join(project_root, "src/data/all_documents.json")

        documents_list=[]
        if os.path.isfile(store_path):
            with open(store_path,"r",encoding="utf-8") as file:
                try:
                    documents_list=json.load(file)
                except json.JSONDecodeError:
                    pass
        documents_list.append(new_doc.to_json())
        with open(store_path,"w",encoding="utf-8") as file:
            json.dump(documents_list,file,indent=4)
        return document_hash

    def validate_project_id(self,project_id:str):
        '''method to validate the project id'''

        if not isinstance(project_id, str) or not re.match(r"^[a-fA-F0-9]{32}$", project_id):
            raise EnterpriseManagementException("KO(Not a valid Project ID)")
        return True

    def validate_filename(self,filename:str):
        '''method to validate the filename'''
        if not isinstance(filename, str) or not re.match(r"^[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)$", filename):
            raise EnterpriseManagementException("KO(Not a valid FILENAME)")

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
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

    def check_project_budget(self,project_id:str):
        '''calculates the project expenses'''
        # 1. validate project id
        if not self.validate_project_id(project_id):
            raise EnterpriseManagementException("Project format is not in MD5")
        # 2. read and validate the flows.json input file
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.normpath(os.path.join(current_dir, "../../../../"))
            base_path = os.path.join(project_root, "src/data")

            output_file = os.path.join(base_path, "flows.json")
            with open(output_file, encoding="utf-8", mode="r") as file:
                all_flows=json.load(file)
        except FileNotFoundError as fnfe:
            raise EnterpriseManagementException("File not found") from fnfe
        except json.JSONDecodeError as jde:
            raise EnterpriseManagementException("invalid json format output") from jde
        # 3 initialize the calculation
        total_expenses =0.0
        project_found=False
        #4 aggregate project expenses if found
        for flow in all_flows:
            if flow.get("projectID")==project_id:
                project_found=True
                if "inFlow" in flow:
                    try:
                        tem_flow=float(flow["inFlow"])
                    except ValueError as exc:
                        raise EnterpriseManagementException("invalid flow value") from exc
                    if tem_flow<0:
                        raise EnterpriseManagementException('flow value cannot be negative')
                    total_expenses+=tem_flow
                elif "outFlow" in flow:
                    try:
                        tem_flow=float(flow["outFlow"])
                    except ValueError as exc:
                        raise EnterpriseManagementException("invalid flow value") from exc
                    if tem_flow<0:
                        raise EnterpriseManagementException('flow value cannot be negative')
                    total_expenses -= tem_flow

        if not project_found:
            raise EnterpriseManagementException("project not found in the input file flow.json")
        timestamp =datetime.now(timezone.utc).timestamp()
        expenses_json={
            "projectID":project_id,
            "expenses":total_expenses,
            "date":timestamp
        }
        output_path = os.path.join(base_path, "output_file.json")
        try:
            if os.path.exists(output_path):
                with open(output_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if not isinstance(data, list):
                        data = []
            else:
                data = []
            data.append(expenses_json)
            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except FileNotFoundError as exc:
            raise EnterpriseManagementException("File not found") from exc
        except json.JSONDecodeError as exc:
            raise EnterpriseManagementException("invalid json format output") from exc
        return True
