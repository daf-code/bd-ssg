from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from ssg_handlers import markdown_to_blocks, detect_block_type

def markdown_to_html_node(markdown: str) -> HTMLNode:
    # Create root div node that will contain all blocks
    root = ParentNode("div")
    
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    block_nodes = []
    for block in blocks:
        block_type = detect_block_type(block)
        match block_type:
            case "hblock":
                # Get header level from number of #s
                level = len(block) - len(block.lstrip("#"))
                text = block.lstrip("#").strip()
                # Convert text to nodes
                # Create h1-h6 node with children
                
            case "pblock":
                # Convert text to nodes
                # Create p node with children
                
            case "ulblock":
                # Split into list items
                # Convert each item's text to nodes
                # Create ul node with li children
                
            case "olblock":
                # Split into list items
                # Convert each item's text to nodes
                # Create ol node with li children
                
            case "codeblock":
                # Extract code content
                # Create pre/code node structure
                
            case "qblock":
                # Convert text to nodes
                # Create blockquote node with children
                
        # Add the created node to block_nodes
    
    root.children = block_nodes
    return root
