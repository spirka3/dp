import os
import csv
import json

import darwin.importer as importer
import darwin.exporter as exporter
from glob import glob
from darwin.client import Client
from darwin.exporter import get_exporter
from darwin.importer import get_importer

client = Client.from_api_key('CaMjwSx.no24YD4TW-7huMLygDOhb046DzWC_jXX')
dataset = client.get_remote_dataset(dataset_identifier='chunks-video')

frame_schema = """
    {
        "bounding_box": {
            "h": "@h",
            "w": "@w",
            "x": "@x",
            "y": "@y"
        },
        "keyframe": true
    }
"""

end_schema = """
"interpolate_algorithm": "linear-1.1",
"interpolated": true,
"name": "Ad",
"ranges": [ @range ],
"slot_names": [ "0" ]
}"""

template = ''

files = dataset.fetch_remote_files()
annotation_paths = []

for file in files:
    # if file.status != 'new':
    #     continue
    item_id = file.id
    item_name = file.filename
    chunk = item_name.split('-')[-1]

    if int(chunk) > 9:
        continue

    with open('/home/janci/Downloads/template.json', 'r') as f:
        lines = f.read()
        template = lines.replace('@item_name', item_name).replace('@item_id', str(item_id))

    annotation = '{ "frames": { \n'

    with open(f'/home/janci/Downloads/{item_name}.txt', 'r') as f:
        lines = f.readlines()
        frames = [int(x.split(' ')[0]) for x in lines if len(x.split(' ')) == 10]
        # print(frames)
        # exit()
        bounding_boxs = []
        first_frame = min(frames)
        last_frame = max(frames)
        for line in lines:
            line = line.split(' ')
            if len(line) != 10:
                continue
            frame_number, obj, left, top, w, h = line[:6]
            left, top, w, h, = int(left), int(top), int(w), int(h)
            x, y, w, h = left, top, w, h
            frame = f'"{frame_number}"'
            frame_json = json.loads(frame_schema)
            frame_json['bounding_box']['h'] = h
            frame_json['bounding_box']['w'] = w
            frame_json['bounding_box']['x'] = x
            frame_json['bounding_box']['y'] = y
            bounding_boxs.append(f'{frame}: {json.dumps(frame_json)}')

        for i, b in enumerate(bounding_boxs):
            annotation += b + ',\n'
            if i == len(bounding_boxs) - 1:
                annotation = annotation[:-2] + '},\n'
        annotation += end_schema.replace('@range', f'[{first_frame}, {last_frame}]')
        # print(annotation)

    json_label = template.replace('@annotations', annotation)
    print(json_label)

    with open(f'/home/janci/Downloads/{item_name}.json', 'w') as f:
        f.write(json_label)

    annotation_paths.append(f'/home/janci/Downloads/{item_name}.json')

parser = get_importer('darwin')
importer.import_annotations(dataset, parser, annotation_paths, append=False)


# create csv file with tags
# with open('/home/janci/Downloads/tags.csv', 'w', encoding='UTF8') as f:
#     writer = csv.writer(f)
#     for filename in file_names:
#         row = [f'{filename}.jpg', '2']
#         writer.writerow(row)

# parser = get_importer('csv_tags')
# csv = glob('/home/janci/Downloads/tags.csv')
# importer.import_annotations(dataset, parser, csv, append=False)
