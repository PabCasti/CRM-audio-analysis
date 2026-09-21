# Activar proyecto con whisperx:
#     Abrir Anaconda Prompt
#     >> cd  "G:\Mi unidad\doctorado\Pablo Castillo - DOCTORADO\2_soa\10 Paper NTS"
#     >> G:
#     >> conda activate whisperx-web-ui & python 1.0.code_detectAudio.py

import json
import os
from datetime import datetime

folder = "1. cardiac"
scenario = "cardiac"
iteration = 1

file_prefix = "orders_"+scenario
file_prefix2 = "skills_"+scenario


cur_path = f"G:/Mi unidad/doctorado/Pablo Castillo - DOCTORADO/2_soa/8 Prepare scenario/Audio analysis/LocalPython/Prototipo Whisperx_/structured outputs/{folder}/"


############ Orders ############

# Merge all unique orders
unique_orders = {}

filename = f"{file_prefix}{iteration}.json"
with open(os.path.join(cur_path, filename), "r") as f:
    data = json.load(f)
    for order in data.get("ordersTimeline", []):
        start_ts = order.get("start_timestamp")
        if start_ts not in unique_orders:
            unique_orders[start_ts] = order

# Result: merged list with unique start_timestamps
merged_orders = list(unique_orders.values())


timelineList = []
for orderBlock in merged_orders:
    stop_time = orderBlock['stop_timestamp']
    start_time = orderBlock['start_timestamp'] 
    if stop_time == "None":
        stop_time = float(start_time) + 1.0
    stop_time = datetime.utcfromtimestamp(stop_time).strftime('%Y-%m-%d %H:%M:%S.%f')
    start_time = datetime.utcfromtimestamp(orderBlock['start_timestamp']).strftime('%Y-%m-%d %H:%M:%S.%f')

    leader = orderBlock['leader']['name']
    follower = orderBlock['follower']
    # if leader == "":
    #     leader = orderBlock['leader']['speaker_id']
    if follower != "None" and follower != "" and follower != None:
        if 'name' not in orderBlock['follower']:
            follower = orderBlock['follower']['speaker_id']
        follower = orderBlock['follower']['name']
    if follower == "None" or follower == "" or follower == None:
        follower = "Unknown"
    actionText = leader + " to " + str(follower) + ": " + orderBlock['action'] 
    timelineList.append(actionText)




# Optionally save to a new file
with open(f"simplified_iteration_{iteration}_orders_{scenario}.json", "w") as f:
    json.dump(timelineList, f, indent=2)




############ Skills ############

# Merge all unique skills
unique_skills = {}
filename = f"{file_prefix2}{iteration}.json"
with open(os.path.join(cur_path, filename), "r") as f:
    data = json.load(f)
    for order in data.get("skillsTimeline", []):
        start_ts = order.get("start_timestamp")
        if start_ts not in unique_skills:
            unique_skills[start_ts] = order

# Result: merged list with unique start_timestamps
merged_skills = list(unique_skills.values())

timelineList = []
for skillBlock in merged_skills:
    start_time = datetime.utcfromtimestamp(skillBlock['start_timestamp']).strftime('%Y-%m-%d %H:%M:%S.%f')
    stop_time = datetime.utcfromtimestamp(skillBlock['stop_timestamp']).strftime('%Y-%m-%d %H:%M:%S.%f')
    speaker_name = skillBlock['speaker']['name']
    if speaker_name == "None" or speaker_name == "" or speaker_name == None:
        speaker_name = "Unknown"
    actionText = speaker_name + ": " + skillBlock['main_skill'] + " - "+ skillBlock['skill_description'] 
    timelineList.append(actionText)


# Optionally save to a new file
with open(f"simplified_iteration_{iteration}_skills_{scenario}.json", "w") as f:
    json.dump(timelineList, f, indent=2)





print(len(merged_orders))

print(len(merged_skills))