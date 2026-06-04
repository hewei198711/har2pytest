import os

from util.client import client

data = {
    "certiTypeId": 0,  # TODO: 添加参数说明
    "companyName": "",  # 公司
    "operatorNo": "",  # 下载人会员卡号/工号
    "pageNum": 0,  # 页 默认1
    "pageSize": 0,  # 每页数量 默认10
    "storeCode": "",  # 服务中心编号
    "validTimeEnd": "",  # 下载结束时间
    "validTimeStart": "",  # 下载开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_exportCertiDownLog(data=data, headers=headers):
    """
    公司证件下载日志
    /mgmt/sys/exportCertiDownLog

    参数说明:
    - companyName: 公司
    - operatorNo: 下载人会员卡号/工号
    - pageNum: 页 默认1
    - pageSize: 每页数量 默认10
    - storeCode: 服务中心编号
    - validTimeEnd: 下载结束时间
    - validTimeStart: 下载开始时间
    """

    url = "/mgmt/sys/exportCertiDownLog"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
