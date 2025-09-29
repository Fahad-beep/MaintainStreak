# 🔄 Automated Git Backup System

A robust Python-based automation solution for maintaining GitHub contribution streaks by automatically backing up multiple Git repositories with intelligent commit management.

## 🚀 Features

- **🔄 Automated Daily Backups** - Scheduled daily execution at 11:50 AM
- **📊 Smart Streak Management** - Maintains GitHub contribution streak with minimal commits
- **🎯 Selective Pushing** - Only pushes necessary commits after streak is secured
- **📝 Comprehensive Logging** - YAML-based logging with daily file rotation
- **⚡ Multi-Repository Support** - Processes all Git repositories in a directory
- **🔒 Error Resilience** - Continues processing other repos if one fails

## 📁 Project Structure

```
D:/Fahad/
├── auto_backup.py          # Main backup script
├── auto_backup.bat         # Batch file wrapper
├── requirements.txt        # Python dependencies
└── backup_logs/           # Generated log files
    ├── Project1-backup.yaml
    ├── Project2-backup.yaml
    └── ...
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.6+
- Git installed and configured
- All repositories under `D:/Fahad/`

### 1. Clone/Copy Scripts
Place the following files in `D:/Fahad/`:

**`auto_backup.py`** - [See full script above]

**`auto_backup.bat`**
```batch
@echo off
cd /d "D:\Fahad"
python auto_backup.py
```

**`requirements.txt`**
```
PyYAML>=6.0
```

### 2. Install Dependencies
```cmd
cd D:\Fahad
pip install -r requirements.txt
```

### 3. Configure Task Scheduler

#### Method 1: GUI Setup
1. Open **Task Scheduler** (`taskschd.msc`)
2. Click **"Create Basic Task"**
3. Configure:
   - **Name**: `Auto Git Backup`
   - **Trigger**: Daily at 11:50 AM
   - **Action**: Start a program
   - **Program**: `D:\Fahad\auto_backup.bat`
   - **Start in**: `D:\Fahad`

#### Method 2: PowerShell (Admin)
```powershell
$Action = New-ScheduledTaskAction -Execute "D:\Fahad\auto_backup.bat"
$Trigger = New-ScheduledTaskTrigger -Daily -At "11:50AM"
Register-ScheduledTask -TaskName "AutoGitBackup" -Action $Action -Trigger $Trigger -Description "Automated Git backup for streak maintenance"
```

## 🔧 How It Works

### 🎯 Intelligent Backup Strategy

1. **Processes repositories in sequence**
2. **First repository**: Always ensures a push (creates streak file if no changes)
3. **Subsequent repositories**: Only push if they contain actual code changes
4. **Minimal footprint**: Avoids unnecessary commits once streak is secured

### 📊 Logging System

- **YAML format** for easy parsing and readability
- **Daily file rotation** - fresh logs each day
- **Structured entries** with timestamps and status types
- **Separate log files** per project

**Example Log Entry:**
```yaml
backup_logs:
- timestamp: 2024-01-15 11:50:03
  type: INFO
  project: Card
  message: Starting backup - Changes detected: M src/main.py
- timestamp: 2024-01-15 11:50:07
  type: INFO
  project: Card
  message: Successfully pushed to remote
```

## 🎪 Usage

### Manual Execution
```cmd
cd D:\Fahad
auto_backup.bat
```

### Expected Output
```
Starting Auto Git Backup
Time: 2024-01-15 11:50:00
==================================================
Found 3 projects to backup

Backing up: Card
Path: D:\Fahad\Card
  No changes detected
  Creating streak keeper file...
SUCCESS: Created streak keeper commit
SUCCESS: Git push completed

Backing up: LLM-RAG
Path: D:\Fahad\LLM-RAG
  Changes detected: M README.md, A src/utils.py
SUCCESS: Git push completed

INFO: GitHub streak maintained. Remaining projects will only push if they have actual changes.

==================================================
BACKUP SUMMARY
==================================================
Successful: 2/3
GitHub Streak Maintained: YES
Logs saved in: D:/Fahad/backup_logs
Completed at: 2024-01-15 11:50:45
```

## ⚙️ Configuration

### Customization Options

Modify these variables in `auto_backup.py`:

```python
# Base directory containing your repositories
base_dir = Path("D:/Fahad")

# Log directory
log_dir = base_dir / "backup_logs"

# Commit messages
commit_message = f"auto backup - {timestamp}"
streak_commit_message = f"streak keeper - {timestamp}"
```

## 🔍 Monitoring & Troubleshooting

### Check Logs
```cmd
# View latest logs
type D:\Fahad\backup_logs\ProjectName-backup.yaml
```

### Verify Task Scheduler
1. Open **Task Scheduler**
2. Navigate to **Task Scheduler Library**
3. Find **"Auto Git Backup"** task
4. Check **Last Run Result** and **History**

### Common Issues

**❌ Script doesn't run**
- Check Python installation: `python --version`
- Verify file paths in batch file
- Ensure execution policy allows scripts

**❌ Git authentication failures**
- Ensure SSH keys or credentials are configured
- Test manual `git push` from command line

**❌ Task runs but no commits**
- Check backup logs in `backup_logs/` directory
- Verify repositories have remote origins configured

## 🛡️ Reliability Features

- **✅ Error Handling** - Continues processing other repos if one fails
- **✅ Branch Detection** - Automatically tries `main` and `master` branches
- **✅ Change Detection** - Only commits when necessary
- **✅ Streak Protection** - Guarantees at least one commit per day
- **✅ Log Rotation** - Prevents log file bloat

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**💡 Pro Tip**: This system ensures your GitHub contribution graph stays green even on days when you don't actively code! 🟩
