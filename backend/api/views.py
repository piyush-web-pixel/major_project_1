import os
import json
import tempfile
from pathlib import Path

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from plotly.utils import PlotlyJSONEncoder

from data_engine.pipeline import run_autoinsight

from .serializers import DatasetUploadSerializer


# =========================================================
# HEALTH CHECK
# =========================================================

@api_view(["GET"])
def health_check(request):

    return Response({
        "status": "success",
        "message": "AutoInsight API is running"
    })


# =========================================================
# ANALYZE DATASET
# =========================================================

class AnalyzeDatasetView(APIView):

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    serializer_class = DatasetUploadSerializer


    # =====================================================
    # POST
    # =====================================================

    def post(self, request):

        print("REQUEST FILES:", request.FILES)
        print("REQUEST DATA:", request.data)

        # -------------------------------------------------
        # VALIDATE UPLOAD
        # -------------------------------------------------

        serializer = self.serializer_class(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "status": "error",
                    "errors": serializer.errors
                },
                status=400
            )

        uploaded_file = serializer.validated_data["file"]

        print(
            "UPLOADED FILE:",
            uploaded_file.name
        )


        # -------------------------------------------------
        # CHECK EXTENSION
        # -------------------------------------------------

        suffix = Path(
            uploaded_file.name
        ).suffix.lower()

        allowed_extensions = [
            ".csv",
            ".xlsx",
            ".xls"
        ]

        if suffix not in allowed_extensions:

            return Response(
                {
                    "status": "error",
                    "message": (
                        "Only CSV, XLSX and XLS "
                        "files are supported."
                    )
                },
                status=400
            )


        temp_path = None


        try:

            # =============================================
            # SAVE TEMPORARY FILE
            # =============================================

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                for chunk in uploaded_file.chunks():

                    temp_file.write(chunk)

                temp_path = temp_file.name


            print(
                "TEMP FILE:",
                temp_path
            )


            # =============================================
            # RUN AUTOINSIGHT
            # =============================================

            result = run_autoinsight(
                temp_path,
                max_charts=10
            )


            # =============================================
            # CONVERT CHARTS
            # =============================================

            charts = []


            for chart in result.get(
                "charts",
                []
            ):

                figure = chart.get(
                    "figure"
                )


                chart_data = {

                    "recommendation": chart.get(
                        "recommendation"
                    ),

                    "success": (
                        figure is not None
                    ),

                    "error": chart.get(
                        "error"
                    ),

                    "figure": None
                }


                # -----------------------------------------
                # PLOTLY → JSON
                # -----------------------------------------

                if figure is not None:

                    chart_data["figure"] = json.loads(

                        json.dumps(
                            figure,
                            cls=PlotlyJSONEncoder
                        )

                    )


                charts.append(
                    chart_data
                )


            # =============================================
            # RESPONSE
            # =============================================

            response_data = {

                "status": "success",

                "file_name": uploaded_file.name,

                "profile": result.get(
                    "profile"
                ),

                "detected_columns": result.get(
                    "detected_columns"
                ),

                "cleaning_report": result.get(
                    "cleaning_report"
                ),

                "analysis": result.get(
                    "analysis"
                ),

                "chart_recommendations": result.get(
                    "chart_recommendations"
                ),

                "charts": charts,

                "insights": result.get(
                    "insights"
                ),

                "report": result.get(
                    "report"
                )
            }


            return Response(
                response_data
            )


        # =============================================
        # ERROR
        # =============================================

        except Exception as error:

            print(
                "ANALYZE ERROR:",
                error
            )

            return Response(
                {
                    "status": "error",
                    "message": str(error)
                },
                status=400
            )


        # =============================================
        # DELETE TEMP FILE
        # =============================================

        finally:

            if (
                temp_path
                and os.path.exists(temp_path)
            ):

                os.remove(
                    temp_path
                )