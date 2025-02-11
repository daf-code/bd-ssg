import md_to_html as md_to_html
import ssg_handlers as ssg_handlers
import leafnode as leafnode
import parentnode as parentnode
import os

def extract_title(markdown):
    # Extract the title from the markdown
    # The title is the first line of level 1 heading
    markdown_lines = markdown.split('\n')
    for line in markdown_lines:
        if line.startswith('# '):
            return line[2:].strip()
    return None

def generate_page(from_path, template_path, dest_path):
    print(f"Generating HTML page from {from_path} to {dest_path} using template {template_path}")
    # Read the markdown file
    with open(from_path, 'r') as file:
        markdown = file.read()
        
    # Extract the title
    title = extract_title(markdown)
    if title is None:
        title = "Untitled Page"

    # Read the template file
    with open(template_path, 'r') as file:
        template = file.read()
    
    # Convert markdown to HTML node and then to HTML string
    html_node = md_to_html.markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    
    # Replace the title and content in the template
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    # Write the generated HTML to the destination file
    with open(dest_path, 'w') as file:
        file.write(template)
        
    print(f"Generated HTML page saved to {dest_path}")

def generate_pages_recursively(content_dir, template_path, public_dir):
    """
    Recursively generate HTML pages from markdown files while maintaining directory structure
    """
    # Create the public directory if it doesn't exist
    os.makedirs(public_dir, exist_ok=True)
    
    for item in os.listdir(content_dir):
        content_path = os.path.join(content_dir, item)
        public_path = os.path.join(public_dir, item)
        
        if os.path.isfile(content_path):
            if item.endswith('.md'):
                # Convert .md files to .html
                html_path = public_path.replace('.md', '.html')
                generate_page(content_path, template_path, html_path)
        elif os.path.isdir(content_path):
            # Create corresponding directory in public and recurse
            generate_pages_recursively(content_path, template_path, public_path)
