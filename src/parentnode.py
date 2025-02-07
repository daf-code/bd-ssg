from enum import Enum
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    
    def __init__(self, tag: str = "", children: list = None, props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props) #pass these up to HTMLNode for init
        #parent nodes have tags and children but no values
    
    def to_html(self) -> str:
        if self.value:
            raise ValueError("Parent node value is not allowed")
        
        if self.tag is None:
            raise ValueError("Tag is required for parent nodes") 
                
        if self.children is None:
            raise ValueError("Children are required for parent nodes") 
        
        children_html = "".join(child.to_html() for child in self.children)  
        
        if self.props is None:
            return f"<{self.tag}>{children_html}</{self.tag}>"
    
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"