import glob
import shutil
import os

src_dir = '/home/janci/PycharmProjects/python-scripts/tobii'
dst_dir = '/home/janci/PycharmProjects/python-scripts/tobii'

for i in [0, 1, 2, 3, 4, 6]:

    arr = [str(i) for i in range(58)]
    arr2 = ['03', '08', '014']
    arr = arr + arr2

    for j in range(57):
        paths_ref = sorted(glob.glob(src_dir + f'/{i}/OBJECTS/{j}/*.jpg'))

        for path in paths_ref:
            filename = path.split('/')[-1][:-4]
            obj = filename.split('_')[0]
            try:
                src = src_dir + f'/{i}/OBJECTS/{j}/' + filename + '.jpg'
                # if folder not exist, create it
                if not os.path.isdir(dst_dir + f'/objects-total/{obj}'):
                    os.makedirs(dst_dir + f'/objects-total/{obj}')
                dst = dst_dir + f'/objects-total/{obj}/' + filename + '.jpg'
                print(src, dst)
                shutil.copy(src, dst)
            except:
                print('err', filename)
