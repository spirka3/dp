from glob import glob

files = glob('/home/janci/Downloads/*.txt')


for file in files:
    used = []
    with open(file, 'r') as f:
        # check if the file contains the same object in the same frame
        lines = f.readlines()
        for line in lines:
            if len(line.split(' ')) == 10:
                frame, obj, left, top, width, height, conf, x, y, z = line.split()
                fo = f'{frame} {obj}'
                if fo in used:
                    print(f'{file} Frame {frame} is used twice!')
                used.append(fo)

        ...