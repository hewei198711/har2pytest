import os

from util.client import client

data = {
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "type": 0,  # 配置类型，前端不用传
    "value": "",  # 配置值，比如：传手机号码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getMobiNoDelyConfList(data=data, headers=headers):
    """
    指定手机号不发货配置-列表
    /mgmt/sys/getMobiNoDelyConfList

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    - type: 配置类型，前端不用传
    - value: 配置值，比如：传手机号码
    """

    url = "/mgmt/sys/getMobiNoDelyConfList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
