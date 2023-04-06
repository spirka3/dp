import os

from tracking.utils import prepare_dir

mots = os.listdir('MOTCUSTOM/test')
print(mots)

for mot in mots:
    chunk = mot[-1]
    prepare_dir(f'ride-1/checker/chunks-1-{chunk}/labels')
    gt = os.path.join('MOTCUSTOM/test', mot, 'gt/gt.txt')
    with open(gt, 'r') as f:
        lines = f.readlines()
        # print(lines)
        for line in lines:
            frame, obj, left, top, width, height, conf, x, y, z = line.split()
            left = int(left)
            top = int(top)
            width = int(width)
            height = int(height)
            x, y, w, h = left + width/2, top + height/2, width, height
            x, y, w, h = x / 1920, y / 1080, w / 1920, h / 1080
            with open(f'ride-1/checker/chunks-1-{chunk}/labels/{frame.zfill(6)}.txt', 'a') as l:
                l.write(f'{obj} {x} {y} {w} {h}')
            print(line)
    print('---')
