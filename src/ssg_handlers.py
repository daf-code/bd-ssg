import re # reeeeeeeeeeeeeeeeee
from enum import Enum
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType

#Text Handlers: Node Handling
#TextNode to HTMLNode
def textnode_to_htmlnode(textnode: TextNode) -> HTMLNode:
    match textnode.text_type:
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text or "Image"})
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.NORMAL:
            return LeafNode(None, textnode.text)
        case _:
            raise ValueError(f"Invalid text type: {textnode.text_type}")

#Split Nodes at Delimiters
def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType)->list[TextNode]:
    new_nodes = []
    print(f"\nSplitting nodes with delimiter: '{delimiter}'")  # Debug

    for node in old_nodes:
        print(f"Processing node: '{node.text}'")  # Debug
        if node.text_type != TextType.NORMAL:
            print(f"Skipping non-normal node type: {node.text_type}")  # Debug
            new_nodes.append(node)
            continue
        if not delimiter in node.text:
            print(f"No delimiter found, keeping as is")  # Debug
            new_nodes.append(node)
            continue
        
        l_ptr = 0
        r_ptr = 0
        initial_done = False
        next_seg_inside = False
        delimiter_count = 0

        while l_ptr < len(node.text):
            if node.text[l_ptr:l_ptr+len(delimiter)] == delimiter:
                print(f"Found opening delimiter at position {l_ptr}")  # Debug
                r_ptr = l_ptr+1

                while r_ptr < len(node.text) and node.text[r_ptr:r_ptr+len(delimiter)] != delimiter:
                    r_ptr += 1

                if r_ptr >= len(node.text):
                    print(f"No matching closing delimiter found")  # Debug
                    l_ptr += 1
                    continue

                print(f"Found closing delimiter at position {r_ptr}")  # Debug

                if l_ptr != 0 and not initial_done:
                    print(f"Adding text before first delimiter: '{node.text[0:l_ptr]}'")  # Debug
                    new_nodes.append(TextNode(node.text[0:l_ptr], TextType.NORMAL))
                    initial_done = True
                    next_seg_inside = True

                if not initial_done:
                    text_seg = node.text[l_ptr+len(delimiter):r_ptr]
                    if text_seg: 
                        print(f"Adding delimited text: '{text_seg}' as {text_type}")  # Debug
                        new_nodes.append(TextNode(text_seg, text_type))
                    next_seg_inside = False
                    initial_done = True
                elif next_seg_inside:
                    text_seg = node.text[l_ptr+len(delimiter):r_ptr]
                    if text_seg: 
                        print(f"Adding delimited text: '{text_seg}' as {text_type}")  # Debug
                        new_nodes.append(TextNode(text_seg, text_type))
                    next_seg_inside = False
                else:
                    text_seg = node.text[l_ptr+len(delimiter):r_ptr]
                    if text_seg: 
                        print(f"Adding normal text: '{text_seg}'")  # Debug
                        new_nodes.append(TextNode(text_seg, TextType.NORMAL))
                    next_seg_inside = True

                l_ptr = r_ptr + len(delimiter)
                # Add any text after the closing delimiter if we're done with all delimiters
                if l_ptr < len(node.text) and node.text[l_ptr:].find(delimiter) == -1:
                    remaining_text = node.text[l_ptr:]
                    print(f"Adding remaining text after delimiter: '{remaining_text}'")  # Debug
                    new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
                    break
            else:
                l_ptr += 1

    print(f"Final nodes: {[node.text for node in new_nodes]}")  # Debug
    return new_nodes

#Extract Markdown Links and Images
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # returns list of tuples (alt_text, url)
    return images

def extract_markdown_links(text: str) -> list[tuple[str, str]]:    
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # returns list of tuples (alt_text, url)
    return links

