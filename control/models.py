from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify

# Create your models here.
class Reader(models.Model):
    GRADE_CHOICES: dict = (
        ('10', 'Décima'),
        ('11', 'Décima Primeira'),
        ('12', 'Décima Segunda'),
    )     
    GROUP_CHOICES: dict = {
        ('A', 'Turma A'),
        ('B', 'Turma B'),
        ('C', 'Turma C'),
        ('D', 'Turma D'),
    }
    COURSE_CHOICES: dict = {
        "Informática": 'Informática',
        "Eletrónica": 'Eletrónica'
    }
    user: User = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="reader")
    process_number: int = models.IntegerField(unique=True)
    grade: str = models.CharField("Classe", max_length=3, choices=GRADE_CHOICES)
    course: str = models.CharField("Curso",max_length=30, choices=COURSE_CHOICES)
    group: str = models.CharField("Turma", max_length=3, choices=GROUP_CHOICES)
    photo: str = models.FileField("Perfil",upload_to='profiles-photo/')
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.first_name + self.user.last_name)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username