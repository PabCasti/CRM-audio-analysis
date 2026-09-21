import os
import json
from datetime import datetime

cur_path = f"G:/Mi unidad/doctorado/Pablo Castillo - DOCTORADO/2_soa/8 Prepare scenario/Audio analysis/LocalPython/Prototipo Whisperx_/structured outputs/"

llm_results_path = f"{cur_path}/iteration_results"


scenario = "cardiac"
debug = False

my_range = ["1","2","3","4","5",""]
for iteration in my_range:

    ####################################################################################################
    ################################################ Orders ############################################
    ####################################################################################################
    ############ Manual orders ###########
    unique_manual_orders = [] # Extract all orders
    matching_manual_order = {} # Dictionary to see if LLM orders matched manual ones
    matching_manual_order_speaker = {} # Dictionary to see if LLM orders matched manual ones
    matching_manual_order_content = {} # Dictionary to see if LLM orders matched manual ones
    filename = f"manual_{scenario}.json"
    with open(os.path.join(cur_path, filename), "r") as f:
        data = json.load(f)
        for entry in data:
            if entry["Category"] == "Order":
                unique_manual_orders.append(entry)
                unique_id = entry["Start"]+"_"+ entry["end"] +"_"+ entry["Task"] 
                matching_manual_order[unique_id] = False
                matching_manual_order_content[unique_id] = False

    ############ LLM orders ###########
    # Merge all unique orders
    #unique_llm_orders = {}
    llm_orders_true_positives = 0  # Positive in LLM outcome and also in reality  => In LLM and ref
    llm_orders_false_positives = 0 # LLM predicts but it is not in reality        => In LLM but not in ref
    llm_orders_false_positives_unknown = 0
    llm_orders_false_negatives = 0 # LLM does not predict, but it in reality      => Not in LLM but in ref

    if iteration == "":
        filename = f"orders_merged_{scenario}.json"
    else:
        filename = f"iteration_{iteration}_orders_{scenario}.json"

    with open(os.path.join(llm_results_path, filename), "r") as f:
        data = json.load(f)
        for order in data:
            llm_start_time = float((datetime.strptime(order["Start"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            llm_stop_time = float((datetime.strptime(order["Finish"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            task = order["Task"]
            participants = task.split(":")[0]

            order_found = False
            speaker_found = False
            ############ Iterate manual orders to search match ###########
            for manual_order in unique_manual_orders:
                manual_start_time = float(manual_order["Start"])
                manual_stop_time = float(manual_order["end"])
                manual_participants = manual_order["Task"]

                if (llm_start_time >= manual_start_time and llm_start_time < manual_stop_time) or (llm_stop_time > manual_start_time and llm_stop_time <= manual_stop_time):
                    #order_found = True
                    unique_id = manual_order["Start"]+"_"+ manual_order["end"] +"_"+ manual_order["Task"] 

                    if manual_participants.lower() == participants.lower() and not matching_manual_order[unique_id]:
                        speaker_found = True
                        #print(f"True positive {participants}: {llm_start_time}_{llm_stop_time} and {manual_start_time}_{manual_stop_time}")
                        matching_manual_order[unique_id] = True
                        llm_orders_true_positives = llm_orders_true_positives + 1
                        break

            if speaker_found == False:
                if debug:
                    print(f"False positive: {llm_start_time}_{llm_stop_time} - {participants}")
                if "Unknown" in participants or participants == "":
                    llm_orders_false_positives_unknown = llm_orders_false_positives_unknown + 1
                #if order_found == False:
                llm_orders_false_positives = llm_orders_false_positives+ 1

    # Check False negatives
    for entry in matching_manual_order:
        if matching_manual_order[entry] == False:
            llm_orders_false_negatives = llm_orders_false_negatives + 1

    print("------")
    print(f"{iteration}True positives: {llm_orders_true_positives}")
    print(f"{iteration}False positives: {llm_orders_false_positives}")
    print(f"{iteration}False negatives: {llm_orders_false_negatives} (unk {llm_orders_false_positives_unknown})")
    print("------")


    llm_orders_true_positives_content = 0  # Positive in LLM outcome and also in reality  => In LLM and ref
    llm_orders_false_positives_content = 0
    llm_orders_false_negatives = 0

    with open(os.path.join(llm_results_path, filename), "r") as f:
        data = json.load(f)
        for order in data:
            llm_start_time = float((datetime.strptime(order["Start"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            llm_stop_time = float((datetime.strptime(order["Finish"],'%Y-%m-%d %H:%M:%S.%f') - datetime(1970,1,1)).total_seconds())
            task = order["Task"]
            participants = task.split(":")[0]

            content_found = False
            ############ Iterate manual orders to search match ###########
            for manual_order in unique_manual_orders:
                manual_start_time = float(manual_order["Start"])
                manual_stop_time = float(manual_order["end"])
                manual_participants = manual_order["Task"]

                if (llm_start_time >= manual_start_time and llm_start_time < manual_stop_time) or (llm_stop_time > manual_start_time and llm_stop_time <= manual_stop_time):
                    
                    unique_id = manual_order["Start"]+"_"+ manual_order["end"] +"_"+ manual_order["Task"] 

                    if not matching_manual_order_content[unique_id]:
                        content_found = True
                        matching_manual_order_content[unique_id] = True
                        llm_orders_true_positives_content = llm_orders_true_positives_content + 1
                        break

            if content_found == False:
                if debug:
                    print(f"False positive: {llm_start_time}_{llm_stop_time} - {participants}")
                llm_orders_false_positives_content = llm_orders_false_positives_content+ 1
                
    #unique_llm_orders[str(llm_start_time)+"_"+str(llm_stop_time)] = participants
    #print(unique_llm_orders)

    # Check False negatives
    for entry in matching_manual_order_content:
        if matching_manual_order_content[entry] == False:
            if debug:
                print(f"False negative: {entry}")
            llm_orders_false_negatives = llm_orders_false_negatives + 1

    print(f"Content {iteration}True positives: {llm_orders_true_positives_content}")
    print(f"Content {iteration}False positives: {llm_orders_false_positives_content}")
    print(f"Content {iteration}False negatives: {llm_orders_false_negatives}")
    # print(f"Precision: {llm_orders_true_positives/(llm_orders_true_positives+llm_orders_false_positives)}")
    # print(f"Recall: {llm_orders_true_positives/(llm_orders_true_positives+llm_orders_false_negatives)}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

