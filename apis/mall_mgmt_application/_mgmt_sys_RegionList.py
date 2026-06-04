import os

from util.client import client

params = {
    "cityCode": "",  # 城市编码
    "districtCode": "",  # 地区编码
    "pageNum": "",  # 当前页码,默认为1
    "pageSize": "",  # 当前显示的条数,默认为10
    "provinceCode": "",  # 省编码
    "streetName": "",  # 街道名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_RegionList(params=params, headers=headers):
    """
    获取地区信息
    /mgmt/sys/RegionList

    参数说明:
    - cityCode: 城市编码
    - districtCode: 地区编码
    - pageNum: 当前页码,默认为1
    - pageSize: 当前显示的条数,默认为10
    - provinceCode: 省编码
    - streetName: 街道名
    """

    url = "/mgmt/sys/RegionList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
