
---

# 🧮 100-HC-Tracker – Hardcore Run Tracker for SpeedrunIGT

**100-HC-Tracker** is a lightweight tool designed to track progress in Minecraft Hardcore challenges using SpeedrunIGT. It helps you monitor individual runs, current streaks, and generates files compatible with streaming overlays (e.g., OBS).

## 🛠 Requirements

* Python (3.8+ recommended)
* `pip` (Python package installer)
* SpeedrunIGT must already be set up
* Minecraft launcher like MultiMC

## 📁 Project Structure

By default, all tracker-related files are saved to:

```
~/speedrunigt/100HC/
```

This directory contains:

* `all_runs.json` – A complete log of all runs.
* `current_streak.json` – Tracks your current streak. Resets after death.
* `overlay.txt` – A text file formatted for easy integration into OBS overlays.

## 🧾 Configuration

Create a config file in JSON format:

```json
{
  "version": 1,
  "instance_path": "Path_to_instance", // e.g., "path-to-multi/MultiMC/instances/MyHardcoreInstance"
  "streak_prefix": "",
  "average_igt_prefix": ""
}
```

| Key                  | Description                                                               |
| -------------------- | ------------------------------------------------------------------------- |
| `version`            | Config version. Keep at 1 unless updates specify otherwise.               |
| `instance_path`      | Path to your Minecraft instance folder (used to locate SpeedrunIGT data). |
| `streak_prefix`      | (Optional) Prefix text for streak display in the overlay.                 |
| `average_igt_prefix` | (Optional) Prefix for showing average in-game time in the overlay.        |

## 🗂 Run Data Stored per Attempt

Each entry in `all_runs.json` contains the following:

| Field         | Description                                    |
| ------------- | ---------------------------------------------- |
| `record_file` | Filename from SpeedrunIGT containing raw data  |
| `final_igt`   | Final In-Game Time                             |
| `time`        | Real Time (RTA)                                |
| `finished`    | Boolean – `true` if completed, `false` if died |
| `seed`        | Seed of the world used in the run              |

## 📊 Planned Features (TBD)

* Automatic statistics and summaries (e.g., average IGT, deaths, streak history)
* Enhanced overlay formatting options

---
