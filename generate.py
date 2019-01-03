import json


class Movie(object):
    def __init__(self, image, id, *, names, posters, lang):
        super(Movie, self).__init__()
        self.image = image
        self.names = names
        self.id = id
        self.posters = posters
        self.lang = lang

# https://www.themoviedb.org/movie/id-name
# movie names: en, fr
movies_list = [
            [
                'img/0.jpg',
                28,
            ],
            [
                'img/1.jpg',
                1891,
            ],
            [
                'img/2.jpg',
                11687
            ],
            [
                'img/3.jpg',
                 207
            ],
            [
                'img/4.jpg',
                 25253
            ],
            [
                'img/5.jpg',
                 293660,
            ],
            [
                'img/6.jpg',
                 339403,
            ],
            [
                'img/bon.jpg',
                 429
            ],
            [
                'img/chute.jpg',
                 613,
            ],
            [
                'img/full.jpg',
                 600,
            ],
            [
                'img/grand.jpg',
                 120467,
            ],
            [
                'img/harry_2.jpg',
                 672,
            ],
            [
                'img/harry_7.jpg',
                 12445,
            ],
            [
                'img/lala.jpg',
                 313369,
            ],
            [
                'img/leeloo.jpg',
                 18,
            ],
            [
                'img/mad.jpg',
                 76341,
            ],
            [
                'img/nouveaux.jpg',
                 265195,
            ],
            [
                'img/lord.jpg',
                 121,
            ],
            [
                'img/now.jpg',
                 291805,
            ],
            [
                'img/ny.jpg',
                 198277,
            ],
            [
                'img/padrino.jpg',
                 238,
            ],
            [
                'img/pulp.jpg',
                 680,
            ],
            [
                'img/shining.jpg',
                 694,
            ],
            [
                'img/sparte.jpg',
                 1271,
            ],
            [
                'img/oss.jpg',
                 15588,
            ],
            [
                'img/pod.jpg',
                 1893,
            ],
            [
                'img/up.jpg',
                 14160,
            ],
            [
                'img/west.jpg',
                 1725,
            ],
        ]


def load_movies():
    movies = None
    with open('data.json', 'r') as fh:
        movies = json.load(fh)
    return movies

def write_movies_json(movies):
    print("{} movies".format(len(movies)))

    data = {'movies': movies}

    with open('data.json', 'w') as fh:
        json.dump(data, fh, indent=4, sort_keys=True)
