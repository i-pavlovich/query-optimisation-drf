from django.urls import path

from .views import (
    AccessibleProductsLessonListApiView,
    ProductLessonListApiView,
    ProductStatisticsListApiView,
)


urlpatterns = [
    path(
        "all_lessons/",
        AccessibleProductsLessonListApiView.as_view(),
        name="lesson_list",
    ),
    path(
        "all_lessons/<int:product_id>",
        ProductLessonListApiView.as_view(),
        name="lesson_list_by_product",
    ),
    path(
        "product_statistics/",
        ProductStatisticsListApiView.as_view(),
        name="product_statistics_list",
    ),
]
