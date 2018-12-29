import json


class Movie(object):
    """docstring for Movie."""
    def __init__(self, image, names, url=''):
        super(Movie, self).__init__()
        self.image = image
        if isinstance(names, str):
            names = [names]
        self.names = names
        self.url = url

movies = [
            [
                'img/0.jpg', 'Apocalypse Now',
                'https://www.themoviedb.org/movie/28-apocalypse-now'
            ],
            [
                'img/1.jpg', ['La Guerre des étoiles', 'Star Wars'],
                'https://www.themoviedb.org/movie/11-star-wars'
            ],
            [
                'img/2.png', 'Les Visiteurs',
                'https://www.themoviedb.org/movie/11687-les-visiteurs'
            ],
        ]


data = {'movies': [Movie(*movie).__dict__ for movie in movies]}

with open('data.json', 'w') as fh:
    json.dump(data, fh)
