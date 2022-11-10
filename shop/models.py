from django.db import models

# Create your models here.


class Product(models.Model):
    BOOK_GENRES_CHOICES = [
        ('Action', 'Action and adventure'),
        ('Art', 'Art/architecture'),
        ('Alternate history', 'Alternate history'),
        ('Autobiography', 'Autobiography'),
        ('Anthology', 'Anthology'),
        ('Biography', 'Biography'),
        ('Business', 'Business/economics'),
        ('Children', 'Children'),
        ('Crafts/hobbies', 'Crafts/hobbies'),
        ('Classic', 'Classic'),
        ('Cookbook', 'Cookbook'),
        ('Comic book', 'Comic book'),
        ('Diary', 'Diary'),
        ('Dictionary', 'Dictionary'),
        ('Crime', 'Crime'),
        ('Encyclopedia', 'Encyclopedia'),
        ('Drama', 'Drama'),
        ('Fairytale', 'Fairytale'),
        ('Health', 'Health/fitness'),
        ('Fantasy', 'Fantasy'),
        ('History', 'History'),
        ('Graphic novel', 'Graphic novel'),
        ('Home and garden', 'Home and garden'),
        ('Historical fiction', 'Historical fiction'),
        ('Humor', 'Humor'),
        ('Horror', 'Horror'),
        ('Journal', 'Journal'),
        ('Mystery', 'Mystery'),
        ('Math', 'Math'),
        ('Paranormal romance', 'Paranormal romance'),
        ('Memoir', 'Memoir'),
        ('Picture book', 'Picture book'),
        ('Philosophy', 'Philosophy'),
        ('Poetry', 'Poetry'),
        ('Prayer', 'Prayer'),
        ('Political thriller', 'Political thriller'),
        ('Religion', 'Religion, spirituality, and new age'),
        ('Romance', 'Romance'),
        ('Textbook', 'Textbook'),
        ('Satire', 'Satire'),
        ('True crime', 'True crime'),
        ('Science fiction', 'Science fiction'),
        ('Review', 'Review'),
        ('Short story', 'Short story'),
        ('Science', 'Science'),
        ('Suspense', 'Suspense'),
        ('Self help', 'Self help'),
        ('Thriller', 'Thriller'),
        ('Sports and leisure', 'Sports and leisure'),
        ('Western', 'Western'),
        ('Travel', 'Travel'),
        ('Young adult', 'Young adult'),
    ]
    product_name = models.CharField(blank=True, max_length=255)
    author_name = models.CharField(blank=True, max_length=255)
    price = models.FloatField(blank=True, null=True, default=1)
    digital = models.BooleanField(default=False, null=True, blank=False)
    genres = models.CharField(
        max_length=150, choices=BOOK_GENRES_CHOICES, default='Textbook')
    quantity = models.IntegerField(blank=False, default=1)
    product_pic = models.ImageField(
        default='book-default.jpg', upload_to='product')

    def __str__(self):
        return f'{self.product_name}'
