from rest_framework import serializers
from movie.models import Movie, Reviews

class MovieListSerializer(serializers.ModelSerializer):
    
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')

class FilterReviewListSerializer(serializers.ListSerializer):
    """ ancaq perent komentariyalari cixarmaq ucun """
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class RecursiveSerializers(serializers.Serializer):
    """ review icinde review cixarmaq ucun """
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class ReviewSerializer(serializers.ModelSerializer):
    
    children = RecursiveSerializers(many=True)
 
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Reviews
        fields = ('name', 'text', 'children')


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ('movie', 'parent', 'email', 'name', 'text')
        movie = serializers.SlugRelatedField(slug_field="name", read_only=True)
        parent = serializers.SlugRelatedField(slug_field="name", read_only=True)


class MovieDetailSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    # asagidakini yaza bilmeyimiz ucun Reviews modelinde reviews adli related_name olmasi shertdi
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)