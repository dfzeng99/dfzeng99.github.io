import json
from bs4 import BeautifulSoup, formatter

class MainPage():
    def __init__(self, setup:dict, article:str=""):
        self.setup = setup
        self.article = article
        soup = BeautifulSoup(self.__Web(), 'html.parser')
        self.web = soup.prettify(formatter=formatter.HTMLFormatter(indent=4))
    
    def __Head(self):
        temp = ""
        temp += '<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>' + '\n' # 指定字符集
        temp += '<meta content="no-transform" http-equiv="Cache-Control"/>' + '\n' # 缓存控制
        temp += '<meta content="no-siteapp" http-equiv="Cache-Control"/>' + '\n'
        temp += '<meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>' + '\n' # 指定chromium内核运行
        temp += '<meta content="webkit" name="renderer"/>' + '\n' 
        temp += '<meta content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no,minimal-ui" name="viewport"/>' + '\n' # 支持移动端设备
        temp += '<meta content="yes" name="apple-mobile-web-app-capable"/>' + '\n' 
        temp += '<meta content="black" name="apple-mobile-web-app-status-bar-style"/>' + '\n' 
        temp += '<meta content="telephone=no,email=no,adress=no" name="format-detection"/>' + '\n' 
        temp += '<meta content="#000000" name="theme-color"/>' + '\n' 
        temp += '<meta content="_top" http-equiv="window-target"/>' + '\n' 
        temp += '<title>{}</title>'.format(self.setup['Info']['Title']) + '\n' # title
        temp += '<meta content="{}" name="description"/>'.format(self.setup['Info']['Description']) + '\n' # description
        temp += '<meta content="{}" name="keywords"/>'.format(self.setup['Info']['Keywords']) + '\n' # keywords
        # Basic Components
        temp += '<link href="./resources/image/x-icon/logo.png" rel="icon" type="image/x-icon"/>' + '\n' # logo
        temp += '<link href="./css/style.css" rel="stylesheet"/>' + '\n' # css files
        temp += '<link href="./css/gitalk.min.css" rel="stylesheet"/>' + '\n'
        temp += '<link href="./css/default.min.css" rel="stylesheet"/>' + '\n'
        temp += '<link href="./css/article.css" rel="stylesheet"/>' + '\n'
        temp += '<script src="./js/highlight.min.js"></script>' + '\n' # js files
        temp += '<script>hljs.highlightAll();</script>'
        return '<head>'+'\n'+temp+'\n'+'</head>' 

    def __BodyHeader(self):
        avatar = '<a href="{}" id="avatar" target="_blank">'.format(self.setup['Link']['Github']) + '\n'\
            + '<img class="img-circle img-rotate" height="200" src="./resources/image/x-icon/logo.png" width="200"/>' + '\n'\
            +'</a>' + '\n'
        name = '<h2 class="hidden-xs hidden-sm" id="name">{}</h2>'.format(self.setup['Info']['Name']) + '\n'
        title = '<h3 class="hidden-xs hidden-sm hidden-md" id="title">{}</h3>'.format(self.setup['Info']['Professional']) + '\n'
        localtion = '<small class="text-muted hidden-xs hidden-sm" id="location"><i class="icon icon-map-marker"></i>{}</small>'.format(self.setup['Info']['Location']) + '\n'
        
        # avatar + name + title + localtion --> profile
        profile = '<div class="profile-block text-center">\n' + avatar + name + title + localtion + '</div>' 
        button = '<button aria-controls="main-navbar" aria-expanded="false" class="navbar-toggle collapsed" data-target="#main-navbar" data-toggle="collapse" type="button">\n'\
            +'<span class="sr-only">Toggle navigation</span>\n'\
            +'<span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span>\n'\
            +'</button>\n'
        
        # profile + button --> nav_header
        nav_header = '<div class="navbar-header">\n' + profile + button + '</div>\n'

        herfs = ['./index.html', './projects.html', './readlist.html', './talk.html', './about.html']
        ids = ['首页', '项目', '书单', '闲言碎语', '关于']
        icons = ['icon-home-fill', 'icon-project', 'icon-book-fill', 'icon-friendship', 'icon-cup-fill']
        nav_list = ''
        for i in range(len(herfs)):
            nav_list += '<li class="menu-item menu-item-home">'\
                +'<a href="{}">'.format(herfs[i])\
                +'<i class="icon {}"></i>'.format(icons[i])\
                +'<span class="menu-title">{}</span>'.format(ids[i])\
                +'</a></li>\n'
        nav_bar = '<nav class="collapse navbar-collapse" id="main-navbar" itemscope="" itemtype="http://schema.org/SiteNavigationElement" role="navigation">\n'\
            +'<ul class="nav navbar-nav main-nav">\n'\
            +nav_list\
            +'</ul></nav>\n'
        
        # nav_header + nav_bar --> header
        header = '<header class="header" itemscope="" itemtype="http://schema.org/WPHeader">'\
            +'<div class="slimContent">'\
            +nav_header + nav_bar\
            +'</div></header>'
        return header

    def __BodyMain(self):
        temp = '<main class="main" role="main">'+self.article+'</main>'
        return temp

    def __BodyAside(self):
        title = '<h3 class="widget-title">{}</h3>'.format(self.setup['Info']['AsideTitle'])
        content = '<div class="widget-body"><div id="board"><div class="content">{}</div></div></div>'.format(self.setup['Info']['AsideContent'])
        widget = '<div class="slimContent" style="overflow: hidden; width: auto; height: 815px;">'\
            +'<div class="widget">'+title+content+'</div></div>'
        slimScrollBar = '<div class="slimScrollBar" style="background: rgba(0, 0, 0, 0.15); width: 5px; position: absolute; top: 0px; opacity: 0.4; display: none; border-radius: 7px; z-index: 99; right: 1px; height: 436.99px;"></div>'
        slimScrollRail = '<div class="slimScrollRail" style="width: 5px; height: 100%; position: absolute; top: 0px; display: none; border-radius: 7px; background: rgb(51, 51, 51); opacity: 0.2; z-index: 90; right: 1px;"></div>'
        temp = '<aside class="sidebar" itemscope="" itemtype="http://schema.org/WPSideBar">'\
            +'<div class="slimScrollDiv" style="position: relative; overflow: hidden; width: auto; height: 815px;">'\
            +widget+slimScrollBar+slimScrollRail\
            +'</div></aside>'
        return temp
    
    def __BodyFooter(self):
        ids = ['Github', 'Weibo', 'Twitter', 'Gitee']
        icons = ['icon-github', 'icon-weibo', 'icon-qq', 'icon-gitee']
        links = ''
        for i in range(len(ids)):
            links += '<li><a data-original-title="Github" data-placement="top" data-toggle="tooltip" href="{}" target="_blank" title="">'.format(self.setup['Link'][ids[i]])\
                +'<i class="icon {}"></i></a></li>'.format(icons[i])
        links = '<ul class="social-links">'+links+'</ul>'
        copyright = '<div class="copyright"><div class="publishby">Theme by'\
            +'<a href="https://github.com/cofess" target="_blank">cofess</a>'\
            +'base on <a href="https://github.com/cofess/hexo-theme-pure" target="_blank"> pure </a> . </div> </div>'
        footer = '<footer class="footer" itemscope="" itemtype="http://schema.org/WPFooter">' + links + copyright + '</footer>'
        return footer

    def __Body(self):
        temp = '<body class="main-center" itemscope="" itemtype="http://schema.org/WebPage">'\
            +self.__BodyHeader() + self.__BodyAside() + self.__BodyMain() + self.__BodyFooter()\
            +'<script src="./js/jquery.min.js"></script><script src="./js/plugin.min.js"></script></body>'
        return temp

    def __Web(self):
        temp = '<!DOCTYPE html><html lang="zh">'+self.__Head() + self.__Body()+'</html>'
        return temp

if __name__=="__main__":
    with open('./setup.json', 'r', encoding='utf-8') as f:
        setup = json.load(f)
    web = MainPage(setup)
    with open('./{}.html'.format('test'), 'w', encoding='utf-8') as f:
        f.write(web.web)