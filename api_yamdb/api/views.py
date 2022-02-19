from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .filters import TitleFilter
from .permissions import AdminsOrReadOnly, AuthorOrModeratorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleListSerializer, TitleSerializer)
from reviews.models import Category, Comment, Genre, Review, Title


class DictViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = PageNumberPagination
    permission_classes = (AdminsOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'


class CategoryViewSet(
    DictViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('slug', 'name')


class GenreViewSet(DictViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = (AdminsOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_queryset = Review.objects.select_related(
            'title').filter(title__id=title_id)
        return review_queryset.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AuthorOrModeratorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        comments_queryset = Comment.objects.select_related(
            'review',
            'review__title',
        ).filter(
            review__id=review_id,
            review__title__id=title_id,
        )
        return comments_queryset.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review_queryset = Review.objects.select_related(
            'title').filter(id=review_id, title__id=title_id)
        review = get_object_or_404(review_queryset)
        serializer.save(author=self.request.user, review=review)
