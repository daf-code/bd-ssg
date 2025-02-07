import src.textnode as textnode


def main():
    text = textnode.TextNode("hello world", textnode.TextType.NORMAL)
    print(text)

if __name__ == "__main__": # if the file is run directly then run the main function
    main()  
# hello world textnode
