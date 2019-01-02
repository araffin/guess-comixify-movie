import os
import time
import http.client
from pprint import pprint

import tmdbsimple as tmdb
from PyInquirer import prompt, style_from_dict, Token

from generate import Movie, movies_list, generate_movies_json, movies

# Max 5 request per second
RATE = 1 / 5

custom_style_2 = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    #Token.Selected: '',  # default
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})

if not os.path.isfile('.api_key'):
    raise ValueError("You must create a file .api_key with you The Movie DB api key in it")

with open('.api_key', 'r') as fh:
    tmdb.API_KEY = fh.read().strip()

intentions = {
    'Search for a movie': 'search',
    'Generate data.json file': 'generate',
}

intention_prompt = {
    'type': 'list',
    'name': 'intention',
    'message': 'What do you want to do?',
    'choices': list(intentions.keys()),
    'filter': lambda key: intentions[key]
}

intention = prompt(intention_prompt)['intention']

if intention == 'search':
    movie_title_prompt = {
        'type': 'input',
        'name': 'query',
        'message': 'Movie title?',
    }

    query = prompt(movie_title_prompt)['query']

    search = tmdb.Search()
    response = search.movie(query=query, style=custom_style_2)

    results = {}
    for s in search.results:
        results[s['title']] = s['id']

    movie_id_prompt = {
        'type': 'list',
        'name': 'movie_id',
        'message': 'Which one?',
        'choices': list(results.keys()),
        'filter': lambda key: results[key]
    }

    movie_id = prompt(movie_id_prompt)['movie_id']

    movie = tmdb.Movies(movie_id)
    movie_infos = movie.info()


    # TODO: Get ALternative titles + Get Images
    # time.sleep(RATE)
    # connection = http.client.HTTPSConnection("api.themoviedb.org")
    # payload = "{}"
    #
    # connection.request("GET", "/3/movie/{}/alternative_titles?api_key={}".format(movie, tmdb.API_KEY), payload)
    # data = connection.getresponse().read()
    #
    # connection.request("GET", "/3/movie/{}/images?api_key={}".format(movie, tmdb.API_KEY), payload)
    # data = connection.getresponse().read()

    comix_prompt = {
        'type': 'input',
        'name': 'image_path',
        'message': 'Comixified image name?',
    }

    image_path = prompt(comix_prompt)['image_path']
    if not image_path.startswith('img/'):
        image_path = 'img/' + image_path
    if not image_path.endswith('.jpg'):
        image_path += '.jpg'

    names = {
        'en': movie_infos['title'],
        'fr': '',
        'original_title': movie_infos['original_title']
    }

    movie_obj = Movie(
        image_path,
        names,
        id=movie_id,
        poster=movie_infos['poster_path']
    )
    pprint(movie_obj.__dict__)

else:
    generate_movies_json(movies)
