# OS-Janitor
# 🧹 OS Janitor

**Automated File Organization & Cleanup Tool**

OS Janitor is a Python-based automation tool designed to keep your file system (specifically `Downloads` or `Desktop`) organized. Instead of manually sorting files, this script scans for "stale" files (older than 30 days), moves them to a safe **Quarantine Folder**, and provides a CLI interface to review, restore, or permanently delete them.

It includes **"Silent Mode"** for background automation via Windows Task Scheduler or Linux Cron.

---

## 🚀 Key Features

*   **📅 Stale Detection:** Automatically identifies files older than a specific threshold (default: 30 days).
*   **🛡️ Safety First:** Files are **never** deleted immediately. They are moved to a `_TO_DELETE_REVIEW` folder.
*   **↩️ Smart Restore:** Includes a CLI menu to restore files to their *exact original location* using a JSON history map.
*   **🤖 Automation Ready:** Runs silently in the background when triggered by Task Scheduler/Cron.
*   **📝 Logging:** Keeps a detailed record (`janitor.log`) of every file moved.

---

## 🛠️ Project Structure

```text
OS-Janitor/
│
├── janitor.py          # The main Python script (Cleaner + Restore Wizard)
├── run_janitor.bat     # Batch file for Windows Task Scheduler automation
├── janitor.log         # Log file generated after running (Silent Mode)
└── README.md           # Project documentation

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/OS-Janitor.git
   cd OS-Janitor