import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "isBadAssetStore": 0,  # 是否不良资产门店, 0->否 1->是';
    "operator": 0,  # 零售价运算符: 1为'>='，2为'>'，3为'<=',4为'<'
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "retailPrice": 0.0,  # 零售价合计
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_store_total(params=params, headers=headers):
    """
    库存合计（按服务中心维度）
    /mgmt/inventory/store/total

    参数说明:
    - companyCode: 分公司编号
    - isBadAssetStore: 是否不良资产门店, 0->否 1->是';
    - operator: 零售价运算符: 1为'>='，2为'>'，3为'<=',4为'<'
    - pageNum: 页数
    - pageSize: 页大小
    - retailPrice: 零售价合计
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/store/total"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
