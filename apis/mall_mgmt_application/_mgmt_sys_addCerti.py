import os

from util.client import client

data = {
    "certiTypeId": 0,  # 证件类型id
    "companyId": 0,  # 公司id
    "companyName": "",  # 所属公司名称
    "fileUrl": "",  # 文件地址
    "id": 0,  # 主键id
    "remarks": "",  # 备注
    "status": 0,  # 状态：0.禁用，1.启用
    "validTime": "",  # 失效时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_addCerti(data=data, headers=headers):
    """
    增加证件
    /mgmt/sys/addCerti

    参数说明:
    - certiTypeId: 证件类型id
    - companyId: 公司id
    - companyName: 所属公司名称
    - fileUrl: 文件地址
    - id: 主键id
    - remarks: 备注
    - status: 状态：0.禁用，1.启用
    - validTime: 失效时间
    """

    url = "/mgmt/sys/addCerti"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
