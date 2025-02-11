import unittest
from ssg_handlers import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_link, split_nodes_image 
from ssg_handlers import text_to_textnodes, markdown_to_blocks, detect_block_type, markdown_to_html
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter_1(self):
    # Test 1: Basic code block
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is text with a "
        assert new_nodes[0].text_type == TextType.NORMAL
        #print(f"Split Node Debug: {repr(new_nodes[1].text)}")
        assert new_nodes[1].text == "code block"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " word"
        assert new_nodes[2].text_type == TextType.NORMAL

    # def test_split_nodes_delimiter_2(self):
    # # Test 2: Multiple delimiters
    #     node = TextNode("Hello **world** and **python**", TextType.NORMAL)
    #     new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    #     assert len(new_nodes) == 5
    #     assert new_nodes[0].text == "Hello "
    #     assert new_nodes[1].text == "world"
    #     assert new_nodes[2].text == " and "
    #     assert new_nodes[3].text == "python"
    #     assert new_nodes[4].text == ""

    def test_split_nodes_delimiter_3(self):
    # Test 3: No delimiters
        node = TextNode("Plain text here", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "Plain text here"

    def test_split_nodes_delimiter_4(self):
    # Test 4: Invalid markdown (unmatched delimiters)
        node = TextNode("Hello *world", TextType.NORMAL)
        try:
            split_nodes_delimiter([node], "*", TextType.ITALIC)
            assert False, "Expected ValueError"
        except ValueError:
            assert True
    def test_split_nodes_delimiter_5(self):
    # Test 5: Leading delimiter
        node = TextNode("**Bold text** normal text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 2
        assert new_nodes[0].text == "Bold text"
        assert new_nodes[0].text_type == TextType.BOLD
        assert new_nodes[1].text == " normal text" 
        assert new_nodes[1].text_type == TextType.NORMAL

    def test_split_nodes_delimiter_6(self):
    # Test 6: Trailing delimiter
        node = TextNode("normal text **Bold text**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 2
        assert new_nodes[0].text == "normal text "
        assert new_nodes[0].text_type == TextType.NORMAL
        assert new_nodes[1].text == "Bold text"
        assert new_nodes[1].text_type == TextType.BOLD

    # def test_split_nodes_delimiter_7(self):
    # # Test 7: Empty delimiters
    #     node = TextNode("text with **** empty bold", TextType.NORMAL)
    #     new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    #     assert len(new_nodes) == 3
    #     assert new_nodes[0].text == "text with "
    #     assert new_nodes[0].text_type == TextType.NORMAL
    #     assert new_nodes[1].text == ""
    #     assert new_nodes[1].text_type == TextType.BOLD
    #     assert new_nodes[2].text == " empty bold"
    #     assert new_nodes[2].text_type == TextType.NORMAL

    # def test_split_nodes_delimiter_8(self):
    # # Test 8: Multiple nodes in input
    #     node1 = TextNode("Hello **world**", TextType.NORMAL)
    #     node2 = TextNode("This is *italic*", TextType.NORMAL)
    #     node3 = TextNode("**bold** again", TextType.NORMAL)
    #     nodes = [node1, node2, node3]
    #     new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    #     assert len(new_nodes) == 7
    #     assert new_nodes[0].text == "Hello "
    #     assert new_nodes[0].text_type == TextType.NORMAL
    #     assert new_nodes[1].text == "world"
    #     assert new_nodes[1].text_type == TextType.BOLD
    #     assert new_nodes[2].text == "This is *italic*"  # Leaves other delimiters untouched
    #     assert new_nodes[2].text_type == TextType.NORMAL
    #     assert new_nodes[3].text == "bold"
    #     assert new_nodes[3].text_type == TextType.BOLD
    #     assert new_nodes[4].text == " again"
    #     assert new_nodes[4].text_type == TextType.NORMAL

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links_empty_1(self):
        assert extract_markdown_links("") == []
    def test_extract_markdown_links_single_link_2(self):
        assert extract_markdown_links("[text](url)") == [("text", "url")]
    def test_extract_markdown_links_multiple_links_3(self):
        test_text = "[link1](url1) [link2](url2)"
        assert extract_markdown_links(test_text) == [("link1", "url1"), ("link2", "url2")]
    def test_extract_markdown_links_none_4(self):
        assert extract_markdown_links("plain text") == []
    def test_extract_markdown_links_mixed_content_5(self): # Mixed content test 
        test_text = "![img](img.jpg) [link](url)"
        assert extract_markdown_links(test_text) == [("link", "url")]

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images_empty_1(self):
        assert extract_markdown_images("") == []
    def test_extract_markdown_images_single_image_2(self):
        assert extract_markdown_images("![alt](url)") == [("alt", "url")]
    def test_extract_markdown_images_multiple_images_3(self):
        test_text = "![alt1](url1) ![alt2](url2)"
        assert extract_markdown_images(test_text) == [("alt1", "url1"), ("alt2", "url2")]
    def test_extract_markdown_images_none_4(self):
        assert extract_markdown_images("plain text") == []
    def test_extract_markdown_images_mixed_content_5(self):
        test_text = "![img](img.jpg) [link](url)"
        assert extract_markdown_images(test_text) == [("img", "img.jpg")]


class TestSplitNodesLink(unittest.TestCase):
    def test_no_links(self):
        # Test text with no links
        nodes = [TextNode("This is plain text without any links", TextType.NORMAL)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is plain text without any links")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_links_different_positions(self):
        # Test links at start, middle, and end
        input_text = "[Start](start.com) middle text [Middle](middle.com) more text [End](end.com)"
        nodes = [TextNode(input_text, TextType.NORMAL)]
        result = split_nodes_link(nodes)
        
        expected = [
            TextNode("Start", TextType.LINK, "start.com"),
            TextNode(" middle text ", TextType.NORMAL),
            TextNode("Middle", TextType.LINK, "middle.com"),
            TextNode(" more text ", TextType.NORMAL),
            TextNode("End", TextType.LINK, "end.com")
        ]
        
        self.assertEqual(len(result), 5)
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            if expected[i].text_type == TextType.LINK:
                self.assertEqual(result[i].url, expected[i].url)

    def test_back_to_back_links(self):
        # Test consecutive links without space between them
        input_text = "[Link1](url1.com)[Link2](url2.com)"
        nodes = [TextNode(input_text, TextType.NORMAL)]
        result = split_nodes_link(nodes)
        
        expected = [
            TextNode("Link1", TextType.LINK, "url1.com"),
            TextNode("Link2", TextType.LINK, "url2.com")
        ]
        
        self.assertEqual(len(result), 2)
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)

    def test_only_normal_text(self):
        # Test with multiple nodes of normal text
        nodes = [
            TextNode("First normal text", TextType.NORMAL),
            TextNode("Second normal text", TextType.NORMAL)
        ]
        result = split_nodes_link(nodes)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "First normal text")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "Second normal text")
        self.assertEqual(result[1].text_type, TextType.NORMAL)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_single_1(self):
        # Test a single image conversion
        node = TextNode("![alt text](https://example.com/image.png)", TextType.NORMAL)
        nodes = split_nodes_image([node])
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(nodes[0].url, "https://example.com/image.png")

    def test_split_nodes_image_text_before_2(self):
        # Test text before image
        node = TextNode("Hello ![alt text](https://example.com/image.png)", TextType.NORMAL)
        nodes = split_nodes_image([node])
        
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(nodes[1].text, "")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/image.png")

    def test_split_nodes_image_text_after_3(self):
        # Test text after image
        node = TextNode("![alt text](https://example.com/image.png) World", TextType.NORMAL)
        nodes = split_nodes_image([node])
        
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(nodes[0].url, "https://example.com/image.png")
        self.assertEqual(nodes[1].text, " World")
        self.assertEqual(nodes[1].text_type, TextType.NORMAL)

    def test_split_nodes_image_text_both_sides_4(self):
        # Test text on both sides of image
        node = TextNode("Hello ![alt text](https://example.com/image.png) World", TextType.NORMAL)
        nodes = split_nodes_image([node])
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(nodes[1].text, "")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/image.png")
        self.assertEqual(nodes[2].text, " World")
        self.assertEqual(nodes[2].text_type, TextType.NORMAL)

    def test_split_nodes_multiple_images_5(self):
        print("\nStarting test_split_nodes_multiple_images_5")
        # Test multiple images in one node
        input_text = "![first](https://example.com/1.png) middle ![second](https://example.com/2.png)"
        print(f"Input text: {input_text}")
        
        node = TextNode(input_text, TextType.NORMAL)
        nodes = split_nodes_image([node])
        
        print("\nTest 5 Resulting nodes:")
        for i, n in enumerate(nodes):
            print(f"Node {i}: text='{n.text}', type={n.text_type}, url={getattr(n, 'url', None)}")
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(nodes[0].url, "https://example.com/1.png")
        self.assertEqual(nodes[1].text, " middle ")
        self.assertEqual(nodes[1].text_type, TextType.NORMAL)
        self.assertEqual(nodes[2].text, "")
        self.assertEqual(nodes[2].text_type, TextType.IMAGE)
        self.assertEqual(nodes[2].url, "https://example.com/2.png")

    def test_split_nodes_no_images_6(self):
        # Test text without any images
        node = TextNode("Just plain text", TextType.NORMAL)
        nodes = split_nodes_image([node])
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Just plain text")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)

    def test_split_nodes_empty_text_7(self):
        # Test empty text
        node = TextNode("", TextType.NORMAL)
        nodes = split_nodes_image([node])
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)

    def test_split_nodes_multiple_nodes_8(self):
        # Test multiple input nodes
        nodes = [
            TextNode("First ![alt1](https://example.com/1.png)", TextType.NORMAL),
            TextNode("Second ![alt2](https://example.com/2.png)", TextType.NORMAL)
        ]
        result = split_nodes_image(nodes)
        
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "First ")
        self.assertEqual(result[1].text, "")
        self.assertEqual(result[1].url, "https://example.com/1.png")
        self.assertEqual(result[2].text, "Second ")
        self.assertEqual(result[3].text, "")
        self.assertEqual(result[3].url, "https://example.com/2.png")

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_1(self):
    # Test 1: Plain text without any formatting
        input_text = "This is plain text."
        output_nodes = text_to_textnodes(input_text)
        print(output_nodes)  
    # Expect: [TextNode("This is plain text.", TextType.TEXT)]

    def test_text_to_textnodes_2(self):
    # Test 2: Bold text (`**` delimiters)
        input_text = "This text is **bold**."
        output_nodes = text_to_textnodes(input_text)
        print(output_nodes)
    # Expect: [
    #     TextNode("This text is ", TextType.TEXT),
    #     TextNode("bold", TextType.BOLD),
    #     TextNode(".", TextType.TEXT)
    # ]

    def test_text_to_textnodes_3(self): 
    # Test 3: Mixed types (italic and bold)
        input_text = "This is *italic* and this is **bold**."
        output_nodes = text_to_textnodes(input_text)
        print(output_nodes)
    # Expect: [
    #     TextNode("This is ", TextType.TEXT),
    #     TextNode("italic", TextType.ITALIC),
    #     TextNode(" and this is ", TextType.TEXT),
    #     TextNode("bold", TextType.BOLD),
    #     TextNode(".", TextType.TEXT)
    # ]

    def test_text_to_textnodes_4(self):
    # Test 4: Code block (` backticks)
        input_text = "This `code` is in a block."
        output_nodes = text_to_textnodes(input_text)
        print(output_nodes)
    # Expect: [
    #     TextNode("This ", TextType.TEXT),
    #     TextNode("code", TextType.CODE),
    #     TextNode(" is in a block.", TextType.TEXT)
    # ]

    def test_text_to_textnodes_5(self):
    # Test 5: Image
        input_text = "![image description](https://example.com/image.png)"
        output_nodes = text_to_textnodes(input_text)
        print(output_nodes)
    # Expect: [
    #     TextNode("image description", TextType.IMAGE, "https://example.com/image.png")
    # ]
    input_text = "Visit [Boot.dev](https://boot.dev) for learning."
    output_nodes = text_to_textnodes(input_text)
    print(output_nodes)
    # Expect: [
    #     TextNode("Visit ", TextType.TEXT),
    #     TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
    #     TextNode(" for learning.", TextType.TEXT)
    # ]

    # Test 7: Mixed content with all node types
    input_text = "Here is *italic*, **bold**, `code`, ![image](https://img.com) and a [link](https://link.com)."
    output_nodes = text_to_textnodes(input_text)
    print(output_nodes)
    # Expect: [
    #     TextNode("Here is ", TextType.TEXT),
    #     TextNode("italic", TextType.ITALIC),
    #     TextNode(", ", TextType.TEXT),
    #     TextNode("bold", TextType.BOLD),
    #     TextNode(", ", TextType.TEXT),
    #     TextNode("code", TextType.CODE),
    #     TextNode(", ", TextType.TEXT),
    #     TextNode("image", TextType.IMAGE, "https://img.com"),
    #     TextNode(" and a ", TextType.TEXT),
    #     TextNode("link", TextType.LINK, "https://link.com"),
    #     TextNode(".", TextType.TEXT)
    # ]

    # Test 8: Edge case with unmatched delimiters
    input_text = "This text has *unmatched delimiters."
    try:
        output_nodes = text_to_textnodes(input_text)
    except ValueError as e:
        print(e)  # Expect: "Invalid markdown: unmatched delimiters"

    # Test 9: Empty input
    input_text = ""
    output_nodes = text_to_textnodes(input_text)
    print(output_nodes)
    # Expect: []  (an empty list, as there's no content)

    # Test 10: Overlapping delimiters (ambiguous markdown)
    input_text = "**bold*italic**"
    try:
        output_nodes = text_to_textnodes(input_text)
    except ValueError as e:
        print(e)
        # Expect: "Invalid markdown: unmatched delimiters"
    # The rationale: If the function sees `**bold` as bold and leaves a lone `*`, this is invalid based on the lesson instructions
    # not to try to handle unmatched delimiters. An error should be raised.

   
    # Test 10: Overlapping delimiters (ambiguous markdown)
    input_text = "**bold*italic**"
    try:
        output_nodes = text_to_textnodes(input_text)
    except ValueError as e:
        print(e)
        # Expect: "Invalid markdown: unmatched delimiters"
    # The rationale: If the function sees `**bold` as bold and leaves a lone `*`, this is invalid based on the lesson instructions
    # not to try to handle unmatched delimiters. An error should be raised.

    # Test 11: Multiple images in a row
    input_text = "![img](https://img1.com) and ![pic](https://img2.com)."
    output_nodes = text_to_textnodes(input_text)
    print(output_nodes)
    # Expect: [
    #     TextNode("img", TextType.IMAGE, "https://img1.com"),
    #     TextNode(" and ", TextType.TEXT),
    #     TextNode("pic", TextType.IMAGE, "https://img2.com"),
    #     TextNode(".", TextType.TEXT)
    # ]

    # Test 12: Nested delimiters (not handled)
    input_text = "This is **bold *and italic*** text."
    try:
        output_nodes = text_to_textnodes(input_text)
    except ValueError as e:
        print(e)
        # Expect: "Invalid markdown: nested delimiters not supported"
    # Nested delimiters like `**bold *italic***` are not supported as per the lesson instructions.

    # # Test 13: Escaped delimiters -- not required by the lesson
    # input_text = "Use \\*this\\* to escape *italic*."
    # output_nodes = text_to_textnodes(input_text)
    # print(output_nodes)
    # # Expect: [
    # #     TextNode("Use *this* to escape ", TextType.TEXT),
    # #     TextNode("italic", TextType.ITALIC),
    # #     TextNode(".", TextType.TEXT)
    # # ]
    # # Rationale: Ensure the function does NOT treat `\\*` as a delimiter but processes it as literal text.

    # Test 14: Content-heavy input
    input_text = (
        "Here is **bold text**, *italic text*, `inline code`, "
        "a ![sample image](https://example.com/image.png), and "
        "a [helpful link](https://example.com). Plus some plain text!"
    )
    output_nodes = text_to_textnodes(input_text)
    print(output_nodes)
    # Expect: [
    #     TextNode("Here is ", TextType.TEXT),
    #     TextNode("bold text", TextType.BOLD),
    #     TextNode(", ", TextType.TEXT),
    #     TextNode("italic text", TextType.ITALIC),
    #     TextNode(", ", TextType.TEXT),
    #     TextNode("inline code", TextType.CODE),
    #     TextNode(", a ", TextType.TEXT),
    #     TextNode("sample image", TextType.IMAGE, "https://example.com/image.png"),
    #     TextNode(", and a ", TextType.TEXT),
    #     TextNode("helpful link", TextType.LINK, "https://example.com"),
    #     TextNode(". Plus some plain text!", TextType.TEXT)
    # ]
    # Rationale: This covers the full spectrum of possible markdown sequences handled by your function—bold, italic, code, image, link, and plain text.
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic_1(self):
        input_text = '''
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
        output_blocks = markdown_to_blocks(input_text)
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(output_blocks, expected_blocks)

    def test_markdown_to_blocks_multiple_blank_lines_2(self):
        input_text = '''# Heading


    
