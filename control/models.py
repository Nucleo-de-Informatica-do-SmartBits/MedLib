from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Reader(models.Model):
     user: User = models.ForeignKey(to=User, on_delete=models.CASCADE)
     process_number: int = models.IntegerField(unique=True)

     GRADE_CHOICES: dict = {
          10: '10ª',
          11: '11ª',
          12: '12ª',
          13: '13ª',
     }
     grade: int = models.IntegerField(choices=GRADE_CHOICES)

     COURSE_CHOICES: dict = {
          "informatica": 'Informatica',
          "eletronica": 'Eletronica'
     }
     course: str = models.CharField(max_length=30, choices=COURSE_CHOICES)

     GROUP_CHOICES: dict = {
          "A": 'A',
          "B": 'B',
          "C": 'C',
     }
     group: str = models.CharField(max_length=1, choices=GROUP_CHOICES)

     photo: str = models.FileField(upload_to='profiles-photo/')