import os
import subprocess
import datetime

def backup_database():
    # PostgreSQL connection details
    db_host = str(os.getenv('HOST'))
    db_name = str(os.getenv('NAME'))
    db_user = str(os.getenv('USER'))
    db_pass = str(os.getenv('PASSWORD'))
    db_port = str(os.getenv('PORT'))

    # Backup directory
    backup_dir = './backups/'

    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Backup file name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"{backup_dir}backup_{db_name}_{timestamp}.sql"

    # Command to create backup using pg_dump
    command = f"pg_dump -h {db_host} -U {db_user} -p {db_port} -d {db_name} -w -Fc -f {backup_file}"

    try:
        # Execute the backup command
        subprocess.call(command, shell=True)
        print("Backup successful!")
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during the backup process
        print(f"Error creating backup: {e}")

if __name__ == "__main__":
    backup_database()
