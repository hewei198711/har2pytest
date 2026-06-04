import os

from util.client import client

data = {
    "bindCodeList": [],  # 待绑定的地区编码集合
    "businessRange": 0,  # 业务范围: 1.B 2.C 3.B+C 4.赠品区域
    "depotId": 0,  # 仓库id
    "untieCodeList": [],  # 待解绑的地区编码集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_depot_province_save(data=data, headers=headers):
    """
    保存仓库省份信息
    /mgmt/sys/depot/province/save

    参数说明:
    - bindCodeList: 待绑定的地区编码集合
    - businessRange: 业务范围: 1.B 2.C 3.B+C 4.赠品区域
    - depotId: 仓库id
    - untieCodeList: 待解绑的地区编码集合
    """

    url = "/mgmt/sys/depot/province/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
