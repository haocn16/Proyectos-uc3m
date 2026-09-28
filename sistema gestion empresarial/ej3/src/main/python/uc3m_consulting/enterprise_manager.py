"""Module """

from datetime import datetime, timezone

from storage.project_json_store import ProjectJsonStore
from storage.report_json_store import ReportJsonStore
from storage.document_json_store import DocumentJsonStore
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from attributes.date_format import DateFormat

class EnterpriseManager:
    """Outer class"""
    class __EnterpriseManager:
        """Class for providing the methods for managing the orders"""
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments, too-many-positional-arguments
        def register_project(self,
                             company_cif: str,
                             project_acronym: str,
                             project_description: str,
                             department: str,
                             date: str,
                             budget: str):
            """registers a new project"""

            new_project = EnterpriseProject(company_cif=company_cif,
                                            project_acronym=project_acronym,
                                            project_description=project_description,
                                            department=department,
                                            starting_date=date,
                                            project_budget=budget)

            project_store = ProjectJsonStore()
            project_store.add_item(new_project)
            return new_project.project_id


        def find_docs(self, date_str):
            """
            Generates a JSON report counting valid documents for a specific date.

            Checks cryptographic hashes and timestamps to ensure historical data integrity.
            Saves the output to 'resultado.json'.

            Args:
                date_str (str): date to query.

            Returns:
                number of documents found if report is successfully generated and saved.

            Raises:
                EnterpriseManagementException: On invalid date, file IO errors,
                    missing data, or cryptographic integrity failure.
            """
            DateFormat(date_str)

            # open documents
            document_list = DocumentJsonStore()
            result_count = 0

            # loop to find
            result_count=ProjectDocument.calc_num_docs(date_str,document_list,result_count)
            #check the result of the count
            if result_count == 0:
                raise EnterpriseManagementException("No documents found")
            # prepare json text
            report_timestamp = datetime.now(timezone.utc).timestamp()
            report_entry = {"Querydate":  date_str,
                 "ReportDate": report_timestamp,
                 "Numfiles": result_count
                 }

            report_store=ReportJsonStore()
            report_store.add_item(report_entry)
            return result_count

    __instance=None
    def __new__(cls):
        if not EnterpriseManager.__instance:
            EnterpriseManager.__instance = EnterpriseManager.__EnterpriseManager()
        return EnterpriseManager.__instance
