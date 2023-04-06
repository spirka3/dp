import os

objects = [str(x) for x in range(0, 57)]
objects.extend(['03', '08', '014'])

time_ranges = dict()

for obj in objects:
    files = os.listdir(f'1/OBJECTS/{obj}')
    for file in files:
        n, d, f = file.split('_')
        f = f[:-4]
        if obj not in time_ranges.keys():
            time_ranges[obj] = []
        time_ranges[obj].append(f)

for obj in time_ranges:
    print(obj, min(time_ranges[obj]), max(time_ranges[obj]))
