from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Category, Actor, Genre, Rating, Reviews, Serials
from .forms import ReviewForm, RatingForm



class GenreYear():
    """Жанры и года"""
    def get_genres(self):
        return Genre.objects.all()


    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class MovieView1(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/base.html"





class SerialView(GenreYear, View):
    """Список сериалов"""
    def get(self, request):
        serials = Serials.objects.all()
        return render(request, 'movies/serials.html', {'serial_list': serials})


class SerialDetailView(DetailView):
    """Полное описание сериала"""
    def get(self, request, pk):
        serial = Serials.objects.get(id=pk)
        return render(request, 'movies/serial_detail.html', {'serial': serial})

class MovieView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movie_list.html"
    paginate_by = 2



class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["form"] = ReviewForm()
        return context






class AddReview(View):
    """Отзывы"""
    def post(self, requset, pk):
        form = ReviewForm(requset.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if requset.POST.get("parent", None):
                form.parent_id = int(requset.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())



class FilterMovieView(GenreYear, ListView):
    """фильтр фильмов"""
    paginate_by = 1
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genre__in=self.request.GET.getlist("genre"))
                                        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context




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



class Search(ListView):
    model = Movie
    template_name = 'search_results.html'

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        object_list = Movie.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return object_list


