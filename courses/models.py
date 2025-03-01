from django.db import models
from django.utils.text import slugify

# Create your models here.
class Teacher(models.Model):
      first_name: str = models.CharField(max_length=40)
      last_name: str = models.CharField(max_length=40)
      slug: str = models.SlugField(default="None")

      def __str__(self):
            return self.first_name + self.last_name
      
      def save(self, *args, **kwargs):
            if not self.slug or self.slug == "None":
                  self.slug = slugify(self.first_name+self.last_name)
            return super().save(*args, **kwargs)

class Course(models.Model):
      CHOCES_CATEGORY: list[tuple] = [
            ("PROGRAMAÇÃO", "PROGRAMAÇÃO"),
            ("REDES", "REDES"),
            ("ELETRÓNICA", "ELETRÓNICA"),
            ("ANÓNIMO", "ANÓNIMO"),
            ("OUTROS", "OUTROS"),
      ]
      teacher: Teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE)

      name: str = models.CharField(max_length=200)
      category: str = models.CharField(choices=CHOCES_CATEGORY, default="ANÓNIMO", max_length=50)
      date_publiced: str = models.DateField()
      slug: str = models.SlugField(default="None") 

      def __str__(self):
            return self.name
      
      def save(self, *args, **kwargs):
            if not self.slug or self.slug == "None":
                  self.slug = slugify(self.name+self.teacher.first_name+self.teacher.last_name)
            return super().save(*args, **kwargs)


class Video(models.Model):
      curso: Course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
      title: str = models.CharField(max_length=500)
      path: str = models.FileField(verbose_name="video_path", upload_to="course-videos/", max_length=500)
      slug: str = models.SlugField(default="None")

      def __str__(self):
            return self.title
      
      def save(self, *args, **kwargs):
            if not self.slug or self.slug == "None":
                  self.slug = slugify(self.title)
            return super().save(*args, **kwargs)

