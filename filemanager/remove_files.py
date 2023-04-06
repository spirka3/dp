import os
import shutil

src_dir = f'/home/janci/PycharmProjects/python-scripts/tobii/1/OBJECTS'

for i in range(1, 59):
    # for j in range(9):
        # os remove dir
    # os.rmdir(src_dir + f'/object-{i}/driver-{j}')
    # os.rmdir(src_dir + f'/{i}/labels')
    # os.rmdir(src_dir + f'/{i}/images')
    shutil.rmtree(src_dir + f'/{i}/labels', ignore_errors=True)
    shutil.rmtree(src_dir + f'/{i}/images', ignore_errors=True)
