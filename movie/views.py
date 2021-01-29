from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render

from django.views.generic import View, ListView, DetailView

from .models import Actor, Category, Movie, Genre

from .forms import ReviewForm, RatingForm, Rating

# normalni methoddu get_context_data-ya alternativdi
# bu data-lara her yerde catmaq olar
class GenreYears:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False)

# class MoviesView(View):

#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movie.html", {'movie_list': movies})

# yuxaridaki da ishleyir
class MoviesView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    
    # default olaraq bu view movie_list.html faylini axtarir
    # eger baqda ad template isteyirikse asagidaki kimi qeyd edirik
    # hetta temp. papkasinin icindeki papkada modelin adi ile eyni olmalidi
    # template_name = 'movie/movie_list.html'

    # bu, headerde yazmaqla ana sehifede cixarir categoriyalari, amma detailde cixarmir
    # gerek bunu her yerde yazaq, bu da dry-ya uygun deyil, tag-den istifade edeceyik
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["categories"] = Category.objects.all()
    #     return context


# class MovieDetailView(View):

#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, "movies/movie-detail.html", {'movie': movie})

# yuxaridaki da ishleyir
class MovieDetailView(GenreYears, DetailView):
    model = Movie
    slug_field = "url"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["star_form"] = RatingForm()
        return context

    # asagidaki setre ehtiyac yoxdu, cunki default olara _detail.html-i acir
    # template_name = 'movie/movie-detail.html'

class AddReview(View):
    def post(self, request, pk):
        # print(request.POST)
        movie = Movie.objects.get(id=pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            # modelin movie adli fild-i var, _id yazmaqla review-in hansi movie-ya aid oldugunu deyirik
            # form.movie_id = pk
            # yuxaridaki da asagidaki da eyni seydi, ishleyirler
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorDetailView(GenreYears, DetailView):
    model = Actor
    template_name = 'movie/actor.html'

    # modelde slug field qeyd etmemisem, amma movcud olan name field-ni slug kimi istifade ede bilirem
    slug_field = "name"


class FilterMoviesView(GenreYears, ListView):

    def get_queryset(self):

        # comente aldigim code 2 filter her ikisi odendikde ishleyir, birini doldurmayanda ishlemir
        # queryset = Movie.objects.filter(genres__in=self.request.GET.getlist('genre'), year__in=self.request.GET.getlist('year')) 
         
        queryset = Movie.objects.filter(
            Q(genres__in=self.request.GET.getlist('genre')) | 
            Q(year__in=self.request.GET.getlist('year')))
        return queryset

class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "image")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)

class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)