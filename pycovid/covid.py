#!/usr/bin/env python
# encoding='utf-8'
import json
import requests
from requests.exceptions import RequestException, ConnectionError
from bs4 import BeautifulSoup
import pathlib


class PyCovid:
    """获取国内外的疫情数据"""

    def __init__(self):
        """从网站获取原始html代码，并分别对国内外的数据进行处理，只保留json格式的数据"""
        self.url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
        self.response = requests.get(self.url)
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

    def cn_covid(self):
        """获取国内疫情数据
        :return: 字典，包含国内各个省份的疫情数据
        """
        data = []
        for province in self.c_data:  # 获取每个省份的现存确诊、累计确诊、累计治愈、累计死亡人数
            p_data = {
                'provinceName': province['provinceShortName'],
                'currentConfirmed': province['currentConfirmedCount'],
                'confirmed': province['confirmedCount'],
                'cured': province['curedCount'],
                'dead': province['deadCount']
            }
            data.append(p_data)
        return data

    def province_covid(self, province='北京', include_province_name=True):
        """获取某个省份的数据
        :param province: 想要获取的疫情数据，默认为北京
        :param include_province_name: 返回值是否包含省份名，默认不包含
        :return: 字典，包含该省份各个城市的疫情数据
        """
        data = []
        ignore_cities = ['待明确地区', '境外输入', '外地来沪', '境外来沪', '境外输入人员', '外地来津', '外地来京', '省十里丰监狱', '省级（湖北输入）']  # 这些地区不是城市，所以忽略。
        for province_data in self.c_data:
            # 假如用户想查询北京的数据，无论用户输入北京还是北京市，都可以获取到北京的数据
            if province == province_data['provinceShortName'] or province == province_data['provinceName']:
                if province_data['provinceShortName'] in ['香港', '澳门', '台湾']:
                    raise ValueError(f'暂时不支持查询港澳台的详细数据。')
                for city in province_data['cities']:
                    if city['cityName'] in ignore_cities:
                        continue
                    cn_data = {
                        'cityName': city['cityName'],
                        'currentConfirmed': city['currentConfirmedCount'],
                        'confirmed': city['confirmedCount'],
                        'cured': city['curedCount'],
                        'dead': city['deadCount']
                    }
                    data.append(cn_data)
                break
        return {'provinceName': province, 'data': data} if include_province_name else data

    def world_covid(self):
        """获取全球疫情数据
        :return: 字典，包含全球各个国家的疫情数据
        """
        # 获取当前python文件的绝对路径
        path = pathlib.Path(__file__).absolute()
        # countries.json相对当前python文件的相对路径是../data/countries.json，获取其绝对路径
        path = path.parent.parent / 'data' / 'countries.json'
        # 读取json文件，路径为path
        with open(path, 'r', encoding='utf-8') as f:
            countries_name = json.load(f)
        data = []
        for country in self.w_data:  # 获取每个国家的现存确诊、累计确诊、累计治愈、累计死亡、新增确诊、新增死亡、新增治愈人数
            country_name_en_us = ''                         # 国家名称英文
            country_name_zh_cn = country['provinceName']    # 国家名称中文
            for en_us, zh_cn in countries_name.items():
                if zh_cn == country_name_zh_cn:
                    country_name_en_us = en_us
                    break
            world_data = {
                'countryNameEn': country_name_en_us,
                'countryNameCn': country_name_zh_cn,
                'currentConfirmed': country['currentConfirmedCount'],
                'confirmed': country['confirmedCount'],
                'cured': country['curedCount'],
                'dead': country['deadCount'],
                'confirmedIncr': country['incrVo']['confirmedIncr'],
                'curedIncr': country['incrVo']['curedIncr'],
                'deadIncr': country['incrVo']['deadIncr']
            }
            data.append(world_data)
        return data

    def danger_areas(self):
        """获取国内的中高风险地区"""
        data = []
        for province in self.c_data:
            '''如果某个省份没有中高风险地区，则忽略该省份的数据'''
            if province['highDangerCount'] > 0 or province['midDangerCount'] > 0:
                p_data = {
                    'provinceName': province['provinceShortName'],
                    'highDanger': province['highDangerCount'],
                    'midDanger': province['midDangerCount'],
                    'midDangerAreas': [],
                    'highDangerAreas': [],
                    'cities': []
                }
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
                    if area['cityName'] in area_name:
                        p_data[danger_lv].append(area_name)
                    else:
                        p_data[danger_lv].append(area['cityName'] + area_name)
                for city in province['cities']:
                    """如果某个城市没有中高风险地区，则忽略该城市的数据"""
                    if city['highDangerCount'] > 0 or city['midDangerCount'] > 0:
                        cn_data = {
                            'cityName': city['cityName'],
                            'highDanger': city['highDangerCount'],
                            'midDanger': city['midDangerCount']
                        }
                        print(cn_data)
                        p_data['cities'].append(cn_data)
                data.append(p_data)
        return data


if __name__ == '__main__':
    # 在导入pycovid.py时检查网络连接
    covid = PyCovid()
    covid.cn_covid()
    try:
        status = requests.get('https://ncov.dxy.cn/', timeout=2).status_code
    except ConnectionError:
        raise ImportError('网络连接失败，如果想导入这个包，请检查网络连接')
    except RequestException:
        raise ImportError('网络连接失败，如果想导入这个包，请先检查网络连接')
    else:
        if status != 200:
            raise ImportError(f'网络连接失败，错误码：{status}如果想导入这个包，请先检查网络连接')
    print('网络连接成功')
