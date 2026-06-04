import os

from util.client import client

params = {
    "areaName": "",  # 区/县
    "cityName": "",  # 城市
    "detailAddress": "",  # 服务中心详细地址(门牌号)
    "provinceName": "",  # 省份
    "streetName": "",  # 街道
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_checkBusinessAddressIsExist(params=params, headers=headers):
    """
    检查经营地址是否存在，返回重复的服务中心编码，返回空则表示无重复，
    /mgmt/store/checkBusinessAddressIsExist

    参数说明:
    - areaName: 区/县
    - cityName: 城市
    - detailAddress: 服务中心详细地址(门牌号)
    - provinceName: 省份
    - streetName: 街道
    """

    url = "/mgmt/store/checkBusinessAddressIsExist"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
