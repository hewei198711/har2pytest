import os

from util.client import client

data = {
    "certiTypeId": 0,  # 证件类型id
    "companyId": 0,  # 所属公司id
    "companyName": "",  # 所属公司名称
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 页码不能少于1,默认1
    "pageSize": 0,  # 显示条数不能少于1,默认10
    "remarks": "",  # 备注
    "startTime": "",  # 开设时间
    "status": 0,  # 状态
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getCerti(data=data, headers=headers):
    """
    分页展示证件
    /mgmt/sys/getCerti

    参数说明:
    - certiTypeId: 证件类型id
    - companyId: 所属公司id
    - companyName: 所属公司名称
    - endTime: 结束时间
    - pageNum: 页码不能少于1,默认1
    - pageSize: 显示条数不能少于1,默认10
    - remarks: 备注
    - startTime: 开设时间
    - status: 状态
    """

    url = "/mgmt/sys/getCerti"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
