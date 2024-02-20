from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers

from .models import Lesson, Product, UserAccessibleProduct, UserLessonStatistics


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductStatisticsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    total_lessons_viewed = serializers.IntegerField()
    total_viewing_time = serializers.IntegerField()
    total_students = serializers.IntegerField()
    purchase_percentage = serializers.IntegerField()

    user_count = User.objects.all().count()

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        lessons = Lesson.objects.filter(product=instance.id)
        user_lesson_statistics = UserLessonStatistics.objects.filter(lesson__in=lessons)
        product_users = UserAccessibleProduct.objects.filter(
            product=instance.id
        ).count()

        total_lessons_viewed = user_lesson_statistics.filter(is_viewed=True).count()
        total_viewing_time = (
            user_lesson_statistics.aggregate(Sum("viewing_time"))["viewing_time__sum"]
            or 0
        )
        total_students = product_users
        purchase_percentage = int(product_users / self.user_count * 100)

        instance.total_viewing_time = total_viewing_time
        instance.total_lessons_viewed = total_lessons_viewed
        instance.total_students = total_students
        instance.purchase_percentage = purchase_percentage

        return super().to_representation(instance)


class UserLessonStatisticsSerializer(serializers.ModelSerializer):
    lesson = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = UserLessonStatistics
        exclude = ["user"]
