from pymediainfo import MediaInfo

from shortuuid import uuid

from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from django.db.models import *
from django.contrib.auth.models import User

User = get_user_model()
extra_fields = {"null": True, "blank": True}

      + DEFINIÇÃO
      Autor de um respectivo Curso ou Vídeo

      + Atributos
      - first_name: primeiro nome do Autor
      - last_name: último nome do Autor
      - slug: indentificador do Autor nas urls
      """

      first_name: CharField = models.CharField(max_length=40)
      last_name: CharField = models.CharField(max_length=40)
      slug: CharField = models.SlugField(
            unique=True, 
            editable=False
      )

      def __str__(self):
            """
            Retorna o primeiro e o último nome do Autor
            """
            return self.first_name +" "+ self.last_name
      
      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(self.first_name+self.last_name)
            return super().save(*args, **kwargs)

# TODO: missing cover
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

    CATEGORY_CHOICES = [
        ("DW", "Desenvolvimento Web"),
        ("DM", "Desenvolvimento Mobile"),
        ("CD", "Ciência de Dados"),
        ("RC", "Redes de Computadores"),
        ("Outro", "Outro"),
    ]

    LANGUAGE_CHOICES = [("PT", "Português"), ("EN", "Ingles")]

    cover = models.ImageField("cover", upload_to="course-covers/", **extra_fields)
    preview = models.ForeignKey(
        to="Video",
        on_delete=models.SET_NULL,
        related_name="video_preview",
        **extra_fields,
    )
    teacher = models.CharField(max_length=100, **extra_fields)
    name = models.CharField(max_length=200, **extra_fields)
    description = models.TextField(**extra_fields)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="Outro", **extra_fields
    )
    stars = models.ManyToManyField(User, related_name="courses_with_user_stars")
    publiced_at = models.DateField(auto_now_add=True, **extra_fields)
    updated_at = models.DateField(auto_now=True, **extra_fields)
    slug = models.SlugField(editable=False, **extra_fields)
    uuid = models.CharField(max_length=50, unique=True, **extra_fields)
    language = models.CharField(
        max_length=20, choices=LANGUAGE_CHOICES, default="PT", **extra_fields
    )
    updated_at = models.DateTimeField(auto_now=True, **extra_fields)
    created_at = models.DateTimeField(auto_now_add=True, **extra_fields)

      name: CharField = models.CharField(max_length=200)
      category: CharField = models.CharField(
            choices=CHOCES_CATEGORY, 
            default="OUTROS", 
            max_length=50
      )
      date_publiced: DateField = models.DateField()
      slug: SlugField = models.SlugField(
            unique=True, 
            editable=False
      ) 

<<<<<<< HEAD
      def __str__(self):
            return self.name
      
      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(self.name+self.teacher.first_name+self.teacher.last_name)
            return super().save(*args, **kwargs)
=======
    @property
    def get_stars_in_percentage(self):
        try:
            return round((self.stars.count() * 100) / User.objects.count())
        except:  # noqa
            return 0

    @property
    def get_total_videos(self):
        videos = Video.objects.filter(course=self)
        return videos.count()

    @property
    def get_total_videos_duration(self):
        return (
            (
                Video.objects.filter(course=self).aggregate(total=Sum("duration"))[
                    "total"
                ]
            )
            or 0
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if not self.uuid:
            self.uuid = uuid(name=self.slug)

            while Course.objects.filter(uuid=self.uuid).exists():
                self.uuid = uuid(name=self.slug)

        return super().save(*args, **kwargs)
>>>>>>> dev


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

<<<<<<< HEAD
      curso: Course = models.ForeignKey(
            to=Course, 
            on_delete=models.CASCADE
      )
      title: CharField = models.CharField(max_length=500)
      path: CharField = models.FileField(
            verbose_name="video_path", 
            upload_to="course-videos/", 
            max_length=500
      )
      slug: CharField = models.SlugField(
            unique=True, 
            editable=False
      )
=======
    is_preview = models.BooleanField(default=False)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, **extra_fields)
    title = models.CharField(max_length=150, **extra_fields)
    description = models.TextField(**extra_fields)
    cover = models.ImageField(upload_to="video-cover/", **extra_fields)
    video = models.FileField("videos", upload_to="course-videos/", **extra_fields)
    duration = models.PositiveIntegerField(**extra_fields)
    slug = models.SlugField(editable=False, **extra_fields)
    uuid = models.CharField(max_length=50, unique=True, **extra_fields)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.uuid:
            self.uuid = uuid(name=self.slug)

            while Course.objects.filter(uuid=self.uuid).exists():
                self.uuid = uuid(name=self.slug)

        if self.video:
            try:
                media_info = MediaInfo.parse(self.video.path)
                self.duration = media_info.tracks[0].duration

            except Exception as e:  # noqa
                print(e)
                self.duration = 0

        return super().save(*args, **kwargs)
>>>>>>> dev

      def __str__(self):
            return self.title
      
      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(self.title)
            return super().save(*args, **kwargs)

class Comment(models.Model):
      """
      Model Comment

      + DEFINIÇÃO
      Faz um comentario sobre um video específico

      + Atributos
      - user: relativo a Model User representando que todo comentario terá um Usuário
      - video: O video em que o comentário será exibido
      - content: texto (o texto é o comentário)
      - created_at: data que o comentario foi submetido
      """
      user: User = models.ForeignKey(
            User,
            related_name="videos_comment",
            on_delete=models.CASCADE,
            null=True,
            blank=True,
      )

<<<<<<< HEAD
      video: Video = models.ForeignKey(
            to=Video, 
            related_name="comments", 
            on_delete=models.CASCADE
      )
      content: TextField = models.TextField()
      created_at: DateTimeField = models.DateTimeField(
            auto_now_add=True, 
            null=True, 
            blank=True
      )
=======
    user = models.ForeignKey(
        User, related_name="videos_comment", on_delete=models.CASCADE, **extra_fields
    )
    video = models.ForeignKey(
        Video, related_name="comments", on_delete=models.CASCADE, **extra_fields
    )
    content = models.TextField(**extra_fields)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, **extra_fields)


class Faq(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, **extra_fields)
    question = models.CharField(max_length=80, **extra_fields)
    answer = models.TextField(**extra_fields)
    created_at = models.DateTimeField(auto_now_add=True, **extra_fields)
>>>>>>> dev
