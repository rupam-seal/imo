from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

# Create your models here.
class Image(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    photo = models.ImageField(upload_to="images")
    date = models.DateTimeField(auto_now_add=True)