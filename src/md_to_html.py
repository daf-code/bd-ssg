from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from ssg_handlers import markdown_to_blocks, detect_block_type, text_to_textnodes, textnode_to_htmlnode

def markdown_to_html_node(markdown: str) -> HTMLNode:
    # Create root div node that will contain all blocks of the markdown document
    root = ParentNode("div")
    
    # Split markdown string into blocks based on blank lines and block-level syntax
    blocks = markdown_to_blocks(markdown)
    
    # Initialize list to store HTML nodes for each block
    block_nodes = []
    for block in blocks:
        # Determine the type of block (header, paragraph, list, etc)
        block_type = detect_block_type(block)
        match block_type:
            case "hblock":
                # Count leading #s to determine header level (h1-h6)
                level = len(block) - len(block.lstrip("#"))
                # Remove #s and whitespace to get header text
                text = block.lstrip("#").strip()
                # Parse text for inline elements (bold, italic, etc)
                text_nodes = text_to_textnodes(text)
                # Convert each text node to its HTML representation
                html_nodes = [textnode_to_htmlnode(node) for node in text_nodes]
                # Create header node (h1-h6) containing the processed inline elements
                header = ParentNode(f"h{level}", html_nodes)
                # Add the complete header node to our list of blocks
                block_nodes.append(header)
                
            case "pblock":
                # Parse block text for inline elements (bold, italic, links, etc)
                text_nodes = text_to_textnodes(block)
                # Convert each text node to its HTML representation
                html_nodes = [textnode_to_htmlnode(node) for node in text_nodes]
                # Create paragraph node containing the processed inline elements
                paragraph = ParentNode("p", html_nodes)
                # Add the complete paragraph node to our list of blocks
                block_nodes.append(paragraph)
                
            case "ulblock":
                # Split block into individual list items by newline
                items = block.split("\n")
                # Initialize list to store processed list item nodes
                list_items = []
                for item in items:
                    # Remove leading * or - and whitespace
                    item_text = item.lstrip("* -").strip()
                    # Parse item text for inline elements
                    text_nodes = text_to_textnodes(item_text)
                    # Convert text nodes to HTML nodes
                    html_nodes = [textnode_to_htmlnode(node) for node in text_nodes]
                    # Create li node containing the processed inline elements
                    li_node = ParentNode("li", html_nodes)
                    # Add to list of items
                    list_items.append(li_node)
                # Create ul node containing all list items
                ul_node = ParentNode("ul", list_items)
                # Add the complete unordered list to our blocks
                block_nodes.append(ul_node)
                
            case "olblock":
                # Split block into individual list items by newline
                items = block.split("\n")
                # Initialize list to store processed list item nodes
                list_items = []
                for item in items:
                    # Split on period and take everything after it, remove whitespace
                    item_text = item.split(". ", 1)[1].strip()
                    # Parse item text for inline elements
                    text_nodes = text_to_textnodes(item_text)
                    # Convert text nodes to HTML nodes
                    html_nodes = [textnode_to_htmlnode(node) for node in text_nodes]
                    # Create li node containing the processed inline elements
                    li_node = ParentNode("li", html_nodes)
                    # Add to list of items
                    list_items.append(li_node)
                # Create ol node containing all list items
                ol_node = ParentNode("ol", list_items)
                # Add the complete ordered list to our blocks
                block_nodes.append(ol_node)
                
            case "codeblock":
                # Remove leading and trailing ``` markers
                code_content = block.strip("`").strip()
                # Create leaf node for code content (no parsing of inline elements)
                code_node = LeafNode("code", code_content)
                # Wrap code node in pre node for proper HTML formatting
                pre_node = ParentNode("pre", [code_node])
                # Add the complete code block to our blocks
                block_nodes.append(pre_node)
                
            case "qblock":
                # Split block into lines and process each line
                lines = block.split("\n")
                # Remove leading and trailing empty lines while preserving internal ones
                lines = [line.lstrip(">").strip() for line in lines]
                while lines and not lines[0]:  # Remove leading empty lines
                    lines.pop(0)
                while lines and not lines[-1]:  # Remove trailing empty lines
                    lines.pop()
                
                # Group lines into paragraphs
                paragraphs = []
                current_para = []
                for line in lines:
                    if line:
                        current_para.append(line)
                    elif current_para:  # Empty line and we have content
                        paragraphs.append(" ".join(current_para))
                        current_para = []
                if current_para:  # Don't forget last paragraph
                    paragraphs.append(" ".join(current_para))
                
                quote_nodes = []
                for para in paragraphs:
                    text_nodes = text_to_textnodes(para)
                    html_nodes = [textnode_to_htmlnode(node) for node in text_nodes]
                    if len(paragraphs) > 1:  # Only wrap in <p> if multiple paragraphs
                        p_node = ParentNode("p", html_nodes)
                        quote_nodes.append(p_node)
                    else:
                        quote_nodes.extend(html_nodes)  # Single paragraph, no <p> wrapper
                
                # Create blockquote node containing all processed nodes
                quote_node = ParentNode("blockquote", quote_nodes)
                # Add the complete blockquote to our blocks
                block_nodes.append(quote_node)
    
    # Set all processed blocks as children of the root div
    root.children = block_nodes
    # Return the complete HTML node tree
    return root
