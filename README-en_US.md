# pycovid-19-dxy

Python covid-19 data, you can get the data from the world or your country.

## How to use

### Installation

```bash
pip install pycovid-19-dxy
```

### Download Jupyter Notebook

If you want to see the result， please download our Jupyter Notebook, and then run it in your own computer.

- Download [Click it to download.](https://cdn.jsdelivr.net/gh/senge-studio/pycovid-19-dxy@main/demo-en_US.ipynb)

### Get the Covid-19 data from the world.

- This is a demo.

```python
from pycovid.covid_en import PyCovid
covid = PyCovid()
"""Get the covid-19 data from the world"""
data = covid.world_covid(
	current=True,                   # Current confirmed will be get default.
    confirmed=True,                 # Confirmed count will be get default.
    cured=True,                     # Cured count will be get default.
    dead=True,                      # Dead count will be get default.
    confirmed_incr=True,            # Confirmed increasement will be get default.
    cured_incr=True,                # Cured increasement will be get default.
    dead_incr=True,                 # Dead increasement will be get default.
    name=None,                      # The global data will be get default, if you want to get the data from your country, please set this paramenter to your country(English name).
    return_to_json=False            # If you want the json data, please set the paramenter to True.
)
"""If you don't want to add more paramenter, please set the paramenter as this."""
data = covid.world_covid()		    # It will get the covid-19 data from the world.
"""Get the dead count and dead increasement from Japan."""
data = covid.world_covid(
    current=False,                  # Ignore current confirmed count
    confirmed=False,                # Ignore confirmed count
    cured=False,                    # Ignore cured count
    confirmed_incr=False,           # Ignore confirmed increasement
    cured_incr=False,               # Ignore cured increasement
    name='Japan'
)
```

- The output of the default. This data is from `2022`-`07`-`04`.

```json
[
    {
        "countryName": "France",
        "currentConfirmed": 30751868,
        "confirmed": 31269545,
        "cured": 368023,
        "dead": 149654,
        "confirmedIncr": 125066,
        "curedIncr": 0,
        "deadIncr": 52
    },
    {
        "countryName": "Germany",
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
        "countryName": "Vatican City",
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

- Get the dead count and dead increasement from Japan, this data is from `2022`-`07`-`04`

```json
{
    "countryName": "Japan",
    "dead": 31309,
    "deadIncr": 11
}
```
