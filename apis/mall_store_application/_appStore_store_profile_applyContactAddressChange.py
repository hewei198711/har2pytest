import os

from util.client import client

data = {
    "areaCode": "",  # 区/县code
    "areaName": "",  # 区/县名称
    "cityCode": "",  # 城市编码
    "cityName": "",  # 城市名称
    "detailAddress": "",  # 联系地址详细地址（门牌号）
    "provinceCode": "",  # 省编码
    "provinceName": "",  # 省名称
    "streetCode": "",  # 街道code
    "streetName": "",  # 街道名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_applyContactAddressChange(data=data, headers=headers):
    """
    申请负责人联系地址信息变更(直接通过，不需要审核)
    /appStore/store/profile/applyContactAddressChange

    参数说明:
    - areaCode: 区/县code
    - areaName: 区/县名称
    - cityCode: 城市编码
    - cityName: 城市名称
    - detailAddress: 联系地址详细地址（门牌号）
    - provinceCode: 省编码
    - provinceName: 省名称
    - streetCode: 街道code
    - streetName: 街道名称
    """

    url = "/appStore/store/profile/applyContactAddressChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
