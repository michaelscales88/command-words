def line_by_line(filepath):
        with open(filepath) as fp:  
                for rawline in fp:
                        yield rawline.strip()

def word_by_word(filepath):
    with open(filepath) as fp:  
        for rawline in fp:
                for word in rawline.split():
                        yield word.strip()
           
