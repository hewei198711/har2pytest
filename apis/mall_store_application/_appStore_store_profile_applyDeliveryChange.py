import os

from util.client import client

data = {
    "areaCode": "",  # 区/县code
    "areaName": "",  # 区/县名称
    "cityCode": "",  # 城市编码
    "cityName": "",  # 城市名称
    "detailAddress": "",  # 收货详细地址
    "provinceCode": "",  # 省份编码
    "provinceName": "",  # 省份名称
    "receiver": "",  # 收货人
    "receiverMobile": "",  # 收货人电话
    "streetCode": "",  # 街道code
    "streetName": "",  # 街道名称
    "submitRemark": "",  # 变更原因
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_applyDeliveryChange(data=data, headers=headers):
    """
    申请服务中心收货地址变更
    /appStore/store/profile/applyDeliveryChange

    参数说明:
    - areaCode: 区/县code
    - areaName: 区/县名称
    - cityCode: 城市编码
    - cityName: 城市名称
    - detailAddress: 收货详细地址
    - provinceCode: 省份编码
    - provinceName: 省份名称
    - receiver: 收货人
    - receiverMobile: 收货人电话
    - streetCode: 街道code
    - streetName: 街道名称
    - submitRemark: 变更原因
    """

    url = "/appStore/store/profile/applyDeliveryChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
