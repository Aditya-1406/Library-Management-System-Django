from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=20)
    available_copies = models.IntegerField(default=1)
    image = models.ImageField(upload_to='book_images/',null=True,blank=True)

    
    class Meta:
        # default list ordering in admin and queries (you can still override in queries)
        ordering = ("-id",)  # newest first; or use ("-id",) if no created_at
        indexes = [
            models.Index(fields=["-id"]),  # makes ORDER BY fast
        ]


    def __str__(self):
        return self.title