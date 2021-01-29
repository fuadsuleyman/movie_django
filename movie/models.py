from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, PositiveSmallIntegerField, SlugField, TextField
from datetime import date
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField('Name', max_length=150)
    description = models.TextField('Description')
    url = models.SlugField('Slug', max_length=160, unique=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField('Name', max_length=150)
    age = models.PositiveSmallIntegerField('Age', default=0)
    description = models.TextField('Description')
    image = models.ImageField('Poster', upload_to="actors/", null=True)

    class Meta:
        db_table = 'actors'
        verbose_name = 'Actors and Directors'
        verbose_name_plural = 'Actors and Directors'
    
    def get_absolute_url(self):
        return reverse("actor-detail", kwargs={'slug': self.name  })
    
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Genre', max_length=150)
    description = models.TextField('Description')
    url = models.SlugField('Slug', max_length=160, unique=True)

    class Meta:
        db_table = 'genre'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    
    # relations
    directors = models.ManyToManyField(Actor, verbose_name="Directors", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="Actors", related_name="film_actor")
    directors = models.ManyToManyField(Actor, verbose_name="Directors", related_name="film_director")
    genres = models.ManyToManyField(Genre, verbose_name="Genres", related_name="film_genre")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True)
    
    # informations
    title = models.CharField('Title', max_length=100)
    tagline = models.CharField('Slogan', max_length=100)
    image = models.ImageField('Poster', upload_to="movie/")
    year = models.PositiveSmallIntegerField('Produced_at', default=2020)
    country = models.CharField('Country', max_length=50)
    description = models.TextField('Description')
    url = models.SlugField('Slug', max_length=160, unique=True)
    world_premiere = models.DateField('World Premier', default=date.today)
    budget = models.PositiveIntegerField('Budget', default=0, help_text='Write with dollars')
    fees_in_usa = models.PositiveIntegerField('Fees USA', default=0, help_text='Write with dollars')
    fees_in_world = models.PositiveIntegerField('Fees World', default=0, help_text='Write with dollars')
    draft = models.BooleanField("Draft", default=False)

    class Meta:
        db_table = 'movie'
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
    
    # asagida movie-detail urls.py faylinda verdiyimiz name-di
    def get_absolute_url(self):
        return reverse("movie-detail", kwargs={'slug': self.url})
    
    # asagidaki method yalniz parenti olmayan, review-lari getirecek
    # parant-i null olmasi o demekdiki parenti yoxdu
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)
    
    def __str__(self):
        return self.title


class MovieShots(models.Model):

    # relations
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=CASCADE)

    title = models.CharField('Title', max_length=150)
    description = models.TextField('Description')
    image = models.ImageField("Image", upload_to="movie_shots/")

    class Meta:
        db_table = 'movie_shots'
        verbose_name = 'Movie_shots'
        verbose_name_plural = 'Movie_shots'
    
    def __str__(self):
        return self.title
    

class RatingStar(models.Model):

    value = models.SmallIntegerField('value', default=0)

    class Meta:
        db_table = 'rating_star'
        verbose_name = 'Rating_star'
        verbose_name_plural = 'Rating_stars'
        ordering = ["-value"]
    
    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):

    # relations
    star = models.ForeignKey(RatingStar, verbose_name="star", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="movie", on_delete=models.CASCADE)

    ip = models.CharField('IP address', max_length=30)

    class Meta:
        db_table = 'rating'
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
    
    def __str__(self):
        return f'{self.star} - {self.movie}'


class Reviews(models.Model):

    # relations
    movie = models.ForeignKey(Movie, verbose_name="movie", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True)

    # api ishlek veziyyetde olmasi ucun asagidakini qosh
    # movie = models.ForeignKey(Movie, verbose_name="movie", on_delete=models.CASCADE, related_name="reviews")

    # yazdigim api-de childer-leri cixarmaq ucun related_name elave etmisem, amma bu zaman adi qaydada run edende chilren-ler gorunmur, sebebi maraqlidi
    # parent = models.ForeignKey('self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True, related_name="children")

    email = models.EmailField("Email")
    name = models.CharField('Name', max_length=100)
    text = models.TextField('Message', max_length=5000)

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
    
    def __str__(self):
        return f'{self.name} - {self.movie}'










