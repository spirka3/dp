import glob
import shutil

RIDE = '1'
PATH = f'/home/janci/Documents/DIPLO/PILOT/{RIDE} David Brandys'

paths = sorted(glob.glob(f'{PATH}/images/*.jpg'))

n = 20

# for i in range(n):
#     os.mkdir(f'{PATH}/{i}')
#     os.mkdir(f'{PATH}/{i}/images')
#     os.mkdir(f'{PATH}/{i}/labels')


def split_list(alist, wanted_parts=1):
    length = len(alist)
    for i in range(wanted_parts):
        return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]]


parts = split_list(paths, wanted_parts=20)

for i, paths in enumerate(parts):
    for path in paths:
        filename = path.split('/')[-1][:-4]
        # copy image
        src = PATH + '/images/' + filename + '.jpg'
        dst = PATH + f'/{i}/images/' + filename + '.jpg'
        shutil.copy(src, dst)
        # copy label
        src = PATH + '/labels/' + filename + '.txt'
        dst = PATH + f'/{i}/labels/' + filename + '.txt'
        shutil.copy(src, dst)
