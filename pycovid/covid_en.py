#!/usr/bin/env python
# encoding='utf-8'
import json                         # Data format: JSON
import requests                     # The network requests
from bs4 import BeautifulSoup       # HTML parser

class CovidException(Exception):
    def __init__(self, *args):
        self.args = args

class PyCovid:
    """Get the latest covid-19 data from the website"""

    def __init__(self):
        """Get the html data from the website, and parse the data, only save the json data which we need
        if you want to get the raw data, you can get it by using some parameters in the function
        if you want to get the covid-19 data from China, you can use the function PyCovid().c_data
        if you want to get the covid-19 data from the world, you can use the function PyCovid().w_data
        """
        self.url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
        try:
            self.response = requests.get(self.url)
        except Exception:
            raise CovidException('You\'re offline, please check your network and try again.')
        self.response.encoding = 'utf8'
        self.w_soup = BeautifulSoup(self.response.text, "html.parser")
        self.w_soup = self.w_soup.find('script', id='getListByCountryTypeService2true')
        self.w_data = json.loads(str(self.w_soup)
                                 .strip(
            '<script id="getListByCountryTypeService2true">try { window.getListByCountryTypeService2true = ')
                                 .strip('}catch(e){}</script>')
                                 )
    
    def world_covid(self, current=True, confirmed=True, cured=True, dead=True, confirmed_incr=True, cured_incr=True,
                    dead_incr=True, name=None, return_to_json=False):
        """Get the covid-19 data from the world
        :param current: Current confirmed count will be get default, if you don't want it, please set the paramenter to False
        :param confirmed: Confirmed count will be get default, if you don't want it, please set the paramenter to False.
        :param cured: Cured count will be get default, if you don't want it, please set the paramenter to False
        :param dead: Dead count will be get default, if you don't want it, please set the paramenter to False
        :param confirmed_incr: Confirmed increasement will be get default, if you don't want it, please set the paramenter to False
        :param cured_incr: Cured increasement will be get default, if you don't want it, please set the paramenter to False
        :param dead_incr: Dead increasement will be get default, if you don't want it, please set the paramenter to False
        :param name: Whether to obtain data for the specified country, the default is to obtain the national data, if you want to obtain data for Japan, the parameter is: 'Japan'
        :param return_to_json: If you want to get the data in json format, please set the paramenter to True, the default is False
        :return: Dict, if you set the return_to_json to True, the return will be a json string
        """
        if not current and not confirmed and not cured and not dead and not confirmed_incr and not cured_incr and not dead_incr:
            raise CovidException('At least one of the parameters current, confirmed, cured, dead, confirmed_incr, cured_incr, dead_incr needs to be True')
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
        for country in self.w_data: # Get current confirmed, confirmed, cured, dead, confirmed increasement, dead increasement, cured increasement from the data.
            country_name_en_us = ''  # English name of country
            country_name_zh_cn = country['provinceName']  # Chinese name of the country
            if country_name_zh_cn in ['钻石公主号邮轮']:
                continue
            for zh_cn, en_us in countries_name.items():
                if zh_cn == country_name_zh_cn:
                    country_name_en_us = en_us
                    break
            world_data = {
                'countryName': country_name_en_us,
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
            if name in [country_name_en_us]:
                data = world_data
                break
            data.append(world_data)
        if return_to_json:
            return json.dumps(data, indent=4, ensure_ascii=False)
        return data

    def print_license(self):
        """Print license"""
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
        print('Version: 2.0.2')
        print('Update date: 2022-07-07')
        print('Update log:')
        print('\t\tBug fixed.')

if __name__ == '__main__':
    # Whill importing this package, the internet connection would be checked.
    try:
        status = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia', timeout=2).status_code
    except Exception:
        raise ImportError('Network connection failed, please check your network and try again.')
    else:
        if status != 200:
            raise ImportError(f'Network connection failed, error code:{status}. If you want to import this package, please check your network and try again.')
    print('Network connection successful.')
