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

class UploadDatasetView(APIView):
    parser_classes=(MultiPartParser,FormParser)
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
    def get(self,request, dataset_id):
        try:
            dataset=Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response(
                {"error":"Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        buffer=BytesIO()
        generate_report(buffer,dataset)
        buffer.seek(0)

        response=HttpResponse(buffer,content_type="application/pdf")
        response["Content-Disposition"]=(
            f'attachment; filename="dataset_{dataset_id}_report.pdf'
        )

        return response

