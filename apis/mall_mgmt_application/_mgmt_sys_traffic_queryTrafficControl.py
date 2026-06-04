import os

from util.client import client

data = {
    "cityCode": "",  # 市编码
    "districtCode": "",  # 区县编码
    "pageNum": 0,  # 页 默认1
    "pageSize": 0,  # 每页数量 默认10
    "provinceCode": "",  # 省编码
    "streetCode": "",  # 街道编码
    "trafficControlStatus": 0,  # 状态 1：生效 0：待生效（默认）-1：失效
    "wordsType": 0,  # 类型 0：不可发货 1：可发货但影响配送时效
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_traffic_queryTrafficControl(data=data, headers=headers):
    """
    分页查询交通管制
    /mgmt/sys/traffic/queryTrafficControl

    参数说明:
    - cityCode: 市编码
    - districtCode: 区县编码
    - pageNum: 页 默认1
    - pageSize: 每页数量 默认10
    - provinceCode: 省编码
    - streetCode: 街道编码
    - trafficControlStatus: 状态 1：生效 0：待生效（默认）-1：失效
    - wordsType: 类型 0：不可发货 1：可发货但影响配送时效
    """

    url = "/mgmt/sys/traffic/queryTrafficControl"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
