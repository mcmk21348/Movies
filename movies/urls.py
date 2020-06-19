from django.urls import path

from . import views

urlpatterns = [
    # path('', views.MovieView.as_view()),
    path('filter/', views.FilterMovieView.as_view(), name='filter'),
    path('search/', views.Search.as_view(), name='search'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path('serial/', views.SerialView.as_view(), name='serial_page'),
    path("serial/<int:pk>", views.SerialDetailView.as_view(), name='serial-page'),
    path('film/', views.MovieView.as_view(), name='film_page'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name='movie_detail'),
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_review'),
    path("", views.MovieView1.as_view(), name='index_page'),

]