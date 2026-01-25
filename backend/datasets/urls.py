from django.urls import path
from .views import UploadDatasetView, DatasetHistoryView, DatasetReportView

urlpatterns = [
    path("upload/", UploadDatasetView.as_view(),name="upload_dataset"),
    path("history/", DatasetHistoryView.as_view(),name="dataset_history"),
    path("report/<int:dataset_id>/", DatasetReportView.as_view())
]   
