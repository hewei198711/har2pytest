import os

from util.client import client

data = {
    "businessRange": 0,  # 业务范围:1->B,2->C,3->B+C
    "cityCode": "",  # 市编码
    "cityName": "",  # 市
    "districtCode": "",  # 区县编码
    "districtName": "",  # 区县
    "provinceCode": "",  # 省编码
    "provinceName": "",  # 省
    "stcType": 0,  # 交通管理类型,1:立即生效; 2:定时生效;3:定时生效和失效
    "stcwId": 0,  # 交通管制提示语id
    "streetInfos": [{"streetCode": "", "streetName": ""}],  # 街道信息集合
    "timeOff": 0,  # 定时失效时间
    "timeUp": 0,  # 定时生效时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_traffic_addTrafficControl(data=data, headers=headers):
    """
    添加交通管制
    /mgmt/sys/traffic/addTrafficControl

    参数说明:
    - businessRange: 业务范围:1->B,2->C,3->B+C
    - cityCode: 市编码
    - cityName: 市
    - districtCode: 区县编码
    - districtName: 区县
    - provinceCode: 省编码
    - provinceName: 省
    - stcType: 交通管理类型,1:立即生效; 2:定时生效;3:定时生效和失效
    - stcwId: 交通管制提示语id
    - streetInfos: 街道信息集合
    - streetInfos.streetCode: 街道编码
    - streetInfos.streetName: 街道
    - timeOff: 定时失效时间
    - timeUp: 定时生效时间
    """

    url = "/mgmt/sys/traffic/addTrafficControl"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
