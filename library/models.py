from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    genChoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('scifi','Sci-Fi')
    ]
    
    isbn = models.CharField(max_length=13)
    book_name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=60)
    cover_image = models.ImageField(upload_to="images")
    summary = models.TextField()
    author_email = models.EmailField()
    genre = models.CharField(max_length=40, choices=genChoice)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.BooleanField(default=False)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    slug = models.SlugField()

    def save(self, *args, **kwargs):    
        self.slug = slugify(self.book_name)
        super(Book, self).save(*args, **kwargs) 


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=50)
    borrowing_history = models.TextField(blank=True)
    outstanding_fines = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username
    
class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    notification_status = models.BooleanField(default=False)

class Fine(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.BooleanField(default=False)

class Notification(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)