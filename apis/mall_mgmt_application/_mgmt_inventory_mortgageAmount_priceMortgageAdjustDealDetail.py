import os

from util.client import client

params = {
    "businessNo": "",  # 修数流水号
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_priceMortgageAdjustDealDetail(params=params, headers=headers):
    """
    5款调价商品修数详情
    /mgmt/inventory/mortgageAmount/priceMortgageAdjustDealDetail

    参数说明:
    - businessNo: 修数流水号
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/mortgageAmount/priceMortgageAdjustDealDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
