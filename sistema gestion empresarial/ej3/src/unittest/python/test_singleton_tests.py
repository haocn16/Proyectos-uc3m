import unittest

from uc3m_consulting.enterprise_manager import EnterpriseManager
from storage.document_json_store import DocumentJsonStore
from storage.project_json_store import ProjectJsonStore
from storage.report_json_store import ReportJsonStore


class TestSingleton(unittest.TestCase):
    def test_singleton_enterprise_manager_tests(self):
        enterprise_manager_1=EnterpriseManager()
        enterprise_manager_2 = EnterpriseManager()
        enterprise_manager_3 = EnterpriseManager()

        self.assertEqual(enterprise_manager_1, enterprise_manager_2)
        self.assertEqual(enterprise_manager_2, enterprise_manager_3)
        self.assertEqual(enterprise_manager_3, enterprise_manager_2)

    def test_singleton_document_json_store_tests(self):
        document_json_store_1=DocumentJsonStore()
        document_json_store_2 = DocumentJsonStore()
        document_json_store_3 = DocumentJsonStore()

        self.assertEqual(document_json_store_1, document_json_store_2)
        self.assertEqual(document_json_store_2, document_json_store_3)
        self.assertEqual(document_json_store_3, document_json_store_1)

    def test_singleton_project_json_store_tests(self):
        project_json_store_1=ProjectJsonStore()
        project_json_store_2 = ProjectJsonStore()
        project_json_store_3 = ProjectJsonStore()

        self.assertEqual(project_json_store_1,project_json_store_2)
        self.assertEqual(project_json_store_2, project_json_store_3)
        self.assertEqual(project_json_store_3, project_json_store_1)

    def test_singleton_report_json_store_tests(self):
        report_json_store_1=ReportJsonStore()
        report_json_store_2 = ReportJsonStore()
        report_json_store_3 = ReportJsonStore()

        self.assertEqual(report_json_store_1,report_json_store_2)
        self.assertEqual(report_json_store_2,report_json_store_3)
        self.assertEqual(report_json_store_3,report_json_store_1)

        # add assertion here


if __name__ == '__main__':
    unittest.main()
