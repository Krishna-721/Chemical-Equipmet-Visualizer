from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Dataset
from .services import analyze_csv

from .pdfs import generate_report
from io import BytesIO
from django.http import HttpResponse

from .services import analyze_csv, compute_file_checksum
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

class UploadDatasetView(APIView):
    parser_classes=(MultiPartParser,FormParser)
    permission_classes=[IsAuthenticated]
    parser_classes=(MultiPartParser, FormParser)
    authentication_classes=[BasicAuthentication]
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        dataset = Dataset.objects.create(
            filename=file.name,
            file=file
        )

        try:
            summary = analyze_csv(dataset.file.path)
            dataset.summary=summary
            dataset.checksum=compute_file_checksum(dataset.file.path)
            dataset.save()
        except Exception as e:
            dataset.delete()
            return Response(
                {"error":str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Keep only last 5 datasets
        qs = Dataset.objects.order_by("-uploaded_at")
        if qs.count() > 5:
            for old in qs[5:]:
                old.delete()

        return Response(
            {
                "dataset_id": dataset.id,
                "summary": summary
            },
            status=status.HTTP_201_CREATED
        )


class DatasetHistoryView(APIView):
    permission_classes=[IsAuthenticated]
    auth_class=[BasicAuthentication]

    def get(self, request):
        datasets = Dataset.objects.order_by("-uploaded_at")[:5]
        data = [
            {
                "id": d.id,
                "filename": d.filename,
                "uploaded_at": d.uploaded_at,
                "summary": d.summary,
            }
            for d in datasets
        ]
        return Response(data)
    
class DatasetReportView(APIView):
    permission_classes=[IsAuthenticated]
    auth_class=[BasicAuthentication]

    def get(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not dataset.summary:
            return Response(
                {
                    "error": {
                        "code": "NO_SUMMARY",
                        "message": "Report cannot be generated for datasets with no valid analysis"
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        buffer = BytesIO()

        try:
            generate_report(buffer, dataset)
        except Exception as e:
            return Response(
                {
                    "error": {
                        "code": "PDF_GENERATION_FAILED",
                        "message": str(e)
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if buffer.tell() == 0:
            return Response(
                {
                    "error": {
                        "code": "EMPTY_PDF",
                        "message": "Generated PDF is empty"
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/pdf"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="dataset_{dataset_id}_report.pdf"'
        )

        return response

