# pycovid-19-dxy

Python 新冠肺炎疫情数据，支持获取全球各个国家、国内、国内各个省份以及各个城市的疫情数据、国内的中高风险地区、国内近一周和疫情有关的部分新闻。

- If you want to get the English documentation，please see[README-en_US.md](https://github.com/senge-studio/pycovid-19-dxy/main/README-en_US.md)
- 如果你想访问英文版的文档，请查看[README-en_US.md](https://github.com/senge-studio/pycovid-19-dxy/main/README-en_US.md)

## 使用方法

### 安装

```bash
pip install pycovid-19-dxy
```

### 下载Jupyter Notebook

如果您想查看程序运行效果，请下载我们的Jupyter Notebook，并在终端运行它。

- 下载地址 [点此下载](https://cdn.jsdelivr.net/gh/senge-studio/pycovid-19-dxy@main/demo.ipynb)

### 国内疫情数据

- 以上为示例

```python
from pycovid.covid import PyCovid
covid = PyCovid()
"""以下全部为默认参数"""
data = covid.cn_covid(
	current=True,			        # 是否显示现存确诊人数，默认显示
    confirmed=True,			        # 是否显示累计确诊人数，默认显示
    cured=True,				        # 是否显示累计治愈人数，默认显示
    dead=True,				        # 是否显示累计死亡人数，默认显示
    province_name=None,		        # 是否只获取某个省/自治区/直辖市/特别行政区的数据，默认全部获取
    return_to_json=False            # 是否返回json格式，默认不返回
)
"""如果你只想要北京市的累计确诊人数和累计治愈人数，你可以这样写"""
data = covid.cn_covid(
	current=False,
    dead=False,
    province_name='北京'
)
"""简单的参数设置可以这样写"""
data = covid.cn_covid()
```

- 默认参数输出结果（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准，其中已省略部分数据）

```json
[
    {
        "provinceName": "台湾",
        "currentConfirmed": 3849830,
        "confirmed": 3870528,
        "cured": 13742,
        "dead": 6956
    },
    {
        "provinceName": "香港",
        "currentConfirmed": 265358,
        "confirmed": 338934,
        "cured": 64171,
        "dead": 9405
    },
    {
        "provinceName": "澳门",
        "currentConfirmed": 297,
        "confirmed": 382,
        "cured": 83,
        "dead": 2
    },
    "......",
    {
        "provinceName": "西藏",
        "currentConfirmed": 0,
        "confirmed": 1,
        "cured": 1,
        "dead": 0
    }
]
```

- 获取北京市的累计治愈和累计确诊人数（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准）

```json
{
    "provinceName": "北京",
    "confirmed": 3685,
    "cured": 3657
}
```

### 获取某省份的疫情数据

- 以上为示例

```python
from pycovid.covid import PyCovid
covid = PyCovid()
"""以下全部为默认参数，示例为获取上海的疫情数据"""
data = covid.province_covid(
	province='上海',			        # 获取上海的疫情数据
    include_province_name=True,	    # 默认显示省份名称
    current=True,				    # 默认获取现存确诊数据
    confirmed=True,				    # 默认获取累计确诊数据
    cured=True,					    # 默认获取累计治愈数据
    dead=True,					    # 默认获取累计死亡数据
    city_name=None,				    # 默认获取全部数据(如果不为空，将忽略include_province_name参数)
    return_to_json=False            # 是否返回json格式，默认不返回
)
"""简单的参数设置可以这样写"""
data = covid.province_covid(province='上海')	# 本次获取上海的疫情数据，如果不填，默认获取北京的疫情数据
"""仅获取黄浦区的现存确诊疫情数据"""
data = covid.province_covid(
	province='上海',			        # 获取上海的疫情数据
    confirmed=False,			    # 不获取累计确诊数据
    cured=False,				    # 不获取累计治愈数据
    dead=False,					    # 不获取累计死亡数据
    city_name='黄浦区'			    # 只获取黄浦区的疫情数据
)
```

- 默认参数输出结果（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准，其中已省略部分数据）

```json
{
    "provinceName": "上海",
    "data": [
        {
            "cityName": "浦东新区",
            "currentConfirmed": 395,
            "confirmed": 17133,
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

- 获取上海市黄浦区现存确诊数据（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准）

```json
{
    "cityName": "黄浦区",
    "currentConfirmed": 163
}
```

### 获取全球疫情数据

- 以上为示例

```python
from pycovid.covid import PyCovid
covid = PyCovid()
"""获取全球疫情数据"""
data = covid.world_covid(
	current=True,                   # 默认获取现存确诊数据
    confirmed=True,                 # 默认获取累计确诊数据    
    cured=True,                     # 默认获取累计治愈数据
    dead=True,                      # 默认获取累计死亡数据
    confirmed_incr=True,            # 默认获取新增确诊数据
    cured_incr=True,                # 默认获取新增治愈数据
    dead_incr=True,                 # 默认获取新增死亡数据
    name=None,              # 默认获取全球数据，如果想获取某个国家的数据，可以传入国家名称，如获取日本的新冠肺炎数据，请传入`'日本'`或`'Japan'`
    return_to_json=False            # 是否返回json格式，默认不返回
)
"""简单的参数设置可以这样写"""
data = covid.world_covid()		    # 本次获取全球疫情数据，如果不填，默认获取现存确诊数据
"""获取日本的累计死亡和新增死亡人数"""
data = covid.world_covid(
    current=False,
    confirmed=False,
    cured=False,
    confirmed_incr=False,
    cured_incr=False,
    name='日本'               # 也可以使用`'Japan'`作为参数
)
```

- 默认参数输出结果（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准，其中已省略部分数据）

```json
[
    {
        "countryNameEn": "France",
        "countryNameCn": "法国",
        "currentConfirmed": 30751868,
        "confirmed": 31269545,
        "cured": 368023,
        "dead": 149654,
        "confirmedIncr": 125066,
        "curedIncr": 0,
        "deadIncr": 52
    },
    {
        "countryNameEn": "Germany",
        "countryNameCn": "德国",
        "currentConfirmed": 23922938,
        "confirmed": 28392630,
        "cured": 4328400,
        "dead": 141292,
        "confirmedIncr": 1,
        "curedIncr": 0,
        "deadIncr": 0
    },
    "......",
    {
        "countryNameEn": "",
        "countryNameCn": "梵蒂冈",
        "currentConfirmed": 2,
        "confirmed": 29,
        "cured": 27,
        "dead": 0,
        "confirmedIncr": 0,
        "curedIncr": 0,
        "deadIncr": 0
    }
]
```

- 获取日本的累计死亡和新增死亡人数数据（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准）

```json
{
    "countryNameEn": "Japan",
    "countryNameCn": "日本",
    "dead": 31309,
    "deadIncr": 11
}
```

### 获取国内中高风险地区

- 以上为示例

```python
from pycovid.covid import PyCovid
covid = PyCovid()
"""获取国内中高风险地区"""
data = covid.danger_areas(
    # 如果以下两个参数均为False，则只显示国内的中高风险地区有哪些而不会显示风险地区数量
    include_cities=True,            # 默认获取各个城市的中高风险地区数量
    include_counts=True,            # 默认显示各个省份的中高风险地区数量
    include_danger_areas=True,      # 默认显示中高风险地区的详细信息
    return_to_json=False            # 是否返回json格式，默认不返回
)
"""简单的参数设置可以这样写"""
data = covid.danger_areas()
"""只获取中高风险地区有哪些"""
data = covid.danger_areas(
    include_cities=False,
    include_counts=False
)
"""只获取各个城市的中高风险地区数量"""
data = covid.danger_areas(
    include_counts=False,
    include_danger_areas=False
)
```

- 默认参数的获取结果（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准，其中已省略部分数据）

```json
[
    {
        "provinceName": "上海",
        "midDangerAreas": [
            "奉贤区金汇镇梅园村部分区域（东至航塘港，西至航塘公路，南至梅园9组小排河，北至浦东/奉贤界河）",
            "静安区芷江西路街道西藏北路新赵家宅（36号、51-112号、119-120号）",
            "宝山区高境镇殷高西路333号长江国际生活广场东区二楼老炉家木炭烤肉店",
            "普陀区曹杨新村街道兰溪路148号耕耘茶室"
        ],
        "highDangerAreas": [
            "普陀区长风新村街道光复西路2077弄小区"
        ],
        "cities": [
            {
                "cityName": "静安区",
                "highDanger": 0,
                "midDanger": 1
            },
            {
                "cityName": "宝山区",
                "highDanger": 0,
                "midDanger": 1
            },
            {
                "cityName": "普陀区",
                "highDanger": 1,
                "midDanger": 1
            },
            {
                "cityName": "奉贤区",
                "highDanger": 0,
                "midDanger": 1
            }
        ],
        "highDanger": 1,
        "midDanger": 4
    },
    {
        "provinceName": "北京",
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
        ],
        "highDanger": 1,
        "midDanger": 0
    },
    {
        "provinceName": "陕西",
        "midDangerAreas": [
            "西安大兆街道东伍村",
            "西安大兆街道三益村",
            "西安长安区韦曲街道简王井村的其他区域"
        ],
        "highDangerAreas": [
            "西安曲江新区曲江香都社区万科蜜柚小区5号楼沿街3F-105店铺",
            "西安曲江新区中铁国际社区龙邸保障房小区",
            "西安长安区韦曲街道简王井村陕西朝辉再生资源交易集散市场（大风尚再生艺术馆）"
        ],
        "cities": [
            {
                "cityName": "西安",
                "highDanger": 3,
                "midDanger": 3
            }
        ],
        "highDanger": 3,
        "midDanger": 3
    }
]
```

- 只获取中高风险地区（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准，其中已省略部分数据）

```json
{
    "midDangerAreas": [
        "安徽省宿州滨河社区除封控区外的其他社区",
        "安徽省宿州草沟镇除高风险区外的其他区域",
        "......",
        "辽宁省丹东珍珠街道紫光福郡一期15号楼",
        "辽宁省大连沙河口区南沙河口街道幸福e家5期6区其他区域"
    ],
    "highDangerAreas": [
        "安徽省宿州 大庄镇王官村",
        "......",
        "辽宁省丹东振兴区永昌街道保利一期A2区5号楼",
        "辽宁省大连沙河口区南沙河口街道幸福e家5期6区28号楼"
    ]
}
```

- 只获取中高风险地区数量（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准，其中已省略部分数据）

```json
[
    {
        "provinceName": "安徽",
        "cities": [
            {
                "cityName": "宿州",
                "highDanger": 118,
                "midDanger": 18
            }
        ]
    },
    "......",
    {
        "provinceName": "辽宁",
        "cities": [
            {
                "cityName": "大连",
                "highDanger": 1,
                "midDanger": 1
            },
            {
                "cityName": "丹东",
                "highDanger": 14,
                "midDanger": 18
            }
        ]
    }
]
```

### 获取和疫情相关的新闻

- 获取和疫情相关的新闻

```python
from pycovid.covid import PyCovid
covid = PyCovid()
"""获取和疫情相关的新闻"""
news = covid.news_timeline(
    include_summary=True,           # 默认包含新闻摘要
    include_url=True,               # 默认包含新闻链接
    include_source=True,            # 默认包含新闻来源
    include_time=True,              # 默认包含新闻发布时间
    return_to_json=False,           # 是否返回json格式的新闻，默认不返回
)
"""简单的参数设置"""
news = covid.news_timeline()
"""获取和疫情相关的新闻，并且只包含新闻标题"""
news = covid.news_timeline(
    include_summary=False,
    include_url=False,
    include_source=False,
    include_time=False
)
```

- 获取结果（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准）
```json
[
    {
        "title": "国家卫健委 | 昨日新增本土 41+339 例",
        "publishedTime": "5小时前",
        "source": "央视新闻app",
        "url": "https://content-static.cctvnews.cctv.com/snow-book/index.html?item_id=12277325987870621055&toc_style_id=feeds_default",
        "summary": "7月3日0—24时，31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例72例。其中境外输入病例31例（广东9例，上海7例，福建5例，内蒙古2例，浙江2例，北京1例，天津1例，辽宁1例，江西1例，河南1例，四川1例），含7例由无症状感染者转为确诊病例（广东4例，天津1例，福建1例，河南1例）；本土病例41例（安徽29例，江苏4例，山东4例，上海2例，福建1例，广东1例），含2例由无症状感染"
    },
    {
        "title": "安徽 | 昨日新增本土确诊病例 29 例 ",
        "publishedTime": "6小时前",
        "source": "央视新闻app",
        "url": "https://content-static.cctvnews.cctv.com/snow-book/index.html?item_id=14021295083563446065&toc_style_id=feeds_default",
        "summary": "2022年7月3日0-24时，安徽省报告新增确诊病例29例（均在宿州市泗县，其中1例系已报告的无症状感染者转为确诊病例），无新增疑似病例，新增无症状感染者258例（宿州市灵璧县30例、泗县227例、埇桥区1例）。\n6月26日至7月3日24时，安徽省共报告确诊病例134例，其中境外输入1例，宿州市泗县132例、灵璧县1例；共报告无症状感染者724例。"
    },
    {
        "title": "江苏 | 昨日新增本土确诊病例 4 例 ",
        "publishedTime": "5小时前",
        "source": "央视新闻app",
        "url": "https://content-static.cctvnews.cctv.com/snow-book/index.html?item_id=11305596967674794648&toc_style_id=feeds_default",
        "summary": "江苏省卫健委7月4日通报：7月3日0—24时，江苏新增本土确诊病例4例（无锡市1例，徐州市3例，均在定点医院隔离治疗），新增本土无症状感染者52例（无锡市34例，徐州市16例，苏州市1例，盐城市1例，均在定点医院接受隔离医学管理）。\n新增境外输入无症状感染者3例。新增出院病例1例（境外输入）。新增解除隔离医学管理的无症状感染者2例（均为境外输入）。\n目前，在定点医院隔离治疗的确诊病例24例（本土1"
    },
    {
        "title": "山东 | 昨日新增本土确诊病例 3 例",
        "publishedTime": "13小时前",
        "source": "央视新闻app",
        "url": "https://content-static.cctvnews.cctv.com/snow-book/index.html?item_id=3287854146740678376&toc_style_id=feeds_default",
        "summary": "据山东青岛市卫生健康委员会通报，2022年7月3日0时至24时，青岛市黄岛区新增3例本土确诊病例（轻型），新增4例本土无症状感染者。\n以上7人均系集中隔离管控人员，7月3日例行核酸检测结果均为阳性，由120负压救护车转运至定点医院接受隔离治疗，结合流行病学史、临床表现和实验室检测结果，专家组诊断其中3人为新冠肺炎确诊病例（轻型）、4人为无症状感染者。\n（总台记者 王伟 王子璇）"
    },
    {
        "title": "上海 | 昨日新增本土确诊病例 2 例 ",
        "publishedTime": "6小时前",
        "source": "央视新闻app",
        "url": "https://content-static.cctvnews.cctv.com/snow-book/index.html?item_id=6006725740994437072&toc_style_id=feeds_default",
        "summary": "上海市卫健委今早（7月4日）通报：2022年7月3日0—24时，新增本土新冠肺炎确诊病例2例和无症状感染者1例，其中2例确诊病例在隔离管控中发现。新增境外输入性新冠肺炎确诊病例7例和无症状感染者12例，均在闭环管控中发现。（总台记者 王殿甲 杨静）"
    }
]
```

- 获取新闻标题（以下内容为`2022`-`07`-`04`的数据，当前数据请以官方报道为准）

```json
[
    {
        "title": "国家卫健委 | 昨日新增本土 41+339 例"
    },
    {
        "title": "安徽 | 昨日新增本土确诊病例 29 例 "
    },
    {
        "title": "江苏 | 昨日新增本土确诊病例 4 例 "
    },
    {
        "title": "山东 | 昨日新增本土确诊病例 3 例"
    },
    {
        "title": "上海 | 昨日新增本土确诊病例 2 例 "
    }
]
```