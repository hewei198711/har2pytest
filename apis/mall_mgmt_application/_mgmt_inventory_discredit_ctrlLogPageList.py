import os

from util.client import client

data = {
    "ctrlEndDay": "",  # 操作日期(结束)  格式yyyy-MM-dd
    "ctrlMan": "",  # 操作人
    "ctrlStartDay": "",  # 操作日期(开始)  格式yyyy-MM-dd
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_discredit_ctrlLogPageList(data=data, headers=headers):
    """
    操作日志分页列表
    /mgmt/inventory/discredit/ctrlLogPageList

    参数说明:
    - ctrlEndDay: 操作日期(结束)  格式yyyy-MM-dd
    - ctrlMan: 操作人
    - ctrlStartDay: 操作日期(开始)  格式yyyy-MM-dd
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/discredit/ctrlLogPageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
