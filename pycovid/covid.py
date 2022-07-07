#!/usr/bin/env python
# encoding='utf-8'
import json                         # 数据预处理
import requests                     # 网络请求
from bs4 import BeautifulSoup       # HTML解析
import locale                       # 获取系统语言


class CovidException(Exception):
    def __init__(self, *args):
        self.args = args

class PyCovid:
    """获取国内外的疫情数据"""

    def __init__(self, ignore_region=False):
        """从网站获取原始html代码，并分别对国内外的数据进行处理，只保留json格式的数据
        :param ignore_region: 是否忽略系统语言检测，默认不忽略，如果你的系统语言不是中文，而且你想获取国内的数据，可以设置为True以忽略异常
        如需调用原始数据，请自行添加参数获取
        如果您想获取国内疫情信息的原始数据，请使用PyCovid().c_data
        如果您想获取国外疫情信息的原始数据，请使用PyCovid().w_data
        如果您想获取国内疫情相关的新闻信息，请使用PyCovid().n_data
        """
        self.ignore_region = ignore_region
        # 如果系统语言不是中文，则抛出异常并提示用户使用其他方法进行调用(如果ignore_region为True，则不抛出异常)
        if locale.getdefaultlocale()[0] != 'zh_CN' and not self.ignore_region:
            raise CovidException("""Your system language is not Chinese, please run: "from pycovid.covid_en import PyCovid" instead.
If you want to ignore system language, please run: "from pycovid.covid import PyCovid(ignore_region=True)
""")
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
                    cityname = city['cityName']
                    if city['cityName'] in ignore_cities:
                        continue
                    if city['cityName'] == '大兴安岭':
                        cityname = '大兴安岭地区'
                    city_names = [
                        "锡林郭勒盟",
                        "阿拉善盟",
                        "兴安盟",
                        "甘孜州",
                        "凉山州",
                        "阿坝州",
                        "德宏州",
                        "红河州",
                        "大理州",
                        "文山州",
                        "楚雄州",
                        "赣江新区",
                        "恩施州",
                        "神农架林区",
                        "雄安新区",
                        "喀什地区",
                        "伊犁州",
                        "兵团第四师",
                        "昌吉州",
                        "兵团第九师",
                        "巴州（巴音郭楞蒙古自治州）", 
                        "兵团第十二师",
                        "兵团第七师",
                        "阿克苏地区",
                        "黔南州",
                        "黔东南州",
                        "黔西南州",
                        "海北州",
                    ]
                    if cityname not in city_names:
                        cityname = cityname + '市'
                    city_data = {
                        'cityName': cityname
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
                    dead_incr=True, name=None, return_to_json=False):
        """获取全球疫情数据
        :param current: 是否获取现存确诊人数，默认获取
        :param confirmed: 是否获取累计确诊人数，默认获取
        :param cured: 是否获取累计治愈人数，默认获取
        :param dead: 是否获取累计死亡人数，默认获取
        :param confirmed_incr: 是否获取新增确诊人数，默认获取
        :param cured_incr: 是否获取新增治愈人数，默认获取
        :param dead_incr: 是否获取新增死亡人数，默认获取
        :param name: 是否获取指定国家的数据，默认获取全国数据，如果想获取日本的数据，参数为：'日本'或'Japan'
        :param return_to_json: 是否返回json格式的数据，默认返回字典格式数据
        :return: 字典，包含全球各个国家的疫情数据
        """
        if not current and not confirmed and not cured and not dead and not confirmed_incr and not cured_incr and not dead_incr:
            raise CovidException('参数current、confirmed、cured、dead、confirmed_incr、cured_incr、dead_incr中至少需要获取一个数据')
        countries_name = {
            "法国": "France",
            "德国": "Germany",
            "韩国": "Korea",
            "英国": "United Kingdom",
            "西班牙": "Spain",
            "意大利": "Italy",
            "巴西": "Brazil",
            "土耳其": "Turkey",
            "荷兰": "Netherlands",
            "俄罗斯": "Russia",
            "日本": "Japan",
            "比利时": "Belgium",
            "中国": "China",
            "奥地利": "Austria",
            "瑞士": "Switzerland",
            "希腊": "Greece",
            "伊朗": "Iran",
            "丹麦": "Denmark",
            "墨西哥": "Mexico",
            "瑞典": "Sweden",
            "斯洛伐克": "Slovakia",
            "智利": "Chile",
            "塞尔维亚": "Serbia",
            "伊拉克": "Iraq",
            "美国": "United States",
            "爱尔兰": "Ireland",
            "乌克兰": "Ukraine",
            "哈萨克斯坦": "Kazakhstan",
            "秘鲁": "Peru",
            "格鲁吉亚": "Georgia",
            "斯洛文尼亚": "Slovenia",
            "罗马尼亚": "Romanian",
            "约旦": "Jordan",
            "黎巴嫩": "Lebanon",
            "葡萄牙": "Portugal",
            "波多黎各": "Puerto Rico",
            "危地马拉": "Guatemala",
            "立陶宛": "Lithuania",
            "蒙古": "Mongolia",
            "阿塞拜疆": "Azerbaijan",
            "澳大利亚": "Australia",
            "克罗地亚": "Croatia",
            "多米尼加": "dominica",
            "玻利维亚": "Bolivia",
            "巴拿马": "Panama",
            "孟加拉国": "Bangladesh",
            "捷克": "Czech Republic",
            "塞浦路斯": "Cyprus",
            "留尼旺": "Reunion",
            "印度": "India",
            "加拿大": "Canada",
            "保加利亚": "Bulgaria",
            "摩洛哥": "Morocco",
            "拉脱维亚": "Latvia",
            "巴勒斯坦": "Palestine",
            "乌拉圭": "Uruguay",
            "巴基斯坦": "Pakistan",
            "沙特阿拉伯": "Saudi Arabia",
            "以色列": "Israel",
            "利比亚": "Libya",
            "毛里求斯": "Mauritius",
            "亚美尼亚": "Armenia",
            "阿联酋": "U.A.E",
            "马提尼克": "Martinique",
            "巴拉圭": "Paraguay",
            "埃及": "Egypt",
            "爱沙尼亚": "Estonia",
            "新西兰": "New Zealand",
            "瓜德罗普岛": "Guadeloupe",
            "委内瑞拉": "Venezuela",
            "马来西亚": "Malaysia",
            "博茨瓦纳": "Botswana",
            "摩尔多瓦": "Moldova",
            "卡塔尔": "Qatar",
            "阿根廷": "Argentina",
            "巴林": "Bahrain",
            "埃塞俄比亚": "Ethiopia",
            "阿尔及利亚": "Algeria",
            "文莱": "Brunei",
            "特立尼达和多巴哥": "Trinidad and Tobago",
            "阿曼": "Oman",
            "缅甸": "Myanmar",
            "法属圭亚那": "French Guiana",
            "牙买加": "Jamaica",
            "黑山": "Montenegro",
            "哥斯达黎加": "Costa Rica",
            "古巴": "Cuba",
            "白俄罗斯": "Belarus",
            "莫桑比克": "Mozambique",
            "阿尔巴尼亚": "Albania",
            "巴巴多斯": "Barbados",
            "芬兰": "Finland",
            "肯尼亚": "Kenya",
            "斯威士兰": "Eswatini",
            "斯里兰卡": "Sri Lanka",
            "贝宁": "Benin",
            "刚果（金）": "Democratic Republic of the Congo",
            "不丹": "Bhutan",
            "阿富汗": "Afghanistan",
            "苏里南": "Suriname",
            "新喀里多尼亚": "New Caledonia",
            "哥伦比亚": "Colombia",
            "伯利兹": "Belize",
            "尼日利亚": "Nigeria",
            "圭亚那": "Guyana",
            "泽西岛": "Jersey",
            "乌兹别克斯坦": "Uzbekistan",
            "布隆迪共和国": "Burundi",
            "加纳": "Ghana",
            "纳米比亚": "Namibia",
            "厄瓜多尔": "Ecuador",
            "库拉索岛": "Curacao",
            "卢旺达": "Rwanda",
            "马约特": "Mayotte",
            "喀麦隆": "Cameroon",
            "安哥拉": "Angola",
            "坦桑尼亚": "Tanzania",
            "萨尔瓦多": "El Salvador",
            "关岛": "Guam",
            "马尔代夫": "Maldives",
            "阿鲁巴": "Aruba",
            "叙利亚": "Syria",
            "开曼群岛": "Cayman Islands",
            "根西岛": "Guernsey",
            "巴哈马": "Bahamas",
            "莱索托": "Lesotho",
            "科特迪瓦": "Côte d’Ivoire",
            "苏丹": "Sudan",
            "马拉维": "Malawi",
            "越南": "Vietnam",
            "毛里塔尼亚": "Mauritania",
            "吉尔吉斯斯坦": "Kyrgyzstan",
            "佛得角": "Cape Verde",
            "塞舌尔": "Seychelles",
            "马恩岛": "Isle of Man",
            "马达加斯加": "Madagascar",
            "泰国": "Thailand",
            "海地": "Haiti",
            "加蓬": "Gabon",
            "挪威": "Norway",
            "卢森堡": "Luxembourg",
            "索马里": "Somalia",
            "马里": "Mali",
            "刚果（布）": "Congo (Brazzaville)",
            "新加坡": "Singapore",
            "印度尼西亚": "Indonesia",
            "多米尼克": "Dominica",
            "赞比亚共和国": "Zambia",
            "百慕大": "Bermuda",
            "美属维尔京群岛": "United States Virgin Islands",
            "多哥": "Togo",
            "斐济": "Fiji",
            "尼加拉瓜": "Nicaragua",
            "塞内加尔": "Senegal",
            "格林那达": "Grenada",
            "北马里亚纳群岛联邦": "Commonwealth of the Northern Mariana Islands",
            "突尼斯": "Tunisia",
            "摩纳哥": "Monaco",
            "匈牙利": "Hungary",
            "圣马丁岛": "Saint Martin",
            "也门共和国": "Yemen",
            "格陵兰": "Greenland",
            "圣文森特和格林纳丁斯": "Saint Vincent and the Grenadines",
            "冰岛": "Iceland",
            "波兰": "Poland",
            "中非共和国": "Central African Republic",
            "几内亚": "Guinea",
            "马耳他": "Malta",
            "安提瓜和巴布达": "Antigua and Barbuda",
            "布基纳法索": "Burkina Faso",
            "荷属圣马丁": "St. Maarten, The Netherlands",
            "南苏丹": "South Sudan",
            "科威特": "Kuwait",
            "圣其茨和尼维斯": "Saint-Žić and Nevis",
            "安道尔": "Andorra",
            "列支敦士登": "Liechtenstein",
            "科摩罗": "Comoros",
            "圣巴泰勒米岛": "Saint Barthelemy Island",
            "赤道几内亚": "Equatorial Guinea",
            "东帝汶": "Timor-Leste",
            "圣马力诺": "San Marino",
            "英属维尔京群岛": "British Virgin Islands",
            "巴布亚新几内亚": "Papua New Guinea",
            "乌干达": "Uganda",
            "特克斯和凯科斯群岛": "Turks and Caicos Islands",
            "圣卢西亚": "Saint Lucia",
            "安圭拉": "Anguilla",
            "吉布提": "Djibouti",
            "圣多美和普林西比": "Sao Tome and Principe",
            "法罗群岛": "Faroe Islands",
            "塞拉利昂": "Sierra Leone",
            "洪都拉斯": "Honduras",
            "厄立特里亚": "Eritrea",
            "直布罗陀": "Gibraltar",
            "几内亚比绍": "Guinea-Bissau",
            "尼日尔": "Niger",
            "津巴布韦": "Zimbabwe",
            "圣皮埃尔和密克隆群岛": "Saint Pierre and Miquelon",
            "波黑": "Bosnia",
            "乍得": "Chad",
            "冈比亚": "Gambia",
            "福克兰群岛": "Falkland Islands",
            "利比里亚": "Liberia",
            "北马其顿": "North Macedonia",
            "蒙特塞拉特": "Montserrat",
            "尼泊尔": "Nepal",
            "老挝": "Laos",
            "法属波利尼西亚": "French Polynesia",
            "塔吉克斯坦": "Tajikistan",
            "荷兰加勒比地区": "Netherlands Caribbean",
            "柬埔寨": "Cambodia",
            "梵蒂冈": "Vatican City",
            "菲律宾": "Philippines",
            "南非": "South Africa"
        }
        data = []
        for country in self.w_data:  # 获取每个国家的现存确诊、累计确诊、累计治愈、累计死亡、新增确诊、新增死亡、新增治愈人数
            country_name_en_us = ''  # 国家名称英文
            country_name_zh_cn = country['provinceName']  # 国家名称中文
            if country_name_zh_cn in ['钻石公主号邮轮']:
                continue
            for zh_cn, en_us in countries_name.items():
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
            if name in [country_name_zh_cn, country_name_en_us]:
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
                        cityname = area['cityName']
                        if city['cityName'] == '大兴安岭':
                            cityname = '大兴安岭地区'
                        city_names = [
                            "锡林郭勒盟",
                            "阿拉善盟",
                            "兴安盟",
                            "甘孜州",
                            "凉山州",
                            "阿坝州",
                            "德宏州",
                            "红河州",
                            "大理州",
                            "文山州",
                            "楚雄州",
                            "赣江新区",
                            "恩施州",
                            "神农架林区",
                            "雄安新区",
                            "喀什地区",
                            "伊犁州",
                            "兵团第四师",
                            "昌吉州",
                            "兵团第九师",
                            "巴州（巴音郭楞蒙古自治州）", 
                            "兵团第十二师",
                            "兵团第七师",
                            "阿克苏地区",
                            "黔南州",
                            "黔东南州",
                            "黔西南州",
                            "海北州",
                        ]
                        if cityname not in city_names:
                            cityname = cityname + '市'
                        if area['cityName'] in area_name:
                            area_name = area_name.strip(area['cityName'])
                        area_name = cityname + area_name
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

    def print_license(self):
        """打印授权信息"""
        print('版权所有：@2020-2022 森哥Studio')
        print('许可证：GNU GPLv3')
        print('作者：森哥Studio')
        print('邮箱：senge-studio@protonmail.com')
        print('Github：https://github.com/senge-studio')
        print('数据来源：https://ncov.dxy.cn/ncovh5/view/pneumonia')
        print('您可以免费使用本程序，也可以免费对其进行优化和改进以及再发布，但是必须保留原作者的信息，详情请访问：https://jxself.org/translations/gpl-3.zh.shtml')
        print('无论出于任何目的，本程序都禁止用于商业用途，否则将受到法律责任。')
        print('版本：2.0.3')
        print('更新日期：2022-07-07')
        print('更新日志：')
        print('\t\t修复了部分Bug。')

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