#Process Text Nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:

        remaining_text = node.text
        node_image_list = extract_markdown_images(remaining_text)

        if len(node_image_list) == 0:
            new_nodes.append(node)
            continue
        for alt_text, image_url in node_image_list:
            # Split the text around the current image
            sections = remaining_text.split(f"![{alt_text}]({image_url})", 1)
    
            # 1. Add a TextType.NORMAL node for any text before the image
            if sections[0]:  # Add only if text exists
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
    
            # 2. Add a TextType.IMAGE node for the image itself
            new_nodes.append(TextNode("", TextType.IMAGE, image_url))
    
            # 3. Update the remaining text to process further
            remaining_text = sections[1]

        if remaining_text:
        #if sections[1]:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:

        remaining_text = node.text
        node_link_list = extract_markdown_links(remaining_text)

        if len(node_link_list) == 0:
            new_nodes.append(node)
            continue
        for alt_text, link_url in node_link_list:
            # Split the text around the current link
            sections = remaining_text.split(f"[{alt_text}]({link_url})", 1)
    
            # 1. Add a TextType.NORMAL node for any text before the link
            if sections[0]:  # Add only if text exists
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
    
            # 2. Add a TextType.LINK node for the link itself
            new_nodes.append(TextNode(alt_text, TextType.LINK, link_url))
    
            # 3. Update the remaining text to process further
            remaining_text = sections[1]

        if remaining_text:  # Check if any unprocessed text remains
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
            
    return new_nodes

#Text Handlers: Text to Node
def text_to_textnodes(text: str) -> list[TextNode]:
    
    raw_text_nodes = [TextNode(text, TextType.NORMAL)]
    text_nodes_to_process = split_nodes_delimiter(raw_text_nodes, "**", TextType.BOLD)
    text_nodes_to_process = split_nodes_delimiter(text_nodes_to_process, "*", TextType.ITALIC)
    text_nodes_to_process = split_nodes_delimiter(text_nodes_to_process, "`", TextType.CODE)
    text_nodes_to_process = split_nodes_image(text_nodes_to_process)
    text_nodes_to_process = split_nodes_link(text_nodes_to_process)

    return text_nodes_to_process

    #while text_nodes_to_process:
    #current_node = text_nodes_to_process.pop(0)
        
#Text Handlers: Markdown to Blocks
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    current_block = []
    
    for line in markdown.split("\n"):
        line = line.strip()
        print(f"Processing line: '{line}'")  # Debug
        
        if line.startswith("#"):
            if current_block:
                print(f"Creating block (heading): {current_block}")  # Debug
                blocks.append("\n".join(current_block))
                current_block = []
            blocks.append(line)
            continue
        
        if line.startswith(">") or (current_block and current_block[0].startswith(">")):
            if not line:  # Empty line in blockquote
                if current_block:
                    print(f"Creating block (quote): {current_block}")  # Debug
                    blocks.append("\n".join(current_block))
                    current_block = []
            else:  # Ensure > is preserved for blockquote content
                current_block.append(line)
            continue
        
        # Handle empty lines
        if not line:
            if current_block:
                print(f"Creating block (empty): {current_block}")  # Debug
                blocks.append("\n".join(current_block))
                current_block = []
            continue
            
        # Handle list items
        if line.startswith(("* ", "- ")):
            # If we're not already in a list block, start a new one
            if current_block and not current_block[0].startswith(("* ", "- ")):
                print(f"Creating block (list start): {current_block}")  # Debug
                blocks.append("\n".join(current_block))
                current_block = []
            current_block.append(line)
            continue
            
        # Handle regular text
        if current_block and current_block[0].startswith(("* ", "- ")):
            print(f"Creating block (list end): {current_block}")  # Debug
            blocks.append("\n".join(current_block))
            current_block = []
        current_block.append(line)
    
    if current_block:
        print(f"Creating final block: {current_block}")  # Debug
        blocks.append("\n".join(current_block))
    
    print("\nFinal blocks:")  # Debug
    for i, block in enumerate(blocks):
        print(f"Block {i}: '{block}'")  # Debug
    return blocks

