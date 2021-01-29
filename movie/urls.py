from django.urls import path, include
from .views import MoviesView, MovieDetailView, AddReview, ActorDetailView, FilterMoviesView, JsonFilterMoviesView, AddStarRating

urlpatterns = [
    path('', MoviesView.as_view(), name='movie-list'),
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", JsonFilterMoviesView.as_view(), name='json_filter'),
    path('movie/<slug:slug>/', MovieDetailView.as_view(), name='movie-detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add-review'),
    path('actor/<str:slug>/', ActorDetailView.as_view(), name='actor-detail'),
]