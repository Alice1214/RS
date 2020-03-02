# !/usr/bin/env python
# -*- coding=utf-8 -*-
# Content：从腾讯新闻接口获取当天疫情数据，并利用pyecharts进行可视化呈现
# Author:  HuiHui
# Date:    2020-02-17
# Reference:

import requests
import json    # 处理json格式数据（树状）
import pandas as pd
import numpy as np

from pyecharts import options as opts  # ⚠️pyecharts安装参考https://pyecharts.org/#/zh-cn/quickstart
from pyecharts.charts import Pie,Page,WordCloud,Line,Map
from pyecharts.components import Table
from pyecharts.globals import ThemeType # 使用主题

######## 数据获取 ##############################

#定义获取json数据的函数
def get_html_text(url):
    try:
        res = requests.get(url, timeout=30) #30s后超时
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return "Error"

#获取中国各省份、地区的信息；返回list,list中每个元素是包含某一个省份/城市/区疫情信息的dict
def parse_areaTree():
    result=[]
    province_data=[]
    for country in areaTree_json:
        if(country["name"]=="中国"):
            province_json=country["children"]
            for province in province_json:
                area_json=province["children"]
                province_data.append({'province': province['name'],'province_confirm':province['total']['confirm']})
                for area in area_json:
                    country_name = '中国'
                    province_name= province["name"]
                    area_name=area["name"]
                    confirm=area["total"]["confirm"]
                    suspect=area["total"]["suspect"]
                    dead=area["total"]["dead"]
                    heal=area["total"]["heal"]
                    temp = {'city': area_name, 'province': province_name, 'country': country_name,'confirm': confirm, 'heal': heal, 'dead': dead, 'suspect': suspect,'update_time': update_time}
                    result.append(temp)
    return result,province_data

page_url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5" #打开开发者工具，刷新页面，找到相应的json文件
text = get_html_text(page_url)
#提取json数据中的data字段
data_json = json.loads(text)["data"] #⚠️json.loads（）是将json转化为python字典,这里得到的是data对应的json数据，str类型
data_dict = json.loads(data_json)
#更新时间
update_time=data_dict["lastUpdateTime"]
#国内每日信息汇总
chinaTotal_json=data_dict["chinaTotal"] #dict类型
confirmCount = str(chinaTotal_json["confirm"])
suspectCount = str(chinaTotal_json["suspect"])
deadCount = str(chinaTotal_json["dead"])
heal = str(chinaTotal_json["heal"])

print("更新时间：" + update_time + "\n" + "确诊人数为：" + confirmCount + "人\n" + "死亡人数为：" + deadCount + "人\n" + \
    "疑似人数为：" + suspectCount + "人\n" + "治愈人数为：" + heal + "人\n" )

# 获取中国各省份、地区的所有信息，且国家为首索引
areaTree_json=data_dict["areaTree"] #dict类型
result,province_data = parse_areaTree()
province_data=pd.DataFrame(province_data)
# 写入CSV
data = pd.DataFrame(result,columns=['city', 'province', 'country','confirm', 'dead', 'heal','suspect','update_time']) #转换成DataFrame对象,并指定列的顺序
#print(data)
data.to_csv('city.csv')

#获取累计确诊和现存确诊时间序列
chinaDayList_json=data_dict["chinaDayList"]
chinaDayList_data=pd.DataFrame(chinaDayList_json,columns=['confirm','nowConfirm','date'])

########## 利用pyecharts数据可视化 #########################

#饼图
columns = ["累计确诊", "现存疑似", "累计死亡", "累计治愈"]
data1 = [confirmCount,suspectCount,deadCount,heal]
pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.WHITE,bg_color="transparent")).add("",[list(z) for z in zip(columns, data1)],center=["50%", "50%"], radius=["0%", "70%"])
pie = pie.set_global_opts(title_opts=opts.TitleOpts(title="全国汇总"))
pie = pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

#中间大标题，副标题（time）
big_title=Pie().set_global_opts(title_opts=opts.TitleOpts(title="新型冠状病毒肺炎疫情数据",title_textstyle_opts=opts.TextStyleOpts(font_size=40)))
times = Pie().set_global_opts(title_opts=opts.TitleOpts(subtitle=("截至 " + update_time),subtitle_textstyle_opts=opts.TextStyleOpts(font_size=13)))

#表
headers=["地区", "累计确诊", "死亡", "治愈"]
rows=np.array(pd.DataFrame(result,columns=['city','confirm','dead','heal']))
table=Table(page_title="新型冠状病毒肺炎疫情数据").add(headers, rows[0:50][:]).set_global_opts(title_opts=opts.ComponentTitleOpts(title="中国各地区疫情数据"))

#词云
area=np.array(data['city'])
area_confirm=[int(z) for z in np.array(data['confirm'])]#⚠️这里numpy.int64类型不能直接用
words_confirm=[tuple(z) for z in zip(area,area_confirm)]
wordcloud_confirm=WordCloud().add("", words_confirm, word_size_range=[20, 100]).set_global_opts(title_opts=opts.TitleOpts(title="累计确诊"))

#折线图
confirmList=[int(z) for z in chinaDayList_data['confirm']]
cnowConfirmList=[int(z) for z in chinaDayList_data['nowConfirm']]
line=Line().add_xaxis(list(chinaDayList_data['date'])).add_yaxis(series_name="累计确诊", y_axis=confirmList,is_symbol_show=False,symbol='circle').add_yaxis(series_name="现存确诊", y_axis=cnowConfirmList,is_symbol_show=False,symbol='circle').set_global_opts(title_opts=opts.TitleOpts(title="全国疫情趋势"))

#疫情地图
province=list(province_data['province'])
province_confirm=[int(z) for z in province_data['province_confirm']]
map=Map().add("累计确诊", [list(z) for z in zip(province,province_confirm)], "china",is_map_symbol_show=False,
             tooltip_opts=opts.TooltipOpts(is_show=True),zoom=1.2).set_series_opts(label_opts=opts.LabelOpts(is_show=False)).set_global_opts(title_opts=opts.TitleOpts(title="中国疫情分布"
             ),visualmap_opts=opts.VisualMapOpts(is_piecewise=True,textstyle_opts=opts.TextStyleOpts(color="black"),
                pieces=[{"min": 1001, "label": '>1000', "color": "#893448"},
                        {"min": 500, "max": 1000, "label": '500-1000',"color": "#ff585e"},
                        {"min": 101, "max": 499, "label": '101-499',"color": "#fb8146"},
                        {"min": 10, "max": 100, "label": '10-100',"color": "#ffb248"},
                        {"min": 0, "max": 9, "label": '0-9',"color": "#fff2d1"}]))

#页面图表组合
#page = Page(page_title="新型冠状病毒肺炎疫情数据",layout=Page.DraggablePageLayout) # page_title是HTML 标题;DraggablePageLayout拖动页面布局
page = Page(page_title="新型冠状病毒肺炎疫情数据")
page=page.add(big_title,times,pie,table,wordcloud_confirm,line,map)


#page.render()#⚠️生成render.html文件，浏览器中打开即可看到视图；拖拉/调整图表位置和大小；下载 chart_config.json 配置文件放到当前文件位置；重新渲染即可
page.save_resize_html("render.html",cfg_file="chart_config.json",dest="新型冠状病毒肺炎疫情数据.html")#DraggablePageLayout布局重新渲染

# ❓pyecharts怎么绘制可折叠展开的表格



