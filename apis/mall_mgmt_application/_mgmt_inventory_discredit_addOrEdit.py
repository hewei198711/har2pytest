import os

from util.client import client

data = {
    "adjustAmount": 0.0,  # 调整金额
    "adjustRemark": "",  # 调整备注
    "companyCode": "",  # 分公司编号
    "companyName": "",  # 分公司名称
    "creditAmount": 0.0,  # 当前信誉额
    "effectTime": "",  # 生效时间
    "entryFrom": "",  # 入口
    "returnTime": "",  # 归还时间
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_discredit_addOrEdit(data=data, headers=headers):
    """
    信誉额调整/新建
    /mgmt/inventory/discredit/addOrEdit

    参数说明:
    - adjustAmount: 调整金额
    - adjustRemark: 调整备注
    - companyCode: 分公司编号
    - companyName: 分公司名称
    - creditAmount: 当前信誉额
    - effectTime: 生效时间
    - entryFrom: 入口
    - returnTime: 归还时间
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/inventory/discredit/addOrEdit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
