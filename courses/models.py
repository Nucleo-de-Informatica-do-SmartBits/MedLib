from django.db import models
from django.utils.text import slugify
from django.db.models import *

# Create your models here.
class Teacher(models.Model):
      """
      Model Teacher

      + DEFINIÇÃO
      Autor de um respectivo Curso ou Vídeo

      + Atributos
      - first_name: primeiro nome do Autor
      - last_name: último nome do Autor
      - slug: indentificador do Autor nas urls
      """

      first_name: CharField = models.CharField(max_length=40)
      last_name: CharField = models.CharField(max_length=40)
      slug: CharField = models.SlugField(unique=True , editable=False)

      def __str__(self):
            """
            Retorna o primeiro e o último nome do Autor
            """
            return self.first_name + self.last_name
      
      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(self.first_name+self.last_name)
            return super().save(*args, **kwargs)

class Course(models.Model):
      """
      Model Course

      + DEFINIÇÃO
      Cria um curso nas categorias de (PROGRAMAÇÃO, ELETRÓNICA, REDES, OUTROS)
            *OUTROS
                  Indica que esse curso será uma coleção de video
                  que podem não estar relacionada a tecnologia

      + Atributos
      - teacher: cria um relacionamento de 1-N com a Model Teacher
      - name: (nome/título) do curso
      - category: categoria do curso (PROGRAMAÇÃO, ELETRÓNICA, REDES, OUTROS) default=OUTROS
      - date_publiced: data de publicação do curso
      - slug: indentificador do curso nas urls
      """

      CHOCES_CATEGORY: list[tuple] = [
            ("PROGRAMAÇÃO", "PROGRAMAÇÃO"),
            ("ELETRÓNICA", "ELETRÓNICA"),
            ("OUTROS", "OUTROS"),
            ("REDES", "REDES"),
      ]
      teacher: Teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE)

      name: CharField = models.CharField(max_length=200)
      category: CharField = models.CharField(choices=CHOCES_CATEGORY, default="OUTROS", max_length=50)
      date_publiced: DateField = models.DateField()
      slug: SlugField = models.SlugField(unique=True, editable=False) 

      def __str__(self):
            return self.name
      
      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(self.name+self.teacher.first_name+self.teacher.last_name)
            return super().save(*args, **kwargs)


class Video(models.Model):
      """
      Model Video

      + DEFINIÇÃO
      cria vídeos para um respectivo Curso

      + Atributos
      - curso: relacionamento de 1-N com a model Curso
      - title: (nome/título) do vídeo
      - path: caminho onde está o vídeo que deverá ser colocado em course-videos/
      - slug: identificador do vídeo nas urls
      """

      curso: Course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
      title: CharField = models.CharField(max_length=500)
      path: CharField = models.FileField(verbose_name="video_path", upload_to="course-videos/", max_length=500)
      slug: CharField = models.SlugField(unique=True, editable=False)

      def __str__(self):
            return self.title
      
      def save(self, *args, **kwargs):
            if not self.slug or self.slug == "None":
                  self.slug = slugify(self.title)
            return super().save(*args, **kwargs)
