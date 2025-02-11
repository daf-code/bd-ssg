import subprocess
import os
import shutil


def copy_static():
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from src
    static_dir = os.path.join(directory, 'static')
    public_dir = os.path.join(directory, 'public')
    temp_zip = 'temp.zip'  # Just the filename, since we're changing directory
    original_dir = os.getcwd()  # Store original directory at the start
    
    try:
        # Check if static directory exists
        if not os.path.exists(static_dir):
            raise Exception(f"Static directory not found: {static_dir}")
        
        # Change to static directory for zip operation
        os.chdir(static_dir)
        
        # Zip from within static directory
        subprocess.run(['zip', '-r', '-v', os.path.join('..', temp_zip), '.'], check=True)
    
        # Change to project root for unzip
        os.chdir(directory)
        subprocess.run(['unzip', '-o', temp_zip, '-d', 'public'], check=True)
        
        # Replace the ls commands with find
        static_files = set(subprocess.check_output(
            ['find', static_dir, '-type', 'f', '-printf', '%f\n']
        ).decode('utf-8').splitlines())

        public_files = set(subprocess.check_output(
            ['find', public_dir, '-type', 'f', '-printf', '%f\n']
        ).decode('utf-8').splitlines())

        # Check if each static file exists in public
        missing_files = static_files - public_files
        if missing_files:
            raise Exception(f"Verification failed: Missing files in public: {missing_files}")
        else:
            print("Verification successful: All files copied to public")
            
    finally:
        # Always try to return to original directory
        os.chdir(original_dir)
        # Clean up temp zip file if it exists
        if os.path.exists(os.path.join(directory, temp_zip)):
            os.remove(os.path.join(directory, temp_zip))