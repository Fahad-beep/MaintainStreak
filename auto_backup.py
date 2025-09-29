# -*- coding: utf-8 -*-
import os
import subprocess
import datetime
import yaml
from pathlib import Path

def setup_logging():
    """Setup logging directory and files"""
    log_dir = Path("D:/Fahad/backup_logs")
    log_dir.mkdir(exist_ok=True)
    return log_dir

def write_log(project, message, log_type="INFO"):
    """Write log entry to YAML file"""
    log_file = log_dir / f"{project}-backup.yaml"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = {
        "timestamp": timestamp,
        "type": log_type,
        "project": project,
        "message": message
    }
    
    # Check if it's a new day
    if log_file.exists():
        file_date = datetime.datetime.fromtimestamp(log_file.stat().st_mtime).strftime("%Y-%m-%d")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if file_date != today:
            # New day, clear the file
            with open(log_file, 'w', encoding='utf-8') as f:
                yaml.dump({"backup_logs": [log_entry]}, f)
            return
    
    # Append to existing file or create new
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {"backup_logs": []}
        data["backup_logs"].append(log_entry)
        with open(log_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
    else:
        with open(log_file, 'w', encoding='utf-8') as f:
            yaml.dump({"backup_logs": [log_entry]}, f)

def is_git_repo(path):
    """Check if directory is a git repository"""
    return (Path(path) / ".git").exists()

def get_git_changes(repo_path):
    """Get git status changes"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        changes = result.stdout.strip()
        return changes if changes else None
    except subprocess.CalledProcessError as e:
        return None

def backup_repository(repo_path, repo_name, streak_maintained):
    """Backup a single git repository"""
    print(f"\nBacking up: {repo_name}")
    print(f"Path: {repo_path}")
    
    if not is_git_repo(repo_path):
        write_log(repo_name, "Not a git repository", "ERROR")
        print("ERROR: Not a git repository")
        return streak_maintained, False
    
    # If streak already maintained, only push if there are actual changes
    if streak_maintained:
        changes = get_git_changes(repo_path)
        if not changes:
            print("INFO: Streak already maintained and no changes - skipping")
            write_log(repo_name, "Skipped - streak already maintained and no changes", "INFO")
            return streak_maintained, True
        else:
            print(f"INFO: Streak maintained but has changes - processing: {changes}")
    
    try:
        # Get changes before committing
        changes = get_git_changes(repo_path)
        
        if changes:
            write_log(repo_name, f"Starting backup - Changes detected: {changes}")
            print(f"  Changes detected: {changes}")
        else:
            write_log(repo_name, "Starting backup - No changes detected")
            print("  No changes detected")
        
        # Git add
        print("  Running: git add .")
        result = subprocess.run(["git", "add", "."], cwd=repo_path, capture_output=True, text=True)
        if result.returncode != 0:
            write_log(repo_name, "Git add failed", "ERROR")
            print("ERROR: Git add failed")
            return streak_maintained, False
        
        print("SUCCESS: Git add completed")
        write_log(repo_name, "Git add completed")
        
        # Git commit
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if changes:
            commit_message = f"auto backup - {timestamp}"
        else:
            commit_message = f"streak keeper - {timestamp}"
            
        print(f'  Running: git commit -m "{commit_message}"')
        result = subprocess.run(
            ["git", "commit", "-m", commit_message], 
            cwd=repo_path, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                write_log(repo_name, "No changes to commit", "INFO")
                print("INFO: No changes to commit")
                
                # Only create streak file if streak not maintained yet
                if not streak_maintained:
                    print("  Creating streak keeper file...")
                    streak_file = repo_path / "github_streak_keeper.txt"
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    with open(streak_file, 'w', encoding='utf-8') as f:
                        f.write(f"GitHub streak keeper - {current_time}\n")
                    
                    # Add and commit the streak file
                    subprocess.run(["git", "add", "."], cwd=repo_path, capture_output=True)
                    subprocess.run(["git", "commit", "-m", f"streak keeper - {timestamp}"], cwd=repo_path, capture_output=True)
                    print("SUCCESS: Created streak keeper commit")
                    write_log(repo_name, "Created streak keeper commit", "INFO")
                else:
                    print("INFO: Streak already maintained - no action needed")
                    return streak_maintained, True
            else:
                write_log(repo_name, f"Git commit failed: {result.stderr}", "ERROR")
                print("ERROR: Git commit failed")
                return streak_maintained, False
        else:
            if changes:
                write_log(repo_name, f"Committed actual changes: {changes}")
            else:
                write_log(repo_name, "Committed streak keeper")
            print("SUCCESS: Git commit completed")
        
        # Git push
        print("  Running: git push")
        result = subprocess.run(
            ["git", "push"], 
            cwd=repo_path, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            write_log(repo_name, f"Git push failed: {result.stderr}", "ERROR")
            print("ERROR: Git push failed")
            return streak_maintained, False
        
        write_log(repo_name, "Successfully pushed to remote")
        print("SUCCESS: Git push completed")
        
        # Mark streak as maintained for today
        return True, True
        
    except Exception as e:
        error_msg = str(e)
        write_log(repo_name, f"Backup failed: {error_msg}", "ERROR")
        print(f"ERROR: Backup failed: {error_msg}")
        return streak_maintained, False

def main():
    """Main backup function"""
    print("Starting Auto Git Backup")
    print(f"Time: {datetime.datetime.now()}")
    print("=" * 50)
    
    base_dir = Path("D:/Fahad")
    projects = [p for p in base_dir.iterdir() if p.is_dir() and p.name != "backup_logs"]
    
    print(f"Found {len(projects)} projects to backup")
    
    success_count = 0
    streak_maintained = False
    
    for project in projects:
        streak_maintained, project_success = backup_repository(project, project.name, streak_maintained)
        if project_success:
            success_count += 1
        
        # If streak is maintained, we can be more selective with remaining projects
        if streak_maintained:
            print(f"\nINFO: GitHub streak maintained. Remaining projects will only push if they have actual changes.")
    
    # Summary
    print("\n" + "=" * 50)
    print("BACKUP SUMMARY")
    print("=" * 50)
    print(f"Successful: {success_count}/{len(projects)}")
    print(f"GitHub Streak Maintained: {'YES' if streak_maintained else 'NO'}")
    print(f"Logs saved in: {log_dir}")
    print(f"Completed at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    log_dir = setup_logging()
    main()
