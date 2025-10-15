from django.db import models


class NewsSource(models.Model):
    # Zdroj - name - url -act
    name = models.CharField(max_length=255)
    rss_url = models.URLField(unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    # Zdroj - delete - članky deleted
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    link = models.URLField(unique=True)  # jednoduché pravidlo proti duplicitám
    published = models.DateTimeField(null=True, blank=True)  # niektoré RSS nemajú dátum
    summary = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Digest(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class DigestArticle(models.Model):
    digest = models.ForeignKey(Digest, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("digest", "article")  # ten istý článok v jednom digeste len raz

    def __str__(self):
        return f"{self.digest} -> {self.article}"
