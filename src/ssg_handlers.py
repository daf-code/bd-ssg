import re # reeeeeeeeeeeeeeeeee
from enum import Enum
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType

#Text Handlers: Node Handling
#TextNode to HTMLNode
def textnode_to_htmlnode(textnode: TextNode) -> HTMLNode:
    valid_types = [TextType.NORMAL, TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE]
    
    if textnode.text_type not in valid_types:
        raise ValueError(f"Invalid text type: {textnode.text_type}")
    
    match textnode.text_type:
        case TextType.NORMAL:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("strong", textnode.text)
        case TextType.ITALIC:
            return LeafNode("em", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text}) 
        

#Split Nodes at Delimiters
def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType)->list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        #print(f"Input text: '{node.text}'")
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Invalid markdown: unmatched delimiters")
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        if not delimiter in node.text:
            new_nodes.append(node)
            continue
        
        l_ptr = 0
        r_ptr = 0
        initial_done = False
        next_seg_inside = False

        while l_ptr < len(node.text):
            if node.text[l_ptr:l_ptr+len(delimiter)] == delimiter:
                if l_ptr != 0 and not initial_done:
                    #print(f"Adding initial outsidesegment: '{node.text[0:l_ptr]}'")
                    new_nodes.append(TextNode(node.text[0:l_ptr], TextType.NORMAL))
                    initial_done = True
                    next_seg_inside = True

                r_ptr = l_ptr+1

                while r_ptr < len(node.text) and node.text[r_ptr:r_ptr+len(delimiter)] != delimiter:
                    r_ptr += 1

                if not initial_done:
                    text_seg = node.text[l_ptr+len(delimiter):r_ptr]
                    if text_seg: new_nodes.append(TextNode(text_seg, text_type))
                    next_seg_inside = False # this is the initial segment and is inside the delimiters
                    initial_done = True

                elif next_seg_inside is True:
                    text_seg = node.text[l_ptr+len(delimiter):r_ptr]
                    if text_seg: new_nodes.append(TextNode(text_seg, text_type))
                    next_seg_inside = False

                else:
                    text_seg = node.text[l_ptr+len(delimiter):r_ptr]
                    if text_seg: new_nodes.append(TextNode(text_seg, TextType.NORMAL))
                    next_seg_inside = True


                #print(f"l_ptr: {l_ptr}, r_ptr: {r_ptr}")
               #print(f"Current text segment: '{node.text[l_ptr:r_ptr]}'")
                l_ptr = r_ptr
                
            else:
                l_ptr += 1

        # This is now outside the while loop, at the same level as the while
        if l_ptr < len(node.text) and len(node.text[l_ptr:].strip()) > 0:
            #print(f"Adding final segment: '{node.text[l_ptr:]}'")
            new_nodes.append(TextNode(node.text[l_ptr:], TextType.NORMAL))

    #print("Final nodes:")
    #for i, n in enumerate(new_nodes):
        #print(f"Node {i}: text='{n.text}', type={n.text_type}")

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
    parsed_blocks = []
    for next_lines in markdown.split("\n\n"):
        next_lines = next_lines.strip()
        if next_lines == "":
            continue
        
        block_lines = next_lines.split("\n")
        cleaned_lines = [line.strip() for line in block_lines]
        parsed_blocks.append("\n".join(cleaned_lines))
    return parsed_blocks

#Block Handlers: Block type detection
def detect_block_type(block: str) -> str:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "hblock"
    if block.startswith("```"):
        if block.endswith("```"):
            return "codeblock"
    if block.startswith(("* ", "- ")):
        for blockline in block.split("\n"):
            if not blockline.startswith(("* ", "- ")):
                return "pblock"
        return "ulblock"
    if block.startswith("1. "):
        item_count = 0
        for blockline in block.split("\n"):
            linelist = blockline.split(".")
            if linelist[0].isdigit():
                if linelist[0] == str(item_count+1) and linelist[1].startswith(" "): item_count += 1        
            else: return "pblock"
        return "olblock"
    if block.startswith(">"):
        for blockline in block.split("\n"):
            if not blockline.startswith(">"):
                return "pblock"
        return "qblock"
    return "pblock"

#Block Handlers: Block to HTML
def markdown_to_html(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in blocks:
        block_type = detect_block_type(block)
        match block_type:
            case "hblock":
                text = block.strip("# ")
                nodes = text_to_textnodes(text)
                inner_html = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                html_blocks.append(f"<h{block.count('#')}>{inner_html}</h{block.count('#')}>")

            case "codeblock":
                html_blocks.append(f"<pre><code>{block.strip('```')}</code></pre>")

            case "ulblock":
                ul_items = []
                for item in block.split("\n"):
                    item_text = item.lstrip("* -").strip()
                    nodes = text_to_textnodes(item_text)
                    inner_html = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                    ul_items.append(f"<li>{inner_html}</li>")
                html_blocks.append("<ul>" + "".join(ul_items) + "</ul>")

            case "olblock":
                ol_items = []
                for item in block.split("\n"):
                    item_text = item.split(". ", 1)[1].strip()
                    nodes = text_to_textnodes(item_text)
                    inner_html = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                    ol_items.append(f"<li>{inner_html}</li>")
                html_blocks.append("<ol>" + "".join(ol_items) + "</ol>")

            case "qblock":
                quote_text = "\n".join(line.lstrip(">").strip() for line in block.split("\n"))
                nodes = text_to_textnodes(quote_text)
                inner_html = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                html_blocks.append(f"<blockquote>{inner_html}</blockquote>")

            case "pblock":
                nodes = text_to_textnodes(block)
                inner_html = "".join(textnode_to_htmlnode(node).to_html() for node in nodes)
                html_blocks.append(f"<p>{inner_html}</p>")
                
    return "\n".join(html_blocks)
