import json, re
from page import MainPage
import pypandoc

test = pypandoc.convert_file("./markdown/template.md", 'html', extra_args=['--mathml'])

with open('./setup.json', 'r', encoding='utf-8') as f:
    setup = json.load(f)

def GeneratePageContent(path2article, type='article'):
    """
    path2article: path to the markdown of article.
    type: 'article' or 'linkpage'
    """
    html_convert = pypandoc.convert_file(path2article, 'html', extra_args=['--mathml'])
    html_info = re.search(r'<ul id="articleinfo">(.*?)</ul>', html_convert, flags=re.S).group()[len('<ul id="articleinfo">')+1:-len('</ul>')-1]
    html_content = re.search(r'<div id="main-content">(.*?)</div>', html_convert, flags=re.S).group()[len('<div id="main-content">')+1:-len('</div>')-1]
    html_reference = re.search(r'<ol id="reference">(.*?)</ol>', html_convert, flags=re.S).group()[len('<ol id="reference">')+1:-len('</ol>')-1]
    if type == 'article':
        with open('./cache.json', 'r', encoding='utf-8') as f:
            info_cache = json.load(f)
        info = {}
        info['title'] = re.search(r'<li id="title">(.*?)</li>', html_info, flags=re.S).group()[len('<li id="title">')+1:-len('</li>')-1]
        info['category'] = re.search(r'<li id="category">(.*?)</li>', html_info, flags=re.S).group()[len('<li id="category">')+1:-len('</li>')-1]
        info['tag'] = re.search(r'<li id="tag">(.*?)</li>', html_info, flags=re.S).group()[len('<li id="tag">')+1:-len('</li>')-1]
        info['date'] = re.search(r'<li id="date">(.*?)</li>', html_info, flags=re.S).group()[len('<li id="date">')+1:-len('</li>')-1]
        info['wordcount'] = re.search(r'<li id="wordcount">(.*?)</li>', html_info, flags=re.S).group()[len('<li id="wordcount">')+1:-len('</li>')-1]
        info_cache.append(info)
        # construct
        title = '<h1 class="article-title" itemprop="name">{}</h1>'.format(info['title'])
        date = '<span class="article-date"><i class="icon icon-calendar-check"></i><a class="article-date" href="#">'\
            +'<time datetime="0000-00-00" itemprop="datePublished">{}</time></a></span>'.format(info['date'])
        category = '<span class="article-category"><i class="icon icon-folder"></i>'\
            +'<a class="article-category-link" href="">{}</a></span>'.format(info['category'])
        tag = '<span class="article-tag"><i class="icon icon-tags"></i>'\
            '<a class="article-tag-link" href="">{}</a></span>'.format(info['tag'])
        wordcount = '<span class="post-wordcount hidden-xs" itemprop="wordCount">字数统计: {}(字)</span>'.format(info['wordcount'])
        meta = '<div class="article-meta">'+date+category+tag+wordcount+'</div>'
        header = '<div class="article-header">'+title+meta+'</div>'
        body = '<div class="article-entry marked-body" itemprop="articleBody">'+html_content+'</div>'
        footer = '<div class="article-footer"><blockquote class="mt-2x"><ul class="post-copyright list-unstyled"><li class="post-copyright-link hidden-xs">'\
            +'<strong>本文链接：</strong><a href="{0}" rel="external" target="_blank" title="{1}">{0}</a>'.format(setup['Info']['Driver']+'/'+info['title']+'.html', info['title'])\
            +'</li><li class="post-copyright-license"><strong>版权声明：</strong>本博客所有文章除特别声明外，均采用'\
            +'<a href="http://creativecommons.org/licenses/by/4.0/deed.zh" rel="external" target="_blank">CC BY 4.0 CN协议</a>'\
            +'许可协议。转载请注明出处！</li></ul></blockquote></div>'
        article = '<article id="post-{}" class="article article-type-post" itemscope=""itemtype="http://schema.org/BlogPosting">'.format(info['title'])\
            +header+body+footer+'</article>'
        html_article = '<div class="content">'+article+'</div>'
        html_page = MainPage(setup, html_article, html_reference)
        with open('./html/{}.html'.format(info['title']), 'w', encoding='utf-8') as f:
            f.write(html_page.web)
        with open('cache.json', 'w', encoding='utf-8') as f:
            json.dump(info_cache, f, indent=4)
    elif type == 'linkpage':
        info = {}
        info['title'] = re.search(r'<li id="title">(.*?)</li>', html_info, flags=re.S).group()[len('<li id="title">')+1:-len('</li>')-1]
        html_article = '<div class="content"><article id="post-linkpage" class="article article-type-post" itemscope=""itemtype="http://schema.org/BlogPosting">'+html_content\
            +'</article></div>'
        html_page = MainPage(setup, html_article)
        with open('./{}.html'.format(info['title']), 'w', encoding='utf-8') as f:
            f.write(html_page.web)
    else:
        pass

# GeneratePageContent('./markdown/template.md')