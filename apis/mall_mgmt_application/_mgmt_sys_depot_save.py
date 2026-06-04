import os

from util.client import client

data = {
    "businessRange": 0,  # 业务范围: 1.B 2.C 3.B+C 4.赠品区域
    "depotCode": "",  # 仓库编码
    "depotName": "",  # 仓库名称
    "type": 0,  # 仓库类型: 1.成品仓 2.中转仓
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_save(data=data, headers=headers):
    """
    添加仓库
    /mgmt/sys/depot/save

    参数说明:
    - businessRange: 业务范围: 1.B 2.C 3.B+C 4.赠品区域
    - depotCode: 仓库编码
    - depotName: 仓库名称
    - type: 仓库类型: 1.成品仓 2.中转仓
    """

    url = "/mgmt/sys/depot/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
