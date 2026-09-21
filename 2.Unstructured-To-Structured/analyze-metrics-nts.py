import os
import json
from datetime import datetime

cur_path = f"G:/Mi unidad/doctorado/Pablo Castillo - DOCTORADO/2_soa/8 Prepare scenario/Audio analysis/LocalPython/Prototipo Whisperx_/structured outputs/"

llm_results_path = f"{cur_path}/iteration_results"


scenario = "crmboeing"
debug = False

my_range = ["1","2","3","4","5",""] # "1","2","3","4","5",""
for iteration in my_range:

    ####################################################################################################
    ################################################ NTS ################################################
    ####################################################################################################
    ############ Manual NTS ###########
    unique_manual_skills = [] # Extract all orders
    matching_manual_skills_content = {} # Dictionary to see if LLM orders matched manual ones
    matching_manual_skills_speaker = {} # Dictionary to see if LLM orders matched manual ones
    matching_manual_skills = {} # Dictionary to see if LLM orders matched manual ones
    filename = f"manual_{scenario}.json"
    with open(os.path.join(cur_path, filename), "r") as f:
        data = json.load(f)
        for entry in data:
            if entry["Category"] == "Skill":
                unique_manual_skills.append(entry)
                unique_id = entry["Start"]+"_"+ entry["end"] +"_"+ entry["Task"] 
                matching_manual_skills_content[unique_id] = False
                matching_manual_skills_speaker[unique_id] = False
                matching_manual_skills[unique_id] = False

    ############ LLM NTS ###########
    llm_skills_true_positives_content = 0  # Positive in LLM outcome and also in reality  => In LLM and ref
    llm_skills_false_positives_content = 0 # LLM predicts but it is not in reality        => In LLM but not in ref
    llm_skills_false_negatives_content = 0 # LLM does not predict, but it in reality      => Not in LLM but in ref

    if iteration == "":
        filename = f"skills_merged_{scenario}.json"
    else:
        filename = f"iteration_{iteration}_skills_{scenario}.json"

    ########### Combined ###########
    llm_skills_true_positives = 0  # Positive in LLM outcome and also in reality  => In LLM and ref
    llm_skills_false_positives = 0 # LLM predicts but it is not in reality        => In LLM but not in ref
    llm_skills_false_positives_unknown = 0
    llm_skills_false_negatives = 0 # LLM does not predict, but it in reality      => Not in LLM but in ref

    with open(os.path.join(llm_results_path, filename), "r") as f:
        data = json.load(f)

        for skill in data:
            llm_start_time = float((datetime.strptime(skill["Start"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            llm_stop_time = float((datetime.strptime(skill["Finish"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            task = skill["Task"]
            speaker = task.split(":")[0]
            nts = task.split(":")[1].strip().split("-")[0].strip()
            #print("---------"+speaker+"_"+nts)

            match_found = False
            ############ Iterate manual skills to search match ###########
            for manual_skill in unique_manual_skills:
                manual_start_time = float(manual_skill["Start"])
                manual_stop_time = float(manual_skill["end"])
                manual_speaker = manual_skill["Task"].split(":")[0]
                manual_nts = manual_skill["Task"].split(":")[1].strip()
                #print("\t"+manual_speaker+"_"+manual_nts)

                if (llm_start_time >= manual_start_time and llm_start_time < manual_stop_time) or (llm_stop_time > manual_start_time and llm_stop_time <= manual_stop_time):

                    unique_id = manual_skill["Start"]+"_"+ manual_skill["end"] +"_"+ manual_skill["Task"]

                    # If there is a long manual interval and two intervals detected in LLM,
                    if manual_speaker.lower()+manual_nts.lower() == speaker.lower()+nts.lower(): # and not matching_manual_skills[unique_id]
                        match_found = True
                        #print(f"True positive {manual_speaker}: {llm_start_time}_{llm_stop_time}_{nts} and {manual_start_time}_{manual_stop_time}_{manual_nts}")
                        if not matching_manual_skills[unique_id]:
                            matching_manual_skills[unique_id] = True
                            llm_skills_true_positives = llm_skills_true_positives + 1
                        break

            if match_found == False:
                if debug:
                    print(f"False positive: {llm_start_time}_{llm_stop_time} - {speaker}:{nts}")
                if "Unknown" in speaker or speaker == "":
                    llm_skills_false_positives_unknown = llm_skills_false_positives_unknown + 1
                llm_skills_false_positives = llm_skills_false_positives + 1

    # Check False negatives
    for entry in matching_manual_skills:
        if matching_manual_skills[entry] == False:
            if debug:
                print(f"False negative: {entry}")
            llm_skills_false_negatives = llm_skills_false_negatives + 1
            #print(f"False negative {entry}")

    print("------")
    print(f"{iteration}True positives: {llm_skills_true_positives}")
    print(f"{iteration}False positives: {llm_skills_false_positives} (unk {llm_skills_false_positives_unknown})")
    print(f"{iteration}False negatives: {llm_skills_false_negatives}")
    print(f"Total Manual (TP+FN): {llm_skills_true_positives+llm_skills_false_negatives}")
    print(f"Total LLM (TP+FP): {llm_skills_true_positives+llm_skills_false_positives}")
    print("------")


    ########### Content ###########
    with open(os.path.join(llm_results_path, filename), "r") as f:
        data = json.load(f)

        for skill in data:
            llm_start_time = float((datetime.strptime(skill["Start"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            llm_stop_time = float((datetime.strptime(skill["Finish"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            task = skill["Task"]
            speaker = task.split(":")[0]
            nts = task.split(":")[1].strip().split("-")[0].strip()
            #print("---------"+speaker+"_"+nts)

            content_found = False
            ############ Iterate manual skills to search match ###########
            for manual_skill in unique_manual_skills:
                manual_start_time = float(manual_skill["Start"])
                manual_stop_time = float(manual_skill["end"])
                manual_speaker = manual_skill["Task"].split(":")[0]
                manual_nts = manual_skill["Task"].split(":")[1].strip()
                #print("\t"+manual_speaker+"_"+manual_nts)

                if (llm_start_time >= manual_start_time and llm_start_time < manual_stop_time) or (llm_stop_time > manual_start_time and llm_stop_time <= manual_stop_time):

                    unique_id = manual_skill["Start"]+"_"+ manual_skill["end"] +"_"+ manual_skill["Task"] 

                    if manual_nts.lower() == nts.lower(): # and not matching_manual_skills_content[unique_id]
                        content_found = True
                        #print(f"True positive {participants}: {llm_start_time}_{llm_stop_time} and {manual_start_time}_{manual_stop_time}")
                        if not matching_manual_skills_content[unique_id]:
                            matching_manual_skills_content[unique_id] = True
                            llm_skills_true_positives_content = llm_skills_true_positives_content + 1
                        break

            if content_found == False:
                if debug:
                    print(f"Content False positive: {llm_start_time}_{llm_stop_time} - {nts}")
                llm_skills_false_positives_content = llm_skills_false_positives_content+ 1

    # Check False negatives
    for entry in matching_manual_skills_content:
        if matching_manual_skills_content[entry] == False:
            if debug:
                print(f"False negative: {entry}")
            llm_skills_false_negatives_content = llm_skills_false_negatives_content + 1

    print("------")
    print(f"{iteration}Content True positives: {llm_skills_true_positives_content}")
    print(f"{iteration}Content False positives: {llm_skills_false_positives_content}")
    print(f"{iteration}Content False negatives: {llm_skills_false_negatives_content}")
    print(f"Total Manual (TP+FN): {llm_skills_true_positives_content+llm_skills_false_negatives_content}")
    print(f"Total LLM (TP+FP): {llm_skills_true_positives_content+llm_skills_false_positives_content}")
    print("------")

    ########### Speakers ###########
    llm_skills_true_positives_speaker = 0  # Positive in LLM outcome and also in reality  => In LLM and ref
    llm_skills_false_positives_speaker = 0 # LLM predicts but it is not in reality        => In LLM but not in ref
    llm_skills_false_positives_unknown = 0
    llm_skills_false_negatives_speaker = 0 # LLM does not predict, but it in reality      => Not in LLM but in ref

    with open(os.path.join(llm_results_path, filename), "r") as f:
        data = json.load(f)

        for skill in data:
            llm_start_time = float((datetime.strptime(skill["Start"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            llm_stop_time = float((datetime.strptime(skill["Finish"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            task = skill["Task"]
            speaker = task.split(":")[0]
            nts = task.split(":")[1].strip().split("-")[0].strip()
            #print("---------"+speaker+"_"+nts)

            speaker_found = False
            ############ Iterate manual skills to search match ###########
            for manual_skill in unique_manual_skills:
                manual_start_time = float(manual_skill["Start"])
                manual_stop_time = float(manual_skill["end"])
                manual_speaker = manual_skill["Task"].split(":")[0]
                manual_nts = manual_skill["Task"].split(":")[1].strip()
                #print("\t"+manual_speaker+"_"+manual_nts)

                if (llm_start_time >= manual_start_time and llm_start_time < manual_stop_time) or (llm_stop_time > manual_start_time and llm_stop_time <= manual_stop_time):

                    unique_id = manual_skill["Start"]+"_"+ manual_skill["end"] +"_"+ manual_skill["Task"] 

                    if manual_speaker.lower() == speaker.lower(): # and not matching_manual_skills_speaker[unique_id]
                        speaker_found = True
                        #print(f"Speaker True positive {participants}: {llm_start_time}_{llm_stop_time} and {manual_start_time}_{manual_stop_time}")
                        if not matching_manual_skills_speaker[unique_id]:
                            matching_manual_skills_speaker[unique_id] = True
                            llm_skills_true_positives_speaker = llm_skills_true_positives_speaker + 1
                        break

            if speaker_found == False:
                # if debug:
                #     print(f"Speaker False positive: {llm_start_time}_{llm_stop_time} - {speaker}")
                if "Unknown" in speaker or speaker == "":
                    llm_skills_false_positives_unknown = llm_skills_false_positives_unknown + 1
                llm_skills_false_positives_speaker = llm_skills_false_positives_speaker+ 1

    # Check False negatives
    for entry in matching_manual_skills_speaker:
        if matching_manual_skills_speaker[entry] == False:
            if debug:
                print(f"False negative: {entry}")
            llm_skills_false_negatives_speaker = llm_skills_false_negatives_speaker + 1

    print("------")
    print(f"{iteration}Speaker True positives: {llm_skills_true_positives_speaker}")
    print(f"{iteration}Speaker False positives: {llm_skills_false_positives_speaker} (unk {llm_skills_false_positives_unknown})")
    print(f"{iteration}Speaker False negatives: {llm_skills_false_negatives_speaker}")
    print(f"Total Manual (TP+FN): {llm_skills_true_positives_speaker+llm_skills_false_negatives_speaker}")
    print(f"Total LLM (TP+FP): {llm_skills_true_positives_speaker+llm_skills_false_positives_speaker}")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

