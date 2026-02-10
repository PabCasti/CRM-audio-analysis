# cd "G:\Mi unidad\doctorado\Pablo Castillo - DOCTORADO\2_soa\8 Prepare scenario\Audio analysis\LocalPython\Prototipo Whisperx_\Metrics"
# G:
# conda activate whisperx-web-ui & python generateMetrics.py

import json
import os
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

# ============================================================
# 1. CONSISTENT COLOR MAPPINGS
# ============================================================

SKILL_COLORS = {
    "Team Management": "#5dbcff",
    "Resource Allocation": "#fff86f",
    "Dynamic Decision": "#66ef66",
    "Environmental Awareness": "#ff7676"
}

SPEAKER_COLORS = {
    "Mandy": "#5dbcff",
    "Keith": "#fff86f",
    "Yanni": "#66ef66",
    "Bill": "#ff7676",
    "Isabelle": "#d2a2ff",
    
    "Brian": "#5dbcff",
    "Casey": "#fff86f",
    "Janelle": "#66ef66",
    "Jessie": "#ff7676",

    "Jim": "#5dbcff",
    
    "Emily": "#5dbcff",
    "John": "#fff86f",
    "Captain Jackson": "#66ef66",
}

def safe_filename(name: str) -> str:
    """Remove problematic characters from file names."""
    return "".join(c for c in name if c.isalnum() or c in ("_", "-")).replace(" ", "_")


# ============================================================
# 2. ORDER METRICS
# ============================================================

def compute_metrics_orders(json_path, output_folder):
    with open(json_path, "r") as f:
        data = json.load(f)

    speaker_durations = defaultdict(float)
    speaker_order_count = defaultdict(int)
    all_starts = []
    all_finishes = []
    total_orders = 0

    time_format = "%Y-%m-%d %H:%M:%S.%f"

    for entry in data:
        task = entry["Task"]
        start = datetime.strptime(entry["Start"], time_format)
        finish = datetime.strptime(entry["Finish"], time_format)

        speaker = task.split()[0].strip()

        duration = (finish - start).total_seconds()
        speaker_durations[speaker] += duration
        speaker_order_count[speaker] += 1
        total_orders += 1

        all_starts.append(start)
        all_finishes.append(finish)

    total_duration = (max(all_finishes) - min(all_starts)).total_seconds()

    print("\n=== Speaker Talk Time Summary ===")
    print(f"Total simulation time: {total_duration:.2f} seconds")
    for speaker, duration in speaker_durations.items():
        percentage = (duration / total_duration) * 100 if total_duration > 0 else 0
        orders = speaker_order_count[speaker]
        print(f"\t{speaker}: {duration:.2f} seconds ({percentage:.2f}%), "
              f"Orders given: {orders} ({orders/total_orders*100:.2f}%)")

    # Pie chart 1: speakers talk time (USE SPEAKER COLORS)
    plt.figure(figsize=(6, 6))
    plt.pie(
        speaker_durations.values(),
        labels=speaker_durations.keys(),
        autopct="%1.1f%%",
        colors=[SPEAKER_COLORS.get(s, "#999999") for s in speaker_durations.keys()]
    )
    plt.title("")
    # plt.title("Speaker Talk Time Distribution")
    plt.savefig(os.path.join(output_folder, f"metrics_{scenario}total_speakers_time.png"),
                dpi=300, bbox_inches="tight")
    plt.close()

    return speaker_durations


# ============================================================
# 3. SKILL INTERACTIONS
# ============================================================

def compute_interactions(json_path, output_folder):
    with open(json_path, "r") as f:
        items = json.load(f)

    counts = defaultdict(lambda: defaultdict(int))        # participant → skill → count
    skill_counts = defaultdict(lambda: defaultdict(int))  # skill → participant → count

    def extract_participant(task_text: str) -> str:
        return task_text.split(":")[0].strip()

    def extract_main_category(task_text: str) -> str:
        after_colon = task_text.split(":", 1)[1]
        return after_colon.split("-", 1)[0].strip()

    # Parse data
    for item in items:
        task = item["Task"]
        participant = extract_participant(task)
        main_skill = extract_main_category(task)

        counts[participant][main_skill] += 1
        skill_counts[main_skill][participant] += 1

    # PRINT SUMMARIES
    print("\n=== Speaker Interactions Summary ===")
    for participant, category_dict in counts.items():
        total = sum(category_dict.values())
        print(f"{participant}:")
        for category, count in category_dict.items():
            pct = (count / total) * 100 if total > 0 else 0
            print(f"\t{category}: {count} interactions ({pct:.2f}%)")

    print("\n=== NTS Interactions Summary ===")
    for skill, participants_dict in skill_counts.items():
        total = sum(participants_dict.values())
        print(f"{skill}: {total} total interactions.")
        for participant, count in participants_dict.items():
            pct = (count / total) * 100 if total > 0 else 0
            print(f"\t{participant}: {count} interactions ({pct:.2f}%)")

    # ============================================================
    # PIE CHART A — per SKILL (skill → participants)
    # Slices = speakers → USE SPEAKER COLORS
    # ============================================================

    for skill, participants_dict in skill_counts.items():
        plt.figure(figsize=(6, 6))

        colors = [
            SPEAKER_COLORS.get(participant, "#B6B6B6")
            for participant in participants_dict.keys()
        ]

        plt.pie(
            participants_dict.values(),
            labels=participants_dict.keys(),
            autopct="%1.1f%%",
            pctdistance=1.15,      # move percentages outward
            labeldistance=1.3,    # move labels even more outside
            colors=colors
        )
        plt.title("")
        # plt.title(f"Participants for Skill: {skill}")

        fname = f"metrics_{scenario}{safe_filename(skill)}_speakers.png"
        plt.savefig(os.path.join(output_folder, fname), dpi=300, bbox_inches="tight")
        plt.close()

    # ============================================================
    # PIE CHART B — per PARTICIPANT (participant → skills)
    # Slices = skills → USE SKILL COLORS
    # ============================================================

    for participant, skills_dict in counts.items():
        plt.figure(figsize=(6, 6))

        colors = [
            SKILL_COLORS.get(skill, "#bbbbbb")
            for skill in skills_dict.keys()
        ]

        plt.pie(
            skills_dict.values(),
            labels=skills_dict.keys(),
            autopct="%1.1f%%",
            pctdistance=1.15,      # move percentages outward
            labeldistance=1.3,    # move labels even more outside
            colors=colors
        )
        plt.title("")
        # plt.title(f"{participant} - Interactions by Main Skill")

        fname = f"metrics_{scenario}{safe_filename(participant)}_skills.png"
        plt.savefig(os.path.join(output_folder, fname), dpi=300, bbox_inches="tight")
        plt.close()


###############################################################
# MAIN SCRIPT
###############################################################

scenario = "cardiac"
# scenario = "clinical"
# scenario = "crmscripted"
# scenario = "crmboeing"

os.makedirs(scenario, exist_ok=True)

compute_metrics_orders(scenario + "_timeline_orders.json", scenario)
compute_interactions(scenario + "_timeline_skills.json", scenario)


