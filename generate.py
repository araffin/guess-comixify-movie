import json


class Movie(object):
    def __init__(self, image, names=None, id=None, poster='', names_dict=None):
        super(Movie, self).__init__()
        self.image = image

        if isinstance(names, str):
            names = [names]

        if isinstance(names, list):
            names_dict = {
                'en': names[0]
            }
            if len(names) > 1:
                names_dict['fr'] = names[1]
            if len(names) == 3:
                names_dict['original_title'] = names[2]
            else:
                names_dict['original_title'] = ''

        if names_dict is not None:
            names = list(names_dict.values())

        self.names = names
        self.names_dict = names_dict
        self.id = id
        self.poster = poster

# https://www.themoviedb.org/movie/id-name
# movie names: en, fr
movies_list = [
            [
                'img/0.jpg', 'Apocalypse Now',
                28, '5MMY5V8JCjiRhtdepjWgNTYyOZl.jpg'
            ],
            [
                'img/1.jpg', ['The Empire Strikes Back', 'L\'Empire contre-attaque'],
                1891, 'nqY9dJeRaSEJlmljOpPA5Tc9moQ.jpg'
            ],
            [
                'img/2.jpg', ['The Visitors', 'Les Visiteurs'],
                11687, 'ad3mSN89aBh5e057y402FOPAg0X.jpg'
            ],
            [
                'img/3.jpg', ['Dead Poets Society', 'Le Cercle des poètes disparus'],
                 207, 'mNhThFspwKfFe98zggChX6OqQE3.jpg'
            ],
            [
                'img/4.jpg', ['Crooks in Clover', 'Les tontons flingueurs'],
                 25253, 'dqYig2GxgICQdK3KTS7f8yPl4Pm.jpg'
            ],
            [
                'img/5.jpg', 'Deadpool',
                 293660, 'eJyRzC5uFjQryu8Hm61yqtrzj4S.jpg'
            ],
            [
                'img/6.jpg', 'Baby Driver',
                 339403, 'oTsgNy2XsO50PhpB8u5RRusfkjV.jpg'
            ],
            [
                'img/bon.jpg', ['The Good, the Bad and the Ugly ', 'Le Bon, la Brute et le Truand', 'Il buono, il brutto, il cattivo'],
                 429, 'wfPHdfofBD5PN96dV96a51B3Ja2.jpg'
            ],
            [
                'img/chute.jpg', ['Downfall', 'La Chute', 'Der Untergang'],
                 613, '1PeyCJmWl9G3zGJpvUddausqKuM.jpg'
            ],
            [
                'img/full.jpg', 'Full Metal Jacket',
                 600, 'wNImUY185y8cCEHNJeXgsdB0rC.jpg'
            ],
            [
                'img/grand.jpg', 'The Grand Budapest Hotel',
                 120467, 'gPZ6dO8cKCahCjJJvk5UhUBTJ9N.jpg'
            ],
            [
                'img/harry_2.jpg', ['Harry Potter and the Chamber of Secrets', 'Harry Potter et la Chambre des Secrets'],
                 672, 'ygsu82q2YSrIdePnM2GLGjsFFjr.jpg'
            ],
            [
                'img/harry_7.jpg', ['Harry Potter and the Deathly Hallows', 'Harry Potter et les Reliques de la Mort'],
                 12445, '4gf2Px4oHJld9ASKLGUO1Fpots1.jpg'
            ],
            [
                'img/lala.jpg', 'La La Land',
                 313369, '5KIj6aioW1UtUT1IV0qqW5iZbNH.jpg'
            ],
            [
                'img/leeloo.jpg', ['The Fifth Element', 'Le Cinquième Élément', 'Le 5eme Élément'],
                 313369, '8nx8sttha1Zidt73SbNncVfSwqk.jpg'
            ],
            [
                'img/mad.jpg', 'Mad Max: Fury Road',
                 76341, 'oLy2V6AWSEfdPgKOtrSGnwB3Q2R.jpg'
            ],
            [
                'img/nouveaux.jpg', ['Wild Tales', 'Les Nouveaux Sauvages', 'Relatos salvajes'],
                 265195, 'ohpEgwbU4msY7YnRx6vsJVJPajp.jpg'
            ],
            [
                'img/lord.jpg', ['The Lord of the Rings: The Two Towers', 'Le Seigneur des anneaux : Les Deux Tours'],
                 121, '7RLrUQH2qnCw4To5nVwRAdywGVy.jpg'
            ],
            [
                'img/now.jpg', ['Now You See Me 2', 'Insaisissables 2'],
                 291805, 'hKWFfyRIrUUmdEPqWTDKeK9szsv.jpg'
            ],
            [
                'img/ny.jpg', ['Begin Again', 'New York Melody'],
                 198277, '9B60RUP0Fz7ocR5Lf6Afi1zOfJP.jpg'
            ],
            [
                'img/padrino.jpg', ['The Godfather', 'Le Parrain'],
                 238, 'j0O2PYvV2INW64jmTc4e5IVqQsz.jpg'
            ],
            [
                'img/pulp.jpg', ['Pulp Fiction'],
                 680, '7p8x4U3o3p1JZMBqNY3zAlobY3m.jpg'
            ],
            [
                'img/shining.jpg', ['The Shining', 'Shining'],
                 694, 'lCVa5zPmAZmzoEXJTyGKSuiW1H9.jpg'
            ],
            [
                'img/sparte.jpg', '300',
                 1271, 'nKQqh6kJvPdpOJD24enD3Bm1Hy5.jpg'
            ],
            [
                'img/oss.jpg', ['OSS 117: Lost in Rio', 'OSS 117 : Rio ne répond plus'],
                 15588, 'bCrDUHGcncm51H21AyEyBN13W4t.jpg'
            ],
            [
                'img/pod.jpg', ['The Phantom Menace', 'La Menace fantôme'],
                 1893, 'etnrgeks0Al3wSo44Ji6xgaLBAW.jpg'
            ],
            [
                'img/up.jpg', ['Up', 'Là-haut'],
                 14160, 'fhPsHld7wU1JlgnTZTFBVuF0Dq6.jpg'
            ],
            [
                'img/west.jpg', 'West Side Story',
                 1725, 'lZ7CR15ZAQnpFUTIXh1rR44i0Jy.jpg'
            ],
        ]

movies = [Movie(*movie).__dict__ for movie in movies_list]

def generate_movies_json(movies):
    print("{} movies".format(len(movies)))

    data = {'movies': movies}

    with open('data.json', 'w') as fh:
        json.dump(data, fh)


if __name__ == '__main__':
    generate_movies_json(movies)
