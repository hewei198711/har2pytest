import os

from util.client import client

data = {
    "createTimeMin": None,  # 创建时间始 yyyy-MM-dd HH:mm:ss
    "createTimeMax": None,  # 创建时间末 yyyy-MM-dd HH:mm:ss
    "remarkCode": None,  # 文案编号
    "remark": None,  # 文案
    "pageNum": 1,  # 当前页
    "pageSize": 10,  # 每页数量
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_luckyActivity_luckyBoxRemarkPage(data=data, headers=headers):
    """
    条件分页查询盲盒海报文案列表
    /mgmt/prmt/luckyActivity/luckyBoxRemarkPage

    参数说明:
    - createTimeMax: 创建时间末 yyyy-MM-dd HH:mm:ss
    - createTimeMin: 创建时间始 yyyy-MM-dd HH:mm:ss
    - pageNum: 当前页
    - pageSize: 每页数量
    - remark: 文案
    - remarkCode: 文案编号
    """

    url = "/mgmt/prmt/luckyActivity/luckyBoxRemarkPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
