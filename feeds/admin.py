from django.contrib import admin
from .models import NewsSource, Article, Digest, DigestArticle

# Reg - adminu
@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "rss_url", "active")
    list_filter = ("active",)
    search_fields = ("name", "rss_url")

# Článok - adminu
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "published")
    list_filter = ("source",)
    search_fields = ("title", "link")
    date_hierarchy = "published"

# Inline prip: články - digest
class DigestArticleInline(admin.TabularInline):
    model = DigestArticle
    extra = 1

# Reg - digest (články)
@admin.register(Digest)
class DigestAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    date_hierarchy = "created_at"
    inlines = [DigestArticleInline]

# prip - Digest <-> Article
@admin.register(DigestArticle)
class DigestArticleAdmin(admin.ModelAdmin):
    list_display = ("digest", "article")
    search_fields = ("digest__name", "article__title")
