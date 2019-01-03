import os
import time
import json
import http.client
from pprint import pprint

import tmdbsimple as tmdb
from PyInquirer import prompt, style_from_dict, Token

from generate import Movie, write_movies_json, movies_list, load_movies

# Max 5 request per second
# in fact 40 request every 10 seconds
RATE = 1 / 5
LANGUAGES = ['en', 'fr', 'es']

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

def get_movie_infos(movie_id):
    movie = tmdb.Movies(movie_id)
    names, posters = {}, {}
    for lang in LANGUAGES:
        movie_infos = movie.info(language=lang)
        names[lang] = movie_infos['title']
        posters[lang] = movie_infos['poster_path']
        names['original_title'] = movie_infos['original_title']
        time.sleep(RATE)

    return names, posters, movie_infos['original_language']

intentions = {
    'Search for a movie': 'search',
    'Call The Movie DB api': 'call',
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
    movies = load_movies()
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

    names, posters, lang = get_movie_infos(movie_id)

    # Get ALternative titles + Get Images
    # movie.alternative_titles()
    # time.sleep(RATE)
    # movie.images()

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

    movie_obj = Movie(
        image_path,
        id=movie_id,
        names=names,
        posters=posters,
        lang=lang
    )
    pprint(movie_obj.__dict__)
    movies['movies'].append(movie_obj.__dict__)
    write_movies_json(movies)

elif intention == 'call':
    movies = []
    for idx in range(len(movies_list)):
        image_path, movie_id = movies_list[idx]
        print(idx, image_path)

        names, posters, lang = get_movie_infos(movie_id)

        movie_dict = Movie(
            image_path,
            id=movie_id,
            names=names,
            posters=posters,
            lang=lang
        ).__dict__
        movies.append(movie_dict)

    write_movies_json(movies)
