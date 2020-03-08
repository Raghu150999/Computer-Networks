from bs4 import BeautifulSoup

def html_parser(doc):
    '''
    Takes in html doc as input and returns list of all images srcs found.
    Args:
        doc: html doc to parse
    '''
    soup = BeautifulSoup(doc, 'html.parser')
    imgs = soup.find_all('img')
    srcs = [img.get('src') for img in imgs]
    return srcs

if __name__ == "__main__":
    f = open('output_dir/index.html', 'r')
    doc = f.read()
    f.close()
    srcs = html_parser(doc)
    print(srcs)