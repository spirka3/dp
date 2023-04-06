import shutil
import glob

""""
Create a copy of images with labels to match the pair of image|label
"""

prev = [12, 25, 27, 49, 99]
curr = [10, 23, 25, 48, 49]
# convert to string
prev = [str(i) for i in prev]
curr = [str(i) for i in curr]

ride = 6

src = f'/home/janci/PycharmProjects/python-scripts/tobii'
src_dir = f'{src}/{ride}/manual/'

paths_ref = sorted(glob.glob(src_dir + f'*.jpg'))

# array of 0-56
for path in paths_ref:
    filename = path.split('/')[-1].split('.')[0]
    obj, driver, frame = filename.split('_')
    try:
        find_index = prev.index(obj)
        rpr = curr[find_index]
    except:
        continue
    new_fn = f'{rpr}_{driver}_{frame}'
    # copy image
    src = src_dir + filename + '.jpg'
    dst = src_dir + new_fn + '.jpg'
    shutil.move(src, dst)
