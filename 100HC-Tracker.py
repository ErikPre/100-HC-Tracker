import json
import os
from pathlib import Path

config_path = Path(os.path.expanduser("~/speedrunigt/100HC/config.json"))
if config_path.exists():
    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.decoder.JSONDecodeError:
            print("Config file is corrupted or has an syntax error. Please check the file.")
            config = {
                "version": 1,
                "instance_path": None,
                "streak_prefix": "Streak: ",
                "average_igt_prefix": "Avg IGT: ",
            }

    if config["instance_path"] is not None:
        # check if nbt is installed if not install
        try:
            from nbt import nbt
        except ImportError:
            import subprocess
            import sys

            print("NBT-Bibliothek nicht gefunden. Installiere...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "nbt"])
            from nbt import nbt




def process_record(record_path, config):
    import json

    with open(record_path, 'r') as file:
        record = json.load(file)
        # Here you would add your processing logic

        if config["instance_path"] is not None:
            worldfile = Path(config["instance_path"]) / ".minecraft/saves/" / record["world_name"] / "level.dat"
            info = nbt.NBTFile(worldfile, 'rb')
            seed = info["Data"]["WorldGenSettings"]["seed"].value
            is_hardcore = info["Data"]["hardcore"].value == 1

            if not is_hardcore:
                return
        else:
            seed = None

        if record["is_completed"]:
            print(f"Record {record_path} is completed.")
            print(f"final_igt: {record['final_igt']}")





            with open(Path(os.path.expanduser("~/speedrunigt/100HC/all_runs.json")), "r") as f:
                all_runs = json.load(f)

            if record_path.name in [current["record"] for current in all_runs]:
                print(f"Record {record_path.name} already exists in current streak.")
                return

            with open(Path(os.path.expanduser("~/speedrunigt/100HC/current_streak.json")), "r") as f:
                current_streak = json.load(f)

            current_streak.append({
                    "record": record_path.name,
                    "final_igt": record["final_igt"],
                    "time": record["final_rta"],
                    "finished": True,
                    "seed": seed
                })
            with open(Path(os.path.expanduser("~/speedrunigt/100HC/current_streak.json")), "w") as f:
                json.dump(current_streak, f, indent=4)

            with open(Path(os.path.expanduser("~/speedrunigt/100HC/all_runs.json")), "r") as f:
                all_runs = json.load(f)
            all_runs.append({
                    "record": record_path.name,
                    "final_igt": record["final_igt"],
                    "time": record["final_rta"],
                    "finished": True,
                    "seed": seed,
                    "splits": record["timelines"]
                })
            with open(Path(os.path.expanduser("~/speedrunigt/100HC/all_runs.json")), "w") as f:
                json.dump(all_runs, f, indent=4)
            update_overlay(config)
            return

        if ("minecraft:deaths" in record["stats"][list(record["stats"].keys())[0]]["stats"]["minecraft:custom"].keys()
                and record["stats"][list(record["stats"].keys())[0]]["stats"]["minecraft:custom"]["minecraft:deaths"] > 0):

            with open(Path(os.path.expanduser("~/speedrunigt/100HC/all_runs.json")), "r") as f:
                all_runs = json.load(f)

            if record_path.name in [current["record"] for current in all_runs]:
                print(f"Record {record_path.name} already exists in current streak.")
                return

            print(f"Record {record_path} has deaths.")

            with open(Path(os.path.expanduser("~/speedrunigt/100HC/current_streak.json")), "w") as f:
                json.dump([], f, indent=4)

            with open(Path(os.path.expanduser("~/speedrunigt/100HC/all_runs.json")), "r") as f:
                all_runs = json.load(f)
            all_runs.append({
                "record": record_path.name,
                "final_igt": record["final_igt"],
                "time": record["final_rta"],
                "finished": False,
                "seed": seed,
                "splits": record["timelines"]
            })
            with open(Path(os.path.expanduser("~/speedrunigt/100HC/all_runs.json")), "w") as f:
                json.dump(all_runs, f, indent=4)
            update_overlay(config)



def update_overlay(config):
    import json
    try:
        streak_prefix = config.get("streak_prefix", "")
        average_igt_prefix = config.get("average_igt_prefix", "")
        with open(Path(os.path.expanduser("~/speedrunigt/100HC/current_streak.json")), "r") as f:
            current_streak = json.load(f)

        if not current_streak:
            overlay_content = f"{streak_prefix}{len(current_streak)}\n{average_igt_prefix}00:00"

            with open(Path(os.path.expanduser("~/speedrunigt/100HC/overlay.txt")), "w") as f:
                f.write(overlay_content)
            return
        print("Updating overlay with current streak data...")
        avarage_igt = sum(float(record['final_igt']) for record in current_streak) / len(current_streak)

        # average_igt is in milliseconds, convert to HH:MM:SS format
        avarage_igt_seconds = int(avarage_igt / 1000)
        avarage_igt_hours = avarage_igt_seconds // 3600
        avarage_igt_seconds %= 3600
        avarage_igt_minutes = avarage_igt_seconds // 60
        avarage_igt_seconds %= 60
        avarage_igt = f"{avarage_igt_hours:02}:{avarage_igt_minutes:02}:{avarage_igt_seconds:02}"
        # if hours are 0, show only minutes and seconds
        if avarage_igt_hours == 0:
            avarage_igt = f"{avarage_igt_minutes:02}:{avarage_igt_seconds:02}"

        overlay_content = f"{streak_prefix}{len(current_streak)}\n{average_igt_prefix}{avarage_igt}"

        with open(Path(os.path.expanduser("~/speedrunigt/100HC/overlay.txt")), "w") as f:
            f.write(overlay_content)

        print("Overlay updated successfully.")
    except Exception as e:
        print(f"Error updating overlay: {e}")

def loop(interval, records_path, config):
    import time
    #check if last modified file in records_path

    last_modified = None
    save_seed = config["instance_path"] is not None
    while True:
        try:
            current_modified = max(f.stat().st_mtime for f in records_path.glob("*.json"))
            current_modified_file_name = max(records_path.glob("*.json"), key=lambda f: f.stat().st_mtime)
            if last_modified is None:
                last_modified = current_modified
                continue

            if current_modified > last_modified:
                last_modified = current_modified
                last_modified_file_name = current_modified_file_name
                print("New record detected, processing...")
                # Here you would call your processing function
                process_record(last_modified_file_name, config)
        except Exception as e:
            print(f"Error processing records: {e}")

        time.sleep(interval)



def init():
    folder = Path(os.path.expanduser("~/speedrunigt/100HC"))
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {folder}")

    if not Path(os.path.expanduser("~/speedrunigt/100HC/current_streak.json")).exists():
        with open(Path(os.path.expanduser("~/speedrunigt/100HC/current_streak.json")), 'w') as f:
            f.write('[]')

    if not Path(os.path.expanduser("~/speedrunigt/100HC/all_runs.json")).exists():
        with open(Path(os.path.expanduser("~/speedrunigt/100HC/all_runs.json")), 'w') as f:
            f.write('[]')

    if not Path(os.path.expanduser("~/speedrunigt/100HC/overlay.txt")).exists():
        with open(Path(os.path.expanduser("~/speedrunigt/100HC/overlay.txt")), 'w') as f:
            f.write('0\n00:00')

    # config.json
    if not Path(os.path.expanduser("~/speedrunigt/100HC/config.json")).exists():
        with open(Path(os.path.expanduser("~/speedrunigt/100HC/config.json")), 'w') as f:
            init_config = {
                "version": 1,
                "instance_path": None,
                "streak_prefix": "",
                "average_igt_prefix": "",
            }
            f.write(json.dumps(init_config, indent=4))





if __name__ == "__main__":
    # User/username/speedrunigt/records
    init()

    # load config
    config_path = Path(os.path.expanduser("~/speedrunigt/100HC/config.json"))
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            print("Loaded config:", config)
    else:
        print("Config file not found, using default settings.")

    update_overlay(config)
    records_path = Path(os.path.expanduser("~/speedrunigt/records"))
    loop(5, records_path, config)  # Check every 5 seconds
