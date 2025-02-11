import textnode as textnode
import file_handler as file_handler
import generate_page as generate_page
import os
import shutil

def main():
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from src
    static_dir = os.path.join(directory, 'static')
    public_dir = os.path.join(directory, 'public')
    
    # Remove the public directory if it exists
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir, ignore_errors=True)
    # Create the public directory
    os.makedirs(public_dir) 
   
    # Copy the static files to the public directory
    file_handler.copy_static()

    # Generate the index page
    generate_page.generate_pages_recursively(os.path.join(directory, 'content'), os.path.join(directory, 'template.html'), public_dir)

if __name__ == "__main__":
    main()