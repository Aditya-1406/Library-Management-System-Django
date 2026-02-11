from django.contrib import admin
from .models import Author, Book
from django.utils.html import format_html

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ("id","title", "author", "available_copies", "published_date","cover_thumb")
    list_filter = ("title", "author")
    search_fields = ("title","author__name")
    ordering = ("isbn",)
    list_display_links = ("title",)
    
    def cover_thumb(self, obj):
            if obj.image:
                return format_html(
                    '<img src="{}" style="height: 50px; width: auto; border-radius:4px;" />',
                    obj.image.url
                )
            return "—"
           





admin.site.register(Author)
admin.site.register(Book, BookAdmin)

