from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from .models import Dataset
from .services import analyze_csv

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