#Block Handlers: Block type detection
def detect_block_type(block: str) -> str:
    print(f"\nDetecting block type for: '{block}'")  # Debug
    result = "pblock"  # Default
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        result = "hblock"
    elif block.startswith("```"):
        if block.endswith("```"):
            result = "codeblock"
    elif block.startswith(("* ", "- ")):
        for blockline in block.split("\n"):
            if blockline and not blockline.startswith(("* ", "- ")):
                result = "pblock"
                break
            # Ensure there's content after the list marker
            if blockline.startswith(("* ", "- ")) and len(blockline.lstrip("* -").strip()) == 0:
                result = "pblock"
                break
        else:
            result = "ulblock"
    elif block.startswith("1. "):
        item_count = 0
        for blockline in block.split("\n"):
            linelist = blockline.split(".")
            if linelist[0].isdigit():
                if linelist[0] == str(item_count+1) and linelist[1].startswith(" "): 
                    item_count += 1        
            else: 
                result = "pblock"
                break
        else:
            result = "olblock"
    elif block.startswith(">"):
        result = "qblock"
    
    print(f"Detected type: {result}")  # Debug
    return result

#Block Handlers: Block to HTML
def markdown_to_html(markdown: str) -> str:
    if not markdown.strip():
        return ""
        
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    
    for block in blocks:
        block_type = detect_block_type(block)
        match block_type:
            case "hblock":
                level = len(block) - len(block.lstrip("#"))
                text = block.lstrip("#").strip()
                nodes = text_to_textnodes(text)
                content = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                html_blocks.append(f"<h{level}>{content}</h{level}>")
            case "codeblock":
                html_blocks.append(f"<pre><code>{block.strip('```')}</code></pre>")
            case "ulblock":
                items = block.split("\n")
                html_blocks.append(process_nested_list(items))
            case "olblock":
                ol_items = []
                for item in block.split("\n"):
                    item_text = item.split(". ", 1)[1].strip()
                    nodes = text_to_textnodes(item_text)
                    content = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                    ol_items.append(f"<li>{content}</li>")
                html_blocks.append("<ol>" + "".join(ol_items) + "</ol>")
            case "qblock":
                html_blocks.append(process_blockquote(block))
            case "pblock":
                nodes = text_to_textnodes(block)
                content = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                html_blocks.append(f"<p>{content}</p>")
    
    return "\n".join(html_blocks)

def process_nested_list(items: list[str]) -> str:
    result = ["<ul>"]
    
    for item in items:
        # Split by newlines in case items were joined
        for subitem in item.split("\n"):
            if subitem.strip():  # Skip empty lines
                content = subitem.lstrip("* -").strip()
                nodes = text_to_textnodes(content)
                inner_html = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                result.append(f"<li>{inner_html}</li>")
    
    result.append("</ul>")
    return "\n".join(result)

def process_blockquote(block: str) -> str:
    raw_paragraphs = []
    current = []
    
    for line in block.split("\n"):
        line = line.lstrip(">").strip()  # Remove > and whitespace
        
        # If we have content and this line starts a list but previous content wasn't a list
        if line and line.startswith(("- ", "* ")) and current and not current[0].startswith(("- ", "* ")):
            raw_paragraphs.append("\n".join(current))
            current = []
        
        # If we have content and this line doesn't start a list but previous content was a list
        if line and not line.startswith(("- ", "* ")) and current and current[0].startswith(("- ", "* ")):
            raw_paragraphs.append("\n".join(current))
            current = []
        
        if line:  # If line has content
            current.append(line)
        elif current:  # If empty line and we have content
            raw_paragraphs.append("\n".join(current))
            current = []
    
    if current:
        raw_paragraphs.append("\n".join(current))
    
    # Process each paragraph
    html_blocks = []
    for para in raw_paragraphs:
        lines = para.split("\n")
        if lines[0].startswith(("- ", "* ")):  # List paragraph
            list_items = []
            for item in lines:
                item_text = item.lstrip("- *").strip()
                nodes = text_to_textnodes(item_text)
                content = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                list_items.append(f"<li>{content}</li>")
            html_blocks.append("<ul>\n" + "\n".join(list_items) + "\n</ul>")
        else:  # Regular paragraph
            nodes = text_to_textnodes(para)
            content = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
            html_blocks.append(f"<p>{content}</p>")
    
    return "<blockquote>\n" + "\n".join(html_blocks) + "\n</blockquote>"
