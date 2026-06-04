import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 服务中心编号
    "verifyStatus": 0,  # 审核状态 0 全部  1通过 2不通过 3没审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_listMortgageAmountMaxRemitInfo(params=params, headers=headers):
    """
    服务中心押货额度详情--全部/待审核
    /mgmt/inventory/mortgageAmount/listMortgageAmountMaxRemitInfo

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编号
    - verifyStatus: 审核状态 0 全部  1通过 2不通过 3没审核
    """

    url = "/mgmt/inventory/mortgageAmount/listMortgageAmountMaxRemitInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
