import os

s = '/home/janci/PycharmProjects/python-scripts/tobii/objects-total'

for i in range(60):
    os.makedirs(f'{s}/object-{i}', exist_ok=True)
    for j in range(9):
        os.makedirs(f'{s}/object-{i}/driver-{j}', exist_ok=True)
