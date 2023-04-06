import glob
import shutil
import os

src_dir = '/home/janci/PycharmProjects/python-scripts/tobii'
dst_dir = '/home/janci/PycharmProjects/python-scripts/tobii'

ads = dict()


arr = [str(i) for i in range(57)]
arr2 = ['03', '08', '014']
arr = arr + arr2


for a in arr:
    ads[a] = dict()

    for d in range(7):
        ads[a][str(d)] = 0

print(ads)

for a in arr:
    paths_ref = sorted(glob.glob(src_dir + f'/objects-seen/{a}/*.jpg'))

    for path in paths_ref:
        filename = path.split('/')[-1][:-4]
        # print(filename)
        obj, driver, _ = filename.split('_')
        # if driver == '0':
        ads[a][driver] += 1

ms = 1 / 25

categories = dict()
categories['none'] = []
categories['short'] = []
categories['medium'] = []
categories['long'] = []
categories_d = dict()
categories_d['none'] = 0
categories_d['short'] = 0
categories_d['medium'] = 0
categories_d['long'] = 0

tt = []

print(15 * ms)

for a in ads:
    driver = []
    seen = 0
    total_seen = 0
    for d in ads[a]:
        if ads[a][d] > 0:
            seen += 1
            driver.append(d)
        total_seen += ads[a][d]

    if seen == 0:
        categories['none'].append(a)
        print('-')
    else:
        if total_seen/seen * ms >= 0.6:
            categories['long'].append(a)
            categories_d['long'] += len(driver)
            print('long')
        elif total_seen/seen * ms >= 0.3:
            categories['medium'].append(a)
            categories_d['medium'] += len(driver)
            print('medium')
        else:
            categories['short'].append(a)
            categories_d['short'] += len(driver)
            print('short')

    # if seen > 0:
    #     tt.append(total_seen / seen * ms)
        # print(total_seen / seen * ms)

# print(max(tt))

# for a in ads:
    # print(a, ads[a])

for c in categories.keys():
    if c == 'none':
        continue
    elif c == 'short':
        t = '1-28ms'
    elif c == 'medium':
        t = '29-60ms'
    elif c == 'long':
        t = '61+ ms'
    print(c,  categories_d[c]/len(categories[c]))

print(sum(categories_d.values()))
