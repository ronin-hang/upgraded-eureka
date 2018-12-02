'''

 项目 熊猫TV 英雄联盟类下 主播根据人气排名
'''
import re

from urllib import request

# 断点调试
# 强烈推荐  库:Beautiful Soup  www.crummy.com   
#          爬虫框架: scrapy  www.scrapy.org   
# 爬虫, 反爬虫, 反反爬虫
# ip 封
# 代理ip库
class Spider():
    '''
    this is a class
    '''

    # 更改lol 可以实现其他板块
    url = 'https://www.panda.tv/cate/lol'
    root_patten = '<div class="video-info">([\s\S]*?)</div>'
    name_patten = '</i>([\s\S]*?)</span>'
    number_patten = '<span class="video-number">([\s\S]*?)</span>'
    
    
    def __fetch_content(self):
        '''
        提取内容
        '''

        # This is ....
        r = request.urlopen(Spider.url)
        html = r.read()
        htmls = str(html, encoding='utf-8')
        return htmls


    def __analysis(self, htmls):
        '''
        分析内容
        '''
        root_html = re.findall(Spider.root_patten, htmls)

        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_patten, html)
            number = re.findall(Spider.number_patten, html)
            anchor = {'name':name, 'number':number}
            anchors.append(anchor)

        return anchors
       

    def __refine(self, anchors):
        '''
        精炼内容
        '''
        l = lambda anchor: {
            'name':anchor['name'][0].strip(),
            'number':anchor['number'][0]
            }
        return map(l, anchors)


    def __sort(self, anchors):
        '''
        对内容做业务处理
        '''
        anchors = sorted(anchors,
         key=self.__sort_seed,reverse=True)
        return anchors


    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number


    def __show(self, anchors):
        # for anchor in anchors:
        #     print(anchor['name'] + '...' + anchor['number'])
        for rank in range(0, len(anchors)):
            print('rank' + str(rank + 1)
            + ': '+anchors[rank]['name']
            + '  '+anchors[rank]['number'])
    

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)
        


spider = Spider()
spider.go()

# ctrl shift .   快速查找
