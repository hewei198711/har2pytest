import os

from util.client import client

params = {
    "cityCode": "",  # 城市编码
    "districtCode": "",  # 地区编码
    "districtName": "",  # 地区搜索
    "pageNum": 0,  # 当前页码
    "pageSize": 0,  # 当前显示的条数
    "provinceCode": "",  # 省编码
    "streetName": "",  # 街道名
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_region_page(params=params, headers=headers):
    """
    分页查询地区信息
    /mgmt/sys/region/page

    参数说明:
    - cityCode: 城市编码
    - districtCode: 地区编码
    - districtName: 地区搜索
    - pageNum: 当前页码
    - pageSize: 当前显示的条数
    - provinceCode: 省编码
    - streetName: 街道名
    """

    url = "/mgmt/sys/region/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
