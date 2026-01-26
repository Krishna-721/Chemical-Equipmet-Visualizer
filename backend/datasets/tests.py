from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Dataset

class TestDatasetUpload(TestCase):
    def setUp(self):
        self.client=APIClient()

    def test_valid_csv_upload(self):
        content=(
            "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
            "Pump A, Pump, 100,50,6\n"
            "Valve B, Valve, 80, 3, 50\n"
        )

        file=SimpleUploadedFile(
            "valid_csv",
            content.encode("utf-8"),
            content_type="text/csv"
        )
        response=self.client.post(
            "/api/upload/",
            {"file": file},
            format="multipart"
        )

        self.assertEqual(response.status_code,201)
        self.assertIn("summary",response.data)
        self.assertEqual(Dataset.objects.count(),1)

    def test_empty_csv_failure(self):
        content=(
            "Equipment Name,Type,Flowrate,Pressure,Temperature\n")
        file=SimpleUploadedFile(
            "invalid_csv",
            content.encode("utf-8"),
            content_type="text/csv"
        )
        response=self.client.post(
            "/api/upload/",
            {"file": file},
            format="multipart"
        )

        self.assertEqual(response.status_code,400)
        self.assertIn("error",response.data)
        self.assertEqual(Dataset.objects.count(),0)

    def test_last_five_datasets_are_present(self):
        content=(
        "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
        "Pump A, Pump, 500,40,9\n"
        )
        for i in range(6):
            file=SimpleUploadedFile(
                f"file_{i}.csv",
                content.encode("utf-8"),
                content_type="text/csv"
            )

            response=self.client.post(
                "/api/upload/",
                {"file":file},
                format="multipart"
            )

            self.assertEqual(response.status_code,201)
        self.assertEqual(Dataset.objects.count(),5)

    def test_missing_column_fails(self):
        content = (
            "Equipment Name,Type,Flowrate,Pressure\n"  # Temperature missing
            "Pump A,Pump,100,5\n"
        )

        file = SimpleUploadedFile(
            "missing_column.csv",
            content.encode("utf-8"),
            content_type="text/csv"
        )

        response = self.client.post(
            "/api/upload/",
            {"file": file},
            format="multipart"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing columns", response.data["error"])
        self.assertEqual(Dataset.objects.count(), 0)
    
    def test_history_requires_auth(self):
        response=self.client.get("/api/history")
        self.assertEqual(response.status_code,403)