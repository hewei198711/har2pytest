import os

from util.client import client

data = {
    "companyCode": "",  # 分公司编号
    "endMonth": "",  # 结束月份期间(yyyy-MM)
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 页数
    "startMonth": "",  # 开始月份期间(yyyy-MM)
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_reportForm_remitPageList(data=data, headers=headers):
    """
    累计已汇押货款余额列表
    /mgmt/inventory/reportForm/remitPageList

    参数说明:
    - companyCode: 分公司编号
    - endMonth: 结束月份期间(yyyy-MM)
    - pageNum: 第几页
    - pageSize: 页数
    - startMonth: 开始月份期间(yyyy-MM)
    - storeCode: 店铺编号
    """

    url = "/mgmt/inventory/reportForm/remitPageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
