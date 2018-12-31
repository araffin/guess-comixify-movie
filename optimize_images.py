import os
import subprocess

folder = 'img/'

images = [im for im in os.listdir(folder) if im.endswith('.jpg') or im.endswith('.png')]


HEIGHT = str(675)

for im in images:
    args = [im]
    if im.endswith('.png'):
        out = im.split('.png')[0] + '.jpg'
    else:
        out = im
    args += [out]
    subprocess.call(['convert', '-resize', 'x{}'.format(HEIGHT)] + args, cwd=folder)
    # subprocess.call(['ls'] + args, cwd=folder)
