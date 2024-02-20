from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Lesson, Product, UserAccessibleProduct, UserLessonStatistics
from .serializers import (
    ProductStatisticsSerializer,
    UserLessonStatisticsSerializer,
)


class AccessibleProductsLessonListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonStatisticsSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        accessible_products = UserAccessibleProduct.objects.filter(user=user_id).values(
            "product"
        )
        lessons = Lesson.objects.filter(product__in=accessible_products).values("id")
        queryset = UserLessonStatistics.objects.filter(
            user=user_id, lesson__in=lessons
        ).select_related("lesson")
        return queryset


class ProductLessonListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonStatisticsSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        product_id = self.kwargs["product_id"]
        lessons = Lesson.objects.filter(product=product_id).values("id")
        queryset = UserLessonStatistics.objects.filter(
            user=user_id, lesson__in=lessons
        ).select_related("lesson")
        return queryset


class ProductStatisticsListApiView(generics.ListAPIView):
    serializer_class = ProductStatisticsSerializer
    queryset = Product.objects.all().select_related("author")
