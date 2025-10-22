from django.forms import ModelForm
from .models import Movie


class CreateMovieForm(ModelForm):
	class Meta:
		model = Movie
		fields = ['Movie_id', 'Movie_name', 'Movie_rating', 'Movie_year', 'Movie_genre']