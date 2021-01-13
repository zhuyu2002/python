#coding:utf-8
"""
综合项目:世行历史数据基本分类及其可视化
作者：朱渝
日期：2021/1/13

"""

import csv
import math
import pygal
import pygal_maps_world  #导入需要使用的库


def read_csv_as_nested_dict(filename, keyfield, separator, quote): #读取原始csv文件的数据，格式为嵌套字典
    """
    输入参数:
      filename:csv文件名
      keyfield:键名
      separator:分隔符
      quote:引用符

    输出:
      读取csv文件数据，返回嵌套字典格式，其中外层字典的键对应参数keyfiled，内层字典对应每行在各列所对应的具体值
    """
    result={}
    with open(filename,newline="")as csvfile:
        csvreader=csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
        for row in csvreader:
            rowid=row[keyfield]
            result[rowid]=row

    return result
def reconcile_countries_by_name(plot_countries, gdp_countries): #返回在世行有GDP数据的绘图库国家代码字典，以及没有世行GDP数据的国家代码集合
    """
    
    输入参数:
    plot_countries: 绘图库国家代码数据，字典格式，其中键为绘图库国家代码，值为对应的具体国名
    gdp_countries:世行各国数据，嵌套字典格式，其中外部字典的键为世行国家代码，值为该国在世行文件中的行数据（字典格式)
    
    输出：
    返回元组格式，包括一个字典和一个集合。其中字典内容为在世行有GDP数据的绘图库国家信息（键为绘图库各国家代码，值为对应的具体国名),
    集合内容为在世行无GDP数据的绘图库国家代码
    """
    empty=[]
    gdp_countries_names=[]
    for i in gdp_countries.values():                    #for循环于gdp值中以使世行中国家名字存入列表中
        gdp_countries_names.append(i["Country Name"])
    for m in list(plot_countries):                      #for循环于plot中，判断世行国家名字是否能在绘图库中得到
        if plot_countries[m] not in gdp_countries_names:
            empty.append(m)                             #在empty列表中加入不能在绘图库中得到的世行国家名字
            plot_countries.pop(m)                       #删除不能得到国家名字的值
    result=(plot_countries,empty)        #输出结果
    return result
    # 编码，结束后将pass删除
    # 不要忘记返回结果
def build_map_dict_by_name(gdpinfo, plot_countries, year,gdp_countries,reconcile_countries):
    """
    输入参数:
    gdpinfo: 
	plot_countries: 绘图库国家代码数据，字典格式，其中键为绘图库国家代码，值为对应的具体国名
	year: 具体年份值
	
    输出：
    输出包含一个字典和二个集合的元组数据。其中字典数据为绘图库各国家代码及对应的在某具体年份GDP产值（键为绘图库中各国家代码，值为在具体年份（由year参数确定）所对应的世行GDP数据值。为
    后续显示方便，GDP结果需转换为以10为基数的对数格式，如GDP原始值为2500，则应为log2500，ps:利用math.log()完成)
    2个集合一个为在世行GDP数据中完全没有记录的绘图库国家代码，另一个集合为只是没有某特定年（由year参数确定）世行GDP数据的绘图库国家代码

   """
    no_gdp_year=[]
    for i in gdp_countries.values():                            #for循环遍历gdp值
        for m in list(plot_countries):                          #for循环遍历plot键
            if i[gdpinfo["country_name"]]==plot_countries[m]:     #如果gdp值中有plot中的国家，进入年份查询
                if i[year] == "":                                 #指定年数据为空时，进行的操作
                    no_gdp_year.append(m)                           #在no_gdp_append列表中插入指定年为空的国家代码
                    plot_countries.pop(m)                           #删除plot中数据为空的国家代码
                else:
                    plot_countries[m]=str(math.log(float(i[year])))    #将指定有数据的值进行log
    result=(plot_countries,reconcile_countries[1],no_gdp_year)   #输出结果
    return result

    # 编码，结束后将pass删除
    # 不要忘记返回结果
def render_world_map(gdpinfo, plot_countries, year, map_file): #将具体某年世界各国的GDP数据(包括缺少GDP数据以及只是在该年缺少GDP数据的国家)以地图形式可视化
    """
    Inputs:
      
      gdpinfo:gdp信息字典
      plot_countires:绘图库国家代码数据，字典格式，其中键为绘图库国家代码，值为对应的具体国名
      year:具体年份数据，以字符串格式程序，如"1970"
      map_file:输出的图片文件名
    
    目标：将指定某年的世界各国GDP数据在世界地图上显示，并将结果输出为具体的的图片文件
    提示：本函数可视化需要利用pygal.maps.world.World()方法
    """
    worldmap_chart=pygal.maps.world.World()                  #绘图
    worldmap_chart.title="全球GDP分布图"                     #图表标题
    for i in list(plot_countries[0]):               #利用for循环遍历，将值从字符串转化为浮点数
        plot_countries[0][i]=float(plot_countries[0][i])
    worldmap_chart.add(year,plot_countries[0])               #绘制图表，前为图例，后为值
    worldmap_chart.add("missing from w...",plot_countries[1])
    worldmap_chart.add("no date at thi...",plot_countries[2])
    worldmap_chart.render_to_file(map_file)                  #图表导出为map_file

    #编码，结束后将pass删除
    #不要忘记返回结果
def test_render_world_map(year):  #测试函数
    """
    对各功能函数进行测试
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    } #定义数据字典
    pygal_countries = pygal.maps.world.COUNTRIES   # 获得绘图库pygal国家代码字典
    gdp_countries = read_csv_as_nested_dict("isp_gdp.csv", gdpinfo["country_code"], gdpinfo["separator"],
                                            gdpinfo["quote"])          #利用函数将数据库内容存入变量
    reconcile_countries=reconcile_countries_by_name(pygal_countries,gdp_countries)
    #利用函数使得国家代码与国家名字的字典与无数据的列表的元组存入reconcile_countries
    build_countries=build_map_dict_by_name(gdpinfo,reconcile_countries[0],year,gdp_countries,reconcile_countries)
    #利用函数将数据库对应代码及gdp的值存入变量build_countries
    render_world_map(gdpinfo,build_countries, year, "isp_gdp_world_name_%s.svg"%year)
    # 测试时可以1970年为例，对函数继续测试，将运行结果与提供的svg进行对比，其它年份可将文件重新命名
#程序测试和运行
print("欢迎使用世行GDP数据可视化查询")
print("----------------------")
year=input("请输入需查询的具体年份:")
test_render_world_map(year)