Next block'''
        expected_blocks = [
            "# Heading",
            "Next block"
        ]
        self.assertEqual(markdown_to_blocks(input_text), expected_blocks)

    def test_markdown_to_blocks_whitespace_handling_3(self):
        input_text = '''   # Heading with spaces    

        * List with indentation
        * Second item    
            * Indented item   '''
        expected_blocks = [
            "# Heading with spaces",
            "* List with indentation\n* Second item\n* Indented item"
        ]
        self.assertEqual(markdown_to_blocks(input_text), expected_blocks)

    def test_markdown_to_blocks_single_block_4(self):
        input_text = "Just one block of text"
        expected_blocks = ["Just one block of text"]
        self.assertEqual(markdown_to_blocks(input_text), expected_blocks)

    def test_markdown_to_blocks_only_whitespace_5(self):
        input_text = """
        
            
        
        """
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(input_text), expected_blocks)

    def test_markdown_to_blocks_mixed_indentation_6(self):
        input_text = """# Heading

    * Tab indented item
    * Space indented item
    * Mixed indentation
    * Weird spacing"""
        
        expected_blocks = [
            "# Heading",
            "* Tab indented item\n* Space indented item\n* Mixed indentation\n* Weird spacing"
        ]
        self.assertEqual(markdown_to_blocks(input_text), expected_blocks)

class TestDetectBlockType(unittest.TestCase):

    def combined_block_handling_1(self):
    # Test headings
        assert detect_block_type("# Heading 1") == "hblock"
        assert detect_block_type("### Heading 3") == "hblock"
        assert detect_block_type("#Invalid heading") == "pblock"  # no space
        
    # Test code blocks
        assert detect_block_type("```\nsome code\n```") == "codeblock"
        assert detect_block_type("```\nno end") == "pblock"
        
    # Test unordered lists
        assert detect_block_type("* Item 1\n* Item 2") == "ulblock"
        assert detect_block_type("- Item 1\n- Item 2") == "ulblock"
        assert detect_block_type("* Item 1\n- Item 2") == "ulblock"
        
    # Test ordered lists
        assert detect_block_type("1. First\n2. Second") == "olblock"
        assert detect_block_type("1. Only one") == "olblock"
        assert detect_block_type("1. First\n3. Third") == "pblock"  # wrong sequence
        
    # Test quotes
        assert detect_block_type(">Quote line") == "qblock"
        assert detect_block_type("> Quote line") == "qblock"
        assert detect_block_type(">Line 1\n>Line 2") == "qblock"

    # Test paragraphs (default)
        assert detect_block_type("Just some text") == "pblock"

    #problem cases
        # Edge cases for headings
        assert detect_block_type("###### Six hashes") == "hblock"
        assert detect_block_type("####### Seven hashes") == "pblock"
        
        # Edge cases for lists
        assert detect_block_type("1. First\n2.Second") == "pblock"  # missing space after period
        assert detect_block_type("* Item\n*No space") == "pblock"   # missing space after asterisk
        
        # Edge cases for code blocks
        assert detect_block_type("```\n```") == "codeblock"         # empty code block
        assert detect_block_type("````\n```") == "pblock"           # wrong number of backticks
        
        # Edge cases for quotes
        assert detect_block_type(">") == "qblock"                   # empty quote
        assert detect_block_type(">\n>") == "qblock"               # multi-line empty quote

class TestMarkdownToHtml(unittest.TestCase):
    def test_md_to_html_empty_input_1(self):
        self.assertEqual(markdown_to_html(""), "")

    def test_md_to_html_basic_blocks_2(self):
        input_text = """
# Heading
Simple paragraph.
"""
        expected_html = "<h1>Heading</h1>\n<p>Simple paragraph.</p>"
        self.assertEqual(markdown_to_html(input_text), expected_html)

    def test_md_to_html_text_formatting_3(self):
        input_text = "Text with **bold**, *italic*, and `code`."
        expected_html = "<p>Text with <strong>bold</strong>, <em>italic</em>, and <code>code</code>.</p>"
        self.assertEqual(markdown_to_html(input_text), expected_html)

    def test_md_to_html_nested_lists_4(self):
        input_text = """
* Level 1
    * Level 2
    * Level 2
        * Level 3
* Level 1
"""
        expected_html = "<ul>\n<li>Level 1</li>\n<li>Level 2</li>\n<li>Level 2</li>\n<li>Level 3</li>\n<li>Level 1</li>\n</ul>"
        self.assertEqual(markdown_to_html(input_text), expected_html)

    def test_md_to_html_complex_blockquote_5(self):
        input_text = """> First paragraph
>
> Second paragraph with **bold**
> - List item 1
> - List item 2
"""
        expected_html = "<blockquote>\n<p>First paragraph</p>\n<p>Second paragraph with <strong>bold</strong></p>\n<ul>\n<li>List item 1</li>\n<li>List item 2</li>\n</ul>\n</blockquote>"
        self.assertEqual(markdown_to_html(input_text), expected_html)

    def test_md_to_html_links_and_images_6(self):
        input_text = """[Link](https://example.com)
![](image.jpg)
Text with inline ![](inline.jpg) image."""
        space_format = "<p><a href='https://example.com'>Link</a> <img src='image.jpg' alt='Image'> Text with inline <img src='inline.jpg' alt='Image'> image.</p>"
        newline_format = "<p><a href='https://example.com'>Link</a>\n<img src='image.jpg' alt='Image'>\nText with inline <img src='inline.jpg' alt='Image'> image.</p>"
        actual = markdown_to_html(input_text)
        self.assertTrue(
            actual == space_format or actual == newline_format,
            f"Expected either\n{space_format}\nor\n{newline_format}\nbut got\n{actual}"
        )

    def test_invalid_markdown_7(self):
        with self.assertRaises(ValueError):
            markdown_to_html("**unclosed bold")

if __name__ == "__main__":
    unittest.main()