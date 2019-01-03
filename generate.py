import json


class Movie(object):
    def __init__(self, image, id, *, names, posters, lang):
        super(Movie, self).__init__()
        self.image = image
        self.names = names
        self.id = id
        self.posters = posters
        self.lang = lang

# Use to add movies in a batch
movies_list = [
            # [
            #     'img/0.jpg', 28,
            # ],
]


def load_movies():
    movies = None
    with open('data.json', 'r') as fh:
        movies = json.load(fh)['movies']
    return movies

def write_movies_json(movies):
    print("{} movies".format(len(movies)))

    data = {'movies': movies}

    with open('data.json', 'w') as fh:
        json.dump(data, fh, indent=4, sort_keys=True)
