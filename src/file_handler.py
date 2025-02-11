import glob
import subprocess
import os
import time
import shutil


def copy_static():
    try:
        directory = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(directory, 'static')
        public_dir = os.path.join(directory, 'public')
        
        # Remove and recreate public directory
        shutil.rmtree(public_dir, ignore_errors=True)
        os.makedirs(public_dir)
        
        timestamp = int(time.time())
        temp_zip = os.path.join(directory, f'temp_{timestamp}.zip')
        
        subprocess.run(['zip', '-r -v', temp_zip, static_dir], check=True)
        subprocess.run(['unzip', '-o -v', temp_zip, '-d', public_dir], check=True)
        
        # Get directory listings and split into lines
        static_ls = set(subprocess.check_output(['ls', '-R', static_dir]).decode('utf-8').splitlines())
        public_ls = set(subprocess.check_output(['ls', '-R', public_dir]).decode('utf-8').splitlines())
        
        # Check if each static file exists in public
        missing_files = static_ls - public_ls
        if missing_files:
            raise Exception(f"Verification failed: Missing files in public: {missing_files}")
        else:
            print("Verification successful: All files copied to public")
            
    finally:
        # Always attempt to clean up the temp file
        if os.path.exists(temp_zip):
            os.remove(temp_zip)