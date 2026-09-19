from django.urls import path

from .views import (
    health_check,
    AnalyzeDatasetView
)


urlpatterns = [

    path(
        "health/",
        health_check,
        name="health"
    ),

    path(
        "analyze/",
        AnalyzeDatasetView.as_view(),
        name="analyze"
    ),

]