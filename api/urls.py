from django.urls import path, include
from .views import MovieApiView, MovieApiDetail, ReviewCreateView, ReviewApiView

urlpatterns = [
    path('', MovieApiView.as_view()),
    path('<int:pk>/', MovieApiDetail.as_view()),
    path('reviews/', ReviewCreateView.as_view()),

    # bu asagidaki url-e mueyyen menada ehtiyac yoxdu, cunki detail review-de gormek olar reveiw-leri
    path('all_reviews/', ReviewApiView.as_view()),
]