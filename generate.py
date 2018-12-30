import json


class Movie(object):
    def __init__(self, image, names, id=None, poster=''):
        super(Movie, self).__init__()
        self.image = image
        if isinstance(names, str):
            names = [names]
        self.names = names
        self.id = id
        self.poster = poster

# https://www.themoviedb.org/movie/id-name
# movie names: en, fr
movies = [
            [
                'img/0.jpg', 'Apocalypse Now',
                28, 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/5MMY5V8JCjiRhtdepjWgNTYyOZl.jpg'
            ],
            [
                'img/1.jpg', ['Star Wars', 'La Guerre des étoiles'],
                11, 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/yVaQ34IvVDAZAWxScNdeIkaepDq.jpg'
            ],
            [
                'img/2.png', ['The Visitors', 'Les Visiteurs'],
                11687, 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/ad3mSN89aBh5e057y402FOPAg0X.jpg'
            ],
            [
                'img/3.png', ['Dead Poets Society', 'Le Cercle des poètes disparus'],
                 207, 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/mNhThFspwKfFe98zggChX6OqQE3.jpg'
            ],
            [
                'img/4.png', ['Crooks in Clover', 'Les tontons flingueurs'],
                 25253, 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/dqYig2GxgICQdK3KTS7f8yPl4Pm.jpg'
            ],
            [
                'img/5.png', 'Deadpool',
                 293660, 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/eJyRzC5uFjQryu8Hm61yqtrzj4S.jpg'
            ],
            [
                'img/6.png', 'Baby Driver',
                 339403, 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/oTsgNy2XsO50PhpB8u5RRusfkjV.jpg'
            ],
        ]


data = {'movies': [Movie(*movie).__dict__ for movie in movies]}

with open('data.json', 'w') as fh:
    json.dump(data, fh)
