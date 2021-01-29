from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from movie.models import Movie, Reviews
from .serializers import MovieListSerializer
# Create your views here.

from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, ReviewSerializer

class MovieApiView(APIView):
    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

class MovieApiDetail(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie, many=False)
        return Response(serializer.data)

class ReviewApiView(APIView):
    def get(self, request):
        reviews = Reviews.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ReviewCreateView(APIView):
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)