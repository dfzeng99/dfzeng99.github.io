import json, re
from page import MainPage
import pypandoc

test = pypandoc.convert_file("./markdown/template.md", 'html', extra_args=['--mathml'])

with open('./setup.json', 'r', encoding='utf-8') as f:
    setup = json.load(f)
web = MainPage(setup, article=test)

with open('./{}.html'.format('test'), 'w', encoding='utf-8') as f:
    f.write(web.web)

def GenerateArticle(path2article):
    pass
