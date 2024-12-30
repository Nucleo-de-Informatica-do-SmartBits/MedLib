from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify

class Reader(models.Model):
    GRADE_CHOICES = (
        ('10', 'Décima'),
        ('11', 'Décima Primeira'),
        ('12', 'Décima Segunda'),
    )     

    GROUP_CHOICES = (
        ('A', 'Turma A'),
        ('B', 'Turma B'),
        ('C', 'Turma C'),
        ('D', 'Turma D'),
    )   

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reader")
    grade = models.CharField("Classe", max_length=3, choices=GRADE_CHOICES)
    group = models.CharField("Turma", max_length=3, choices=GROUP_CHOICES)
    process_number = models.CharField("Número de processo", max_length=5, unique=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.first_name + self.user.last_name)
            
        super().save(*args, **kwargs)