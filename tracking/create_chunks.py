from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from tracking.utils import prepare_dir

ride = '1'  # journey id
src = f'ride-{ride}'

# Replace the filename below.
required_video_file = f'{src}/scenevideo-{ride}.mp4'

frame_duration = 1 / 25

time_ranges = dict()

with open(f'{src}/frames.txt', 'r') as f:
    frames = f.readlines()
    for frame in frames:
        id, start_frame, end_frame = frame.strip().split(' ')
        start_time = int(start_frame) * frame_duration
        end_time = int(end_frame) * frame_duration
        time_ranges[id] = (start_time, end_time)

used_ids = []
video_chunks = []


def find_overlap(id):
    # find recursive overlaps
    used_ids.append(id)
    start_time, end_time = time_ranges[id]

    for id2 in time_ranges:
        if id2 in used_ids:
            continue
        a = 0
        start_time2, end_time2 = time_ranges[id2]
        if id == id2 or id2 in used_ids:
            continue
        elif start_time - a <= start_time2 <= end_time + a:
            return find_overlap(id2)
        elif start_time - a <= end_time2 <= end_time + a:
            return find_overlap(id2)

    return id


for id in time_ranges:
    if id in used_ids:
        continue

    id2 = find_overlap(id)
    start_time, end_time = time_ranges[id]
    start_time2, end_time2 = time_ranges[id2]
    video_chunks.append((id, min(start_time, start_time2), max(end_time, end_time2)))
    # break

dst_dir = prepare_dir(f'{src}/origin-chunks')

for i, chunk in enumerate(video_chunks):
    _, start_time, end_time = chunk
    ffmpeg_extract_subclip(required_video_file, start_time, end_time, targetname=f"{dst_dir}/chunks-1-{i}.mp4")
