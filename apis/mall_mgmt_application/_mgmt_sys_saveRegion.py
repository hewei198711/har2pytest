import os

from util.client import client

data = {
    "cityCode": "",  # 城市编码
    "cityId": 0,  # 城市id
    "cityName": "",  # 城市名称
    "districtDTO": {"districtCode": "", "districtId": 0, "districtName": ""},  # 城市名称
    "provinceCode": "",  # 省份编码
    "streetDTO": {"streetCode": "", "streetId": 0, "streetName": ""},  # 街道信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_saveRegion(data=data, headers=headers):
    """
    新增或修改地区
    /mgmt/sys/saveRegion

    参数说明:
    - cityCode: 城市编码
    - cityId: 城市id
    - cityName: 城市名称
    - districtDTO: 城市名称
    - districtDTO.districtCode: 地区编码
    - districtDTO.districtId: 地区id
    - districtDTO.districtName: 地区名称
    - provinceCode: 省份编码
    - streetDTO: 街道信息
    - streetDTO.streetCode: 街乡镇编码
    - streetDTO.streetId: 街道id
    - streetDTO.streetName: 街乡镇名称
    """

    url = "/mgmt/sys/saveRegion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
