from django import template
from movie.models import Category, Movie

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()


# bu asagidaki moteshemdi, sidebar-in icinden son filmler adli hisseni goturub last_movie.html faylina atdim
# hemin html fayl-in yerini asagida qeyd edirem
# bu mavie_tag faylini sidebar.html-de load edirem, goturub apardigim html-in yerine asagidaki funqsiyanin adini verirem
# count=5 arqumentini vermekle nece kino cixmasini nizamlayiram
@register.inclusion_tag('movie/tags/last_movie.html')
def get_last_movies(count = 5):
    movies = Movie.objects.order_by("id")[:count]
    return {"last_movies": movies}
