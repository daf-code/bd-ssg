from enum import Enum
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    
    def __init__(self, tag: str = None, value: str = None, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)  # Fix the order of arguments
        #leaf nodes don't have children
    
    def to_html(self):
        
        if self.value == None:
            raise ValueError("Leaf node value is required")
        
        if self.tag == None and self.props != None:
            raise ValueError("Cannot have props without a tag")
        
        if self.tag == None:
            return f"{self.value}"
  # The issue might be here - we're checking if props is None, but what if it's an empty dict?
       # print(f"Debug - props is None?: {self.props is None}")
        #print(f"Debug - props type: {type(self.props)}")
    
        if self.props == None:  # This condition might be the problem
            return f"<{self.tag}>{self.value}</{self.tag}>"
    
        props_str = self.props_to_html()
        #print(f"Debug - props_str: {props_str}")
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"