from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    like = serializers.StringRelatedField(many=True)

    def get_movie(self, obj):
        return obj.movie.title
    
    def get_user(self, obj):
        return obj.user.user_name

    class Meta:
        model = Review
        fields = "__all__"


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("content","rating",)

