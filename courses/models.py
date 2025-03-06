from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


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
    cover = models.ImageField(
        "cover", upload_to="course-covers/", null=True, blank=True
    )
    preview = models.FileField(
        "preview", upload_to="course-preview/", null=True, blank=True
    )
    teacher = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20, null=True, blank=True, choices=CATEGORY_CHOICES, default="Outro"
    )
    publiced_at = models.DateField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.name + self.teacher.first_name + self.teacher.last_name
            )
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

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    video = models.FileField(
        "videos", upload_to="course-videos/", null=True, blank=True
    )
    slug = models.SlugField(editable=False)

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

    user = models.ForeignKey(
        User,
        related_name="videos_comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    video = models.ForeignKey(Video, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, editable=False
    )
