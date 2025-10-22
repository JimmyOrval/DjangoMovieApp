from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import CreateMovieForm
from .models import Movie
from django.shortcuts import get_object_or_404, redirect

def index(request):
	return render(request,'index.html')

def get_movies(request):
    movies = Movie.objects.all()
    return render(request, 'get_movies.html', {'movies': movies})
	
def show_movie_details(request, movie_id):
    movie = get_object_or_404(Movie, Movie_id=movie_id)
    return render(request, 'show_movie_details.html', {'movie': movie})
	
def add_movie(request):
    if request.method == 'POST':
        form = CreateMovieForm(request.POST)
        if form.is_valid():
            movie_data = form.cleaned_data
            movie_id = movie_data['Movie_id']
            movie_name = movie_data['Movie_name']
            movie_rating = movie_data['Movie_rating']
            movie_year = movie_data['Movie_year']
            movie_genre = movie_data['Movie_genre']
            Movie.objects.create(
                Movie_id=movie_id,
                Movie_name=movie_name,
                Movie_rating=movie_rating,
                Movie_year=movie_year,
                Movie_genre=movie_genre
            )
            return render(request, 'index.html')
    else:
        form = CreateMovieForm()
    return render(request, 'add_movie.html', {'form': form})
		
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, Movie_id=movie_id)
    if request.method == 'POST':
        form = CreateMovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('show_movie_details', movie_id=movie_id)
    else:
        form = CreateMovieForm(instance=movie)
    return render(request, 'update_movie.html', {'form': form, 'movie': movie})
		
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, Movie_id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'delete_movie.html', {'movie': movie})