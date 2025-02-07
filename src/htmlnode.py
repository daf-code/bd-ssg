from enum import Enum

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f'''HTMLNode(tag={self.tag}, 
        value={self.value}, 
        children={self.children}, 
        props={self.props}'''

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")
    
#props_to_html: should print string of props in format of key="value" with a leading space and separated by spaces    
    # def props_to_html(self):
    #     if self.props:
    #         return " "+" ".join([f"{key}='{value}'" for key, value in self.props.items()])
    #     return "" #if no props, return empty string 

    def props_to_html(self):
        if self.props:
            props_strings = [f"{key}='{value}'" for key, value in self.props.items()]
            return " " + " ".join(props_strings)
        return "" #if no props, return empty string 