from django.contrib.auth.models import User
from django.db import models


class Lesson(models.Model):
    title = models.CharField(max_length=150)
    video_link = models.CharField(max_length=500)
    duration = models.PositiveIntegerField()

    product = models.ManyToManyField("Product")

    def __str__(self) -> str:
        return f"{self.title}"


class Product(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}"


class UserAccessibleProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self) -> str:
        return (
            f"User {self.user.username} has access to the {self.product.title} product"
        )


class UserLessonStatistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    viewing_time = models.PositiveIntegerField()
    is_viewed = models.BooleanField()

    class Meta:
        unique_together = ("user", "lesson")

    def save(self, *args, **kwargs) -> None:
        self.is_viewed = False
        if self.viewing_time >= self.lesson.duration * 0.8:
            self.is_viewed = True
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        result = f"User {self.user.username} started the lesson {self.lesson.title}"
        if self.is_viewed:
            result = f"User {self.user.username} viewed the lesson {self.lesson.title}"
        return result
