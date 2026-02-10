#     Abrir Anaconda Prompt
#     >> cd "G:\Mi unidad\doctorado\Pablo Castillo - DOCTORADO\2_soa\8 Prepare scenario\Audio analysis\LocalPython\Prototipo Whisperx_\GanttCharts"
#     >> G:
#     >> conda activate whisperx-web-ui & python "G:\Mi unidad\doctorado\Pablo Castillo - DOCTORADO\2_soa\8 Prepare scenario\Audio analysis\LocalPython\Prototipo Whisperx_\GanttCharts\B.ConvertJson2Gantt.py"
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def extract_task_name(task_text, filename):
    """Extract the correct task label depending on file type."""
    filename_lower = filename.lower()

    if "orders" in filename_lower:
        return task_text.split(":")[0].strip()

    if "skills" in filename_lower:
        return task_text.split("-")[0].strip().replace(":", " -")

    # Default fallback
    return task_text.strip()



# file_name = "crmscripted_timeline_orders"
file_name = "crmscripted_timeline_skills"



# Load JSON file
with open(file_name+".json", "r") as f:
    data = json.load(f)

# Process tasks
tasks = []
for item in data:
    task_name = extract_task_name(item["Task"], file_name)  # Only text before ":"
    start = datetime.strptime(item["Start"], "%Y-%m-%d %H:%M:%S.%f")
    finish = datetime.strptime(item["Finish"], "%Y-%m-%d %H:%M:%S.%f")
    tasks.append({"Task": task_name, "Start": start, "Finish": finish})

# Create DataFrame and sort by Start time
df = pd.DataFrame(tasks)
df = df.sort_values("Start").reset_index(drop=True)

# Plot Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))
task_labels = df["Task"].unique()

for i, task_label in enumerate(task_labels):
    task_data = df[df["Task"] == task_label]
    for _, row in task_data.iterrows():
        ax.barh(
            i,
            (row["Finish"] - row["Start"]).total_seconds(),
            left=(row["Start"] - df["Start"].min()).total_seconds(),
            height=0.4,
            align='center',
            color='skyblue'  # Same color for all bars
        )

# Set labels
ax.set_yticks(range(len(task_labels)))
ax.set_yticklabels(task_labels)
ax.invert_yaxis()  # Earliest tasks appear at the top
ax.set_xlabel("Time (seconds)")
ax.set_title("Gantt Chart by Orders/Skills")

plt.tight_layout()
plt.savefig("gantt_"+file_name+".png", dpi=300)
