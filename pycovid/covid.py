#!/usr/bin/env python
# encoding='utf-8'
import json
import requests
from bs4 import BeautifulSoup


class CovidException(Exception):
    def __init__(self, *args):
        self.args = args


class PyCovid:
    """获取国内外的疫情数据"""

    def __init__(self):
        """从网站获取原始html代码，并分别对国内外的数据进行处理，只保留json格式的数据"""
        self.url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
        try:
            self.response = requests.get(self.url)
        except Exception:
            raise CovidException('网络连接失败，请检查网络连接。')
        self.response.encoding = 'utf8'
        self.c_soup = BeautifulSoup(self.response.text, "html.parser")
        self.c_soup = self.c_soup.find('script', id='getAreaStat')
        self.c_data = json.loads(str(self.c_soup)
                                 .strip('<script id="getAreaStat">try { window.getAreaStat = ')
                                 .strip('}catch(e){}</script>')
                                 )
        self.w_soup = BeautifulSoup(self.response.text, "html.parser")
        self.w_soup = self.w_soup.find('script', id='getListByCountryTypeService2true')
        self.w_data = json.loads(str(self.w_soup)
                                 .strip(
            '<script id="getListByCountryTypeService2true">try { window.getListByCountryTypeService2true = ')
                                 .strip('}catch(e){}</script>')
                                 )
        self.n_soup = BeautifulSoup(self.response.text, "html.parser")
        self.n_soup = self.n_soup.find('script', id='getTimelineService1')
        self.n_data = json.loads(str(self.n_soup)
                                 .strip('<script id="getTimelineService1">try { window.getTimelineService1 = ')
                                 .strip('}catch(e){}</script>')
                                 )

    def cn_covid(self, current=True, confirmed=True, cured=True, dead=True, province_name=None, return_to_json=False):
        """获取国内疫情数据
        :param current: 是否获取现存确诊人数，默认获取
        :param confirmed: 是否获取累计确诊人数，默认获取
        :param cured: 是否获取累计治愈人数，默认获取
        :param dead: 是否获取累计死亡人数，默认获取
        :param province_name: 是否获取指定省份的数据，默认获取全国数据，如果想获取北京的数据，参数为：'北京'或'北京市'
        :param return_to_json: 是否返回json格式的数据，默认返回字典格式数据
        :return: 字典，包含国内各个省份的疫情数据
        """
        if not current and not confirmed and not cured and not dead:
            raise CovidException('参数current、confirmed、cured、dead中至少需要获取一个数据')
        data = []
        for province in self.c_data:  # 获取每个省份的现存确诊、累计确诊、累计治愈、累计死亡人数
            p_data = {
                'provinceName': province['provinceShortName']
            }
            if current:
                p_data['currentConfirmed'] = province['currentConfirmedCount']
            if confirmed:
                p_data['confirmed'] = province['confirmedCount']
            if cured:
                p_data['cured'] = province['curedCount']
            if dead:
                p_data['dead'] = province['deadCount']
            data.append(p_data)
            if province_name in [province['provinceShortName'], province['provinceName']]:
                data = p_data
                break
        if return_to_json:
            return json.dumps(data, indent=4, ensure_ascii=False)
        return data

    def province_covid(self, province='北京', include_province_name=True, current=True, confirmed=True, cured=True,
                       dead=True, city_name=None, return_to_json=False):
        """获取某个省份的数据
        :param province: 想要获取的疫情数据，默认为北京
        :param include_province_name: 返回值是否包含省份名，默认不包含
        :param current: 是否获取现存确诊人数，默认获取
        :param confirmed: 是否获取累计确诊人数，默认获取
        :param cured: 是否获取累计治愈人数，默认获取
        :param dead: 是否获取累计死亡人数，默认获取
        :param city_name: 是否获取指定城市的数据，默认获取全国数据，如果想获取广州的数据，参数为：'广州'
        :param return_to_json: 是否返回json格式的数据，默认返回字典格式数据
        :return: 字典，包含该省份各个城市的疫情数据
        """
        if not current and not confirmed and not cured and not dead:
            raise CovidException('参数current、confirmed、cured、dead中至少需要获取一个数据')
        data = []
        if province is None:
            raise CovidException('参数province不能为空')
        # 这些地区不是城市，所以忽略。
        ignore_cities = ['待明确地区', '境外输入', '外地来沪', '境外来沪', '境外输入人员', '外地来津', '外地来京', '省十里丰监狱', '省级（湖北输入）']
        for province_data in self.c_data:
            # 假如用户想查询北京的数据，无论用户输入北京还是北京市，都可以获取到北京的数据
            if province == province_data['provinceShortName'] or province == province_data['provinceName']:
                if province_data['provinceShortName'] in ['香港', '澳门', '台湾']:
                    raise CovidException(f'如果想获取港澳台的数据，请使用cn_covid()并设置province_name参数。')
                for city in province_data['cities']:
                    if city['cityName'] in ignore_cities:
                        continue
                    city_data = {
                        'cityName': city['cityName']
                    }
                    if current:
                        city_data['currentConfirmed'] = city['currentConfirmedCount']
                    if confirmed:
                        city_data['confirmed'] = city['confirmedCount']
                    if cured:
                        city_data['cured'] = city['curedCount']
                    if dead:
                        city_data['dead'] = city['deadCount']
                    if city_name == city['cityName']:
                        return city_data
                    data.append(city_data)
                break
        if not data:
            raise CovidException(f'没有找到{province}的数据。')
        if include_province_name:
            data = {
                'provinceName': province,
                'cities': data
            }
        if return_to_json:
            return json.dumps(data, indent=4, ensure_ascii=False)
        return data

    def world_covid(self, current=True, confirmed=True, cured=True, dead=True, confirmed_incr=True, cured_incr=True,
                    dead_incr=True, country_name=None, return_to_json=False):
        """获取全球疫情数据
        :param current: 是否获取现存确诊人数，默认获取
        :param confirmed: 是否获取累计确诊人数，默认获取
        :param cured: 是否获取累计治愈人数，默认获取
        :param dead: 是否获取累计死亡人数，默认获取
        :param confirmed_incr: 是否获取新增确诊人数，默认获取
        :param cured_incr: 是否获取新增治愈人数，默认获取
        :param dead_incr: 是否获取新增死亡人数，默认获取
        :param country_name: 是否获取指定国家的数据，默认获取全国数据，如果想获取日本的数据，参数为：'日本'或'Japan'
        :param return_to_json: 是否返回json格式的数据，默认返回字典格式数据
        :return: 字典，包含全球各个国家的疫情数据
        """
        if not current and not confirmed and not cured and not dead and not confirmed_incr and not cured_incr and not dead_incr:
            raise CovidException('参数current、confirmed、cured、dead、confirmed_incr、cured_incr、dead_incr中至少需要获取一个数据')
        countries_name = {
            "Afghanistan": "阿富汗",
            "Angola": "安哥拉",
            "Albania": "阿尔巴尼亚",
            "Algeria": "阿尔及利亚",
            "Argentina": "阿根廷",
            "Armenia": "亚美尼亚",
            "Australia": "澳大利亚",
            "Austria": "奥地利",
            "Azerbaijan": "阿塞拜疆",
            "Bahamas": "巴哈马",
            "Bangladesh": "孟加拉国",
            "Belgium": "比利时",
            "Benin": "贝宁",
            "Burkina Faso": "布基纳法索",
            "Burundi": "布隆迪",
            "Bulgaria": "保加利亚",
            "Bosnia and Herz.": "波斯尼亚和黑塞哥维那",
            "Belarus": "白俄罗斯",
            "Belize": "伯利兹",
            "Bermuda": "百慕大群岛",
            "Bolivia": "玻利维亚",
            "Brazil": "巴西",
            "Brunei": "文莱",
            "Bhutan": "不丹",
            "Botswana": "博茨瓦纳",
            "Cambodia": "柬埔寨",
            "Cameroon": "喀麦隆",
            "Canada": "加拿大",
            "Central African Rep.": "中非共和国",
            "Chad": "乍得",
            "Chile": "智利",
            "China": "中国",
            "Colombia": "哥伦比亚",
            "Congo": "刚果",
            "Costa Rica": "哥斯达黎加",
            "Côte d'Ivoire": "科特迪瓦",
            "Croatia": "克罗地亚",
            "Cuba": "古巴",
            "Cyprus": "塞浦路斯",
            "Czech Rep.": "捷克共和国",
            "Dem. Rep. Korea": "韩国",
            "Dem. Rep. Congo": "民主刚果",
            "Denmark": "丹麦",
            "Djibouti": "吉布提",
            "Dominican Rep.": "多米尼加共和国",
            "Ecuador": "厄瓜多尔",
            "Egypt": "埃及",
            "El Salvador": "萨尔瓦多",
            "Eq. Guinea": "赤道几内亚",
            "Eritrea": "厄立特里亚",
            "Estonia": "爱沙尼亚",
            "Ethiopia": "埃塞俄比亚",
            "Falkland Is.": "福克兰群岛",
            "Fiji": "斐济",
            "Finland": "芬兰",
            "France": "法国",
            "French Guiana": "法属圭亚那",
            "Fr. S. Antarctic Lands": "法属南部领地",
            "Gabon": "加蓬",
            "Gambia": "冈比亚",
            "Germany": "德国",
            "Georgia": "佐治亚州",
            "Ghana": "加纳",
            "Greece": "希腊",
            "Greenland": "格陵兰",
            "Guatemala": "危地马拉",
            "Guinea": "几内亚",
            "Guinea-Bissau": "几内亚比绍",
            "Guyana": "圭亚那",
            "Haiti": "海地",
            "Heard I. and McDonald Is.": "赫德岛和麦克唐纳群岛",
            "Honduras": "洪都拉斯",
            "Hungary": "匈牙利",
            "Iceland": "冰岛",
            "India": "印度",
            "Indonesia": "印度尼西亚",
            "Iran": "伊朗",
            "Iraq": "伊拉克",
            "Ireland": "爱尔兰",
            "Israel": "以色列",
            "Italy": "意大利",
            "Ivory Coast": "象牙海岸",
            "Jamaica": "牙买加",
            "Japan": "日本",
            "Jordan": "乔丹",
            "Kashmir": "克什米尔",
            "Kazakhstan": "哈萨克斯坦",
            "Kenya": "肯尼亚",
            "Kosovo": "科索沃",
            "Kuwait": "科威特",
            "Kyrgyzstan": "吉尔吉斯斯坦",
            "Laos": "老挝",
            "Lao PDR": "老挝人民民主共和国",
            "Latvia": "拉脱维亚",
            "Lebanon": "黎巴嫩",
            "Lesotho": "莱索托",
            "Liberia": "利比里亚",
            "Libya": "利比亚",
            "Lithuania": "立陶宛",
            "Luxembourg": "卢森堡",
            "Madagascar": "马达加斯加",
            "Macedonia": "马其顿",
            "Malawi": "马拉维",
            "Malaysia": "马来西亚",
            "Mali": "马里",
            "Mauritania": "毛里塔尼亚",
            "Mexico": "墨西哥",
            "Moldova": "摩尔多瓦",
            "Mongolia": "蒙古",
            "Montenegro": "黑山",
            "Morocco": "摩洛哥",
            "Mozambique": "莫桑比克",
            "Myanmar": "缅甸",
            "Namibia": "纳米比亚",
            "Netherlands": "荷兰",
            "New Caledonia": "新喀里多尼亚",
            "New Zealand": "新西兰",
            "Nepal": "尼泊尔",
            "Nicaragua": "尼加拉瓜",
            "Niger": "尼日尔",
            "Nigeria": "尼日利亚",
            "Korea": "朝鲜",
            "Northern Cyprus": "北塞浦路斯",
            "Norway": "挪威",
            "Oman": "阿曼",
            "Pakistan": "巴基斯坦",
            "Panama": "巴拿马",
            "Papua New Guinea": "巴布亚新几内亚",
            "Paraguay": "巴拉圭",
            "Peru": "秘鲁",
            "Republic of the Congo": "刚果共和国",
            "Philippines": "菲律宾",
            "Poland": "波兰",
            "Portugal": "葡萄牙",
            "Puerto Rico": "波多黎各",
            "Qatar": "卡塔尔",
            "Republic of Seychelles": "塞舌尔共和国",
            "Republic of Singapore": "新加坡共和国",
            "Romania": "罗马尼亚",
            "Russia": "俄罗斯",
            "Rwanda": "卢旺达",
            "Samoa": "萨摩亚",
            "Saudi Arabia": "沙特阿拉伯",
            "Senegal": "塞内加尔",
            "Serbia": "塞尔维亚",
            "Sierra Leone": "塞拉利昂",
            "Slovakia": "斯洛伐克",
            "Slovenia": "斯洛文尼亚",
            "Solomon Is.": "所罗门群岛",
            "Somaliland": "索马里兰",
            "Somalia": "索马里",
            "South Africa": "南非",
            "S. Geo. and S. Sandw. Is.": "南乔治亚和南桑德威奇群岛",
            "S. Sudan": "南苏丹",
            "Spain": "西班牙",
            "Sri Lanka": "斯里兰卡",
            "Sudan": "苏丹",
            "Suriname": "苏里南",
            "Swaziland": "斯威士兰",
            "Sweden": "瑞典",
            "Switzerland": "瑞士",
            "Syria": "叙利亚",
            "Tajikistan": "塔吉克斯坦",
            "Tanzania": "坦桑尼亚",
            "Thailand": "泰国",
            "The Kingdom of Tonga": "汤加王国",
            "Timor-Leste": "东帝汶",
            "Togo": "多哥",
            "Trinidad and Tobago": "特立尼达和多巴哥",
            "Tunisia": "突尼斯",
            "Turkey": "土耳其",
            "Turkmenistan": "土库曼斯坦",
            "Uganda": "乌干达",
            "Ukraine": "乌克兰",
            "United Arab Emirates": "阿拉伯联合酋长国",
            "United Republic of Tanzania": "坦桑尼亚联合共和国",
            "United States": "美国",
            "United Kingdom": "英国",
            "United States of America": "美利坚合众国",
            "Uruguay": "乌拉圭",
            "Uzbekistan": "乌兹别克斯坦",
            "Vanuatu": "瓦努阿图",
            "Venezuela": "委内瑞拉",
            "Vietnam": "越南",
            "West Bank": "西岸",
            "W. Sahara": "西撒哈拉",
            "Yemen": "也门",
            "Zambia": "赞比亚",
            "Zimbabwe": "津巴布韦",
            "Liechtenstein": "列支敦士登",
            "Aland": "奥兰群岛",
            "Andorra": "安道尔",
            "American Samoa": "东萨摩亚",
            "Antigua and Barb.": "安提瓜和巴布达",
            "Bahrain": "巴林王国",
            "Barbados": "巴巴多斯",
            "Comoros": "科摩罗",
            "Cape Verde": "佛得角",
            "Curaçao": "库拉索",
            "Cayman Is.": "开曼群岛",
            "N. Cyprus": "塞浦路斯",
            "Dominica": "多米尼克",
            "Faeroe Is.": "法罗群岛",
            "Micronesia": "密克罗尼西亚联邦",
            "Grenada": "格林纳达",
            "Guam": "关岛",
            "Isle of Man": "马恩岛",
            "Br. Indian Ocean Ter.": "英属印度洋领地",
            "Jersey": "泽西岛",
            "Siachen Glacier": "锡亚琴冰川",
            "Kiribati": "基里巴斯",
            "Saint Lucia": "圣卢西亚",
            "Malta": "马耳他岛",
            "N. Mariana Is.": "马里亚纳群岛",
            "Montserrat": "蒙特塞拉特",
            "Mauritius": "毛里求斯",
            "Niue": "纽埃",
            "Palau": "帕劳",
            "Palestine": "巴勒斯坦",
            "Fr. Polynesia": "法属波利尼西亚",
            "Singapore": "新加坡"
        }
        data = []
        for country in self.w_data:  # 获取每个国家的现存确诊、累计确诊、累计治愈、累计死亡、新增确诊、新增死亡、新增治愈人数
            country_name_en_us = ''  # 国家名称英文
            country_name_zh_cn = country['provinceName']  # 国家名称中文
            if country_name_zh_cn in ['钻石公主号邮轮']:
                continue
            for en_us, zh_cn in countries_name.items():
                if zh_cn == country_name_zh_cn:
                    country_name_en_us = en_us
                    break
            world_data = {
                'countryNameEn': country_name_en_us,
                'countryNameCn': country_name_zh_cn
            }
            if current:
                world_data['currentConfirmed'] = country['currentConfirmedCount']
            if confirmed:
                world_data['confirmed'] = country['confirmedCount']
            if cured:
                world_data['cured'] = country['curedCount']
            if dead:
                world_data['dead'] = country['deadCount']
            if confirmed_incr:
                world_data['confirmedIncr'] = country['incrVo']['confirmedIncr']
            if cured_incr:
                world_data['curedIncr'] = country['incrVo']['curedIncr']
            if dead_incr:
                world_data['deadIncr'] = country['incrVo']['deadIncr']
            if country_name in [country_name_zh_cn, country_name_en_us]:
                data = world_data
                break
            data.append(world_data)
        if return_to_json:
            return json.dumps(data, indent=4, ensure_ascii=False)
        return data

    def danger_areas(self, include_cities=True, include_counts=True, include_danger_areas=True, return_to_json=False):
        """获取国内的中高风险地区
        :param include_cities: 是否包含各个城市的风险地区数量，默认为True
        :param include_counts: 是否包含各个省份的风险地区数量，默认为True
        :param include_danger_areas: 是否包含中高风险地区数量，默认为True
        :param return_to_json: 是否返回json格式，默认返回字典格式
        """
        if not include_cities and not include_counts and not include_danger_areas:
            raise CovidException('参数include_cities, include_counts, include_danger_areas至少要有一个为True')
        data = []
        merged_data = {
            'midDangerAreas': [],
            'highDangerAreas': [],
        }
        for province in self.c_data:
            '''如果某个省份没有中高风险地区，则忽略该省份的数据'''
            if province['highDangerCount'] > 0 or province['midDangerCount'] > 0:
                p_data = {
                    'provinceName': province['provinceShortName']
                }
                if include_danger_areas:
                    p_data['midDangerAreas'] = []
                    p_data['highDangerAreas'] = []
                if include_cities:
                    p_data['cities'] = []
                    for city in province['cities']:
                        """如果某个城市没有中高风险地区，则忽略该城市的数据"""
                        if city['highDangerCount'] > 0 or city['midDangerCount'] > 0:
                            cn_data = {
                                'cityName': city['cityName'],
                                'highDanger': city['highDangerCount'],
                                'midDanger': city['midDangerCount']
                            }
                            # print(cn_data)
                            p_data['cities'].append(cn_data)
                if include_counts:
                    p_data['highDanger'] = province['highDangerCount']
                    p_data['midDanger'] = province['midDangerCount']
                if include_danger_areas:
                    for area in province['dangerAreas']:
                        # 去除风险地区的省份名称
                        danger_lv = 'dangerAreas'
                        if area['dangerLevel'] == 1:
                            danger_lv = 'highDangerAreas'
                        elif area['dangerLevel'] == 2:
                            danger_lv = 'midDangerAreas'
                        area_name = area['areaName']
                        if province['provinceName'] in area_name:
                            area_name.strip(province['provinceName'])
                        if province['provinceShortName'] in area_name:
                            area_name.strip(province['provinceShortName'])
                        if area['cityName'] not in area_name:
                            area_name = area['cityName'] + area_name
                        p_data[danger_lv].append(area_name)
                        merged_data[danger_lv].append(province['provinceName'] + area_name)
                data.append(p_data)
        if not data:    # 如果国内没有中高风险地区，则返回空列表
            return None
        if not include_cities and not include_counts:
            data = merged_data
        if return_to_json:
            return json.dumps(data, indent=4, ensure_ascii=False)
        return data

    def news_timeline(self, include_summary=True, include_url=True, include_source=True, include_time=True,
                      return_to_json=False):
        """获取新闻时间轴
        :param include_summary: 是否包含新闻摘要，默认为True
        :param include_url: 是否包含新闻链接，默认为True
        :param include_source: 是否包含新闻来源，默认为True
        :param include_time: 是否包含新闻发布时间，默认为True
        :param return_to_json: 是否返回json格式，默认返回字典格式
        :return: 返回近期的新闻信息
        """
        data = []
        for news in self.n_data:
            news_data = {'title': news['title']}
            if include_time:
                news_data['publishedTime'] = news['pubDateStr']
            if include_source:
                news_data['source'] = news['infoSource']
            if include_url:
                news_data['url'] = news['sourceUrl']
            if include_summary:
                news_data['summary'] = news['summary']
            data.append(news_data)
        if not data:
            print('最近没有相关新闻信息')
            return None
        if return_to_json:
            return json.dumps(data, indent=4, ensure_ascii=False)
        return data

    def print_license(self, language='zh_CN'):
        """打印授权信息
        :param language: 版权信息的语言，支持简体中文和英文
        """
        if language == 'zh_CN':
            print('版权所有：@2020-2022 森哥Studio')
            print('许可证：GNU GPLv3')
            print('作者：森哥Studio')
            print('邮箱：senge-studio@protonmail.com')
            print('Github：https://github.com/senge-studio')
            print('数据来源：https://ncov.dxy.cn/ncovh5/view/pneumonia')
            print('您可以免费使用本程序，也可以免费对其进行优化和改进以及再发布，但是必须保留原作者的信息，详情请访问：https://jxself.org/translations/gpl-3.zh.shtml')
            print('无论出于任何目的，本程序都禁止用于商业用途，否则将受到法律责任。')
            print('版本：1.2.0')
            print('更新日期：2022-07-05')
            print('更新日志：')
            print('\t1.2.0：')
            print('\t\t支持直接将输出的结果保存为json格式')
            print('\t\t修改了文档中的错误提示')
        elif language == 'en_US':
            print('Copyright © 2020-2022 senge-studio')
            print('License: GNU General Public License v3')
            print('Author: senge-studio')
            print('Email: senge-studio@protonmail.com')
            print('Github: https://github.com/senge-studio')
            print('Data: https://ncov.dxy.cn/ncovh5/view/pneumonia')
            print(
                'You can freely use this program, but you can also freely improve it and release it again, '
                'but you must keep the author information. For more information, please visit: '
                'https://www.gnu.org/licenses/gpl-3.0.en.html')
            print('This program is forbidden for commercial use.')
            print('Version: 1.2.0')
            print('Update date: 2022-07-05')
            print('Update log:')
            print('\t1.2.0:')
            print('\t\t1. You can directly save the output result to json format')
            print('\t\t2. Fixed the error of the document.')


if __name__ == '__main__':
    # 在导入pycovid.py时检查网络连接
    try:
        status = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia', timeout=2).status_code
    except Exception:
        raise ImportError('网络连接失败，如果想导入这个包，请检查网络连接')
    else:
        if status != 200:
            raise ImportError(f'网络连接失败，错误码：{status}如果想导入这个包，请先检查网络连接')
    print('网络连接成功')
