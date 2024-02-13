from django.contrib import admin

from .models import Lesson, Product, UserAccessibleProduct, UserLessonStatistics


admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(UserAccessibleProduct)
admin.site.register(UserLessonStatistics)
