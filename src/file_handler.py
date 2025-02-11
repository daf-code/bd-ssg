import glob
import subprocess
import os
import time
import shutil


def copy_static():
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from src
    static_dir = os.path.join(directory, 'static')
    public_dir = os.path.join(directory, 'public')
    timestamp = int(time.time())
    temp_zip = 'temp.zip'  # Just the filename, since we're changing directory
    
    try:
        # Check if static directory exists
        if not os.path.exists(static_dir):
            raise Exception(f"Static directory not found: {static_dir}")
        
        # Remove and recreate public directory
        shutil.rmtree(public_dir, ignore_errors=True)
        os.makedirs(public_dir)
        
        # Change to project root directory for zip/unzip operations
        original_dir = os.getcwd()
        os.chdir(directory)
        
        # Zip and unzip commands
        subprocess.run(['zip', '-r', '-v', temp_zip, 'static'], check=True)
        subprocess.run(['unzip', '-j', '-o', temp_zip, 'static/*', '-d', 'public'], check=True)
        
        # Get directory listings and split into lines, filter out directory paths
        static_ls = set(line for line in subprocess.check_output(['ls', '-R', static_dir]).decode('utf-8').splitlines() 
                       if not line.endswith(':') and line.strip())
        public_ls = set(line for line in subprocess.check_output(['ls', '-R', public_dir]).decode('utf-8').splitlines()
                       if not line.endswith(':') and line.strip())
        
        # Check if each static file exists in public
        missing_files = static_ls - public_ls
        if missing_files:
            raise Exception(f"Verification failed: Missing files in public: {missing_files}")
        else:
            print("Verification successful: All files copied to public")
            
    finally:
        # Change back to original directory and cleanup
        os.chdir(directory)  # Ensure we're in the right directory for cleanup
        if os.path.exists(temp_zip):
            os.remove(temp_zip)
        if original_dir:  # Make sure we go back to where we started
            os.chdir(original_dir)