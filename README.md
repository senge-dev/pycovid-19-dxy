# pycovid-19-dxy
Python 新冠肺炎疫情数据，支持获取国内、全球、国内各个省份的疫情数据和国内的中高风险地区

## 数据类型
轻松几行代码获取丁香园的疫情数据，支持的数据有：
>国内疫情数据
>- 现存确诊
>- 累计确诊
>- 累计治愈
>- 累计死亡
>
>注意事项：
>- 如果某个地区从未有过确诊病例（累计确诊为0），则不会显示当地的确诊情况

>各个省份的疫情数据(不含港澳台)
>- 现存确诊
>- 累计确诊
>- 累计治愈
>- 累计死亡
>
>注意事项：
>- 如果某个地区从未有过确诊病例（累计确诊为0），则不会显示当地的确诊情况，如：日喀则、林芝等地区
>- 剔除了待明确地区、境外输入等词汇

>国内的风险地区
>- 高风险地区数量（省份、城市）
>- 中风险地区数量（省份、城市）
>- 高风险地区（区域）
>- 中风险地区（区域）
>
>注意事项：
>- 如果某个地区全域均为低风险地区，则自动忽略当地的数据

>全球疫情数据
>- 现存确诊
>- 累计确诊
>- 累计治愈
>- 累计死亡
>- 新增确诊
>- 新增治愈
>- 新增死亡
>
> 注意事项：
> - 如果某个国家从未有过确诊病例（累计确诊为0），则该国家不会显示出来

## 使用方法

### 如何安装

```bash
python -m pip install pycovid-19-dxy
```

### 获取上海市的疫情数据
```python
import json
from pycovid.covid import PyCovid
covid = PyCovid()
shanghai_covid = covid.province_covid(province='上海市', include_province_name=True)
print(json.dumps(shanghai_covid, ensure_ascii=False, indent=4))
```
如需获取其他省份、自治区、直辖市的详细数据，请将上海市改为其他地区，如：河南省、新疆维吾尔自治区等。

province参数支持简称，可以用简称替代省份全名，如果你想要获取广西壮族自治区的疫情数据，可以用“广西”替代。

输出内容(只显示部分地区，获取时间为2022年7月1日，实际运行数据会有所变化)：
```json
{
    "provinceName": "上海市",
    "data": [
        {
            "cityName": "浦东新区",
            "currentConfirmed": 391,
            "confirmed": 17129,
            "cured": 16737,
            "dead": 1
        },
        "......",
        {
            "cityName": "金山区",
            "currentConfirmed": 1,
            "confirmed": 338,
            "cured": 337,
            "dead": 0
        }
    ]
}
```

### 获取国内的疫情数数据

```python
from pycovid.covid import PyCovid
import json

covid = PyCovid()
cn_covid = covid.cn_covid()
print(json.dumps(cn_covid, ensure_ascii=False, indent=4))
```
输出内容(只显示部分省份，获取时间为2022年7月1日，实际运行数据会有所变化)
```json
[
    {
        "provinceName": "台湾",
        "currentConfirmed": 3782535,
        "confirmed": 3803049,
        "cured": 13742,
        "dead": 6772
    },
    {
        "provinceName": "香港",
        "currentConfirmed": 264700,
        "confirmed": 338065,
        "cured": 63964,
        "dead": 9401
    },
    "......",
    {
        "provinceName": "宁夏",
        "currentConfirmed": 0,
        "confirmed": 122,
        "cured": 122,
        "dead": 0
    },
    {
        "provinceName": "西藏",
        "currentConfirmed": 0,
        "confirmed": 1,
        "cured": 1,
        "dead": 0
    }
]
```
### 获取国内风险地区

```python
from pycovid.covid import PyCovid
import json

covid = PyCovid()
danger_areas = covid.danger_areas()
print(json.dumps(danger_areas, ensure_ascii=False, indent=4))
```
输出内容(只显示部分地区，获取时间为2022年7月1日，实际运行数据会有所变化)
```json
[
    {
        "provinceName": "上海",
        "highDanger": 0,
        "midDanger": 2,
        "midDangerAreas": [
            "奉贤区金汇镇梅园村部分区域（东至航塘港，西至航塘公路，南至梅园9组小排河，北至浦东/奉贤界河）",
            "静安区芷江西路街道西藏北路新赵家宅（36号、51-112号、119-120号）"
        ],
        "highDangerAreas": [],
        "cities": [
            {
                "cityName": "静安区",
                "highDanger": 0,
                "midDanger": 1
            },
            {
                "cityName": "奉贤区",
                "highDanger": 0,
                "midDanger": 1
            }
        ]
    },
    {
        "provinceName": "北京",
        "highDanger": 1,
        "midDanger": 0,
        "midDangerAreas": [],
        "highDangerAreas": [
            "昌平区小汤山镇大汤山村双兴苑小区"
        ],
        "cities": [
            {
                "cityName": "昌平区",
                "highDanger": 1,
                "midDanger": 0
            }
        ]
    },
    {
        "provinceName": "江苏",
        "highDanger": 0,
        "midDanger": 1,
        "midDangerAreas": [
            "南京六合区龙池街道沿河花园小区"
        ],
        "highDangerAreas": [],
        "cities": [
            {
                "cityName": "南京",
                "highDanger": 0,
                "midDanger": 1
            }
        ]
    }
]
```
### 获取全球疫情数据

```python
from pycovid.covid import PyCovid
import json

covid = PyCovid()
world_covid = covid.world_covid()
print(json.dumps(world_covid, ensure_ascii=False, indent=4))
```
输出内容(只显示部分国家，获取时间为2022年7月1日，实际运行数据会有所变化，部分国家可能数据有误，实际请以官方通报为准)
```json
[
    {
        "countryNameEn": "France",
        "countryNameCn": "法国",
        "currentConfirmed": 30493550,
        "confirmed": 31011133,
        "cured": 368023,
        "dead": 149560,
        "confirmedIncr": 124724,
        "curedIncr": 0,
        "deadIncr": 48
    },
    "......",
    {
        "countryNameEn": "South Africa",
        "countryNameCn": "南非",
        "currentConfirmed": -32147337,
        "confirmed": 3717067,
        "cured": 35764384,
        "dead": 100020,
        "confirmedIncr": 0,
        "curedIncr": 0,
        "deadIncr": 0
    }
]
```

## 免责说明

本程序完全免费使用且使用GNU GPL v3协议开源，禁止用于商业用途

