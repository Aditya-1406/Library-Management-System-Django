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

    def __str__(self):
        return self.title