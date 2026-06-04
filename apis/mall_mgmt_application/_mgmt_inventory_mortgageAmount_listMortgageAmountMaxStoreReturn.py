import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "leaderCardNo": "",  # 负责人卡号
    "leaderName": "",  # 负责人姓名
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_listMortgageAmountMaxStoreReturn(params=params, headers=headers):
    """
    分页查询服务中心可以退最大押货额
    /mgmt/inventory/mortgageAmount/listMortgageAmountMaxStoreReturn

    参数说明:
    - companyCode: 分公司编号
    - leaderCardNo: 负责人卡号
    - leaderName: 负责人姓名
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/inventory/mortgageAmount/listMortgageAmountMaxStoreReturn"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
