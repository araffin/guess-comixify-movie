import json


class Movie(object):
    def __init__(self, image, names, id=None):
        super(Movie, self).__init__()
        self.image = image
        if isinstance(names, str):
            names = [names]
        self.names = names
        self.id = id

# https://www.themoviedb.org/movie/id-name

movies = [
            [
                'img/0.jpg', 'Apocalypse Now',
                28
            ],
            [
                'img/1.jpg', ['La Guerre des étoiles', 'Star Wars'],
                11
            ],
            [
                'img/2.png', ['Les Visiteurs', 'The Visitors'],
                11687
            ],
            [
                'img/3.png', ['Le Cercle des poètes disparus', 'Dead Poets Society'],
                 207
            ],
            [
                'img/4.png', ['Les tontons flingueurs', 'Crooks in Clover'],
                 25253
            ],
            [
                'img/5.png', 'Deadpool',
                 293660
            ],
            [
                'img/6.png', 'Baby Driver',
                 339403
            ],
        ]


data = {'movies': [Movie(*movie).__dict__ for movie in movies]}

with open('data.json', 'w') as fh:
    json.dump(data, fh)
