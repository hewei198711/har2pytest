import os

from util.client import client

data = {
    "processType": 0,  # 处理方式(1:按月，每个自然月剩余可用押货退货额度重新计算)
    "remark": "",  # 备注
    "returnMaxAmount": 0.0,  # 服务中心退货最大额
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_addOrUpdateMortgageAmountMaxStoreReturn(data=data, headers=headers):
    """
    添加或修改服务中心可以退最大押货额
    /mgmt/inventory/mortgageAmount/addOrUpdateMortgageAmountMaxStoreReturn

    参数说明:
    - processType: 处理方式(1:按月，每个自然月剩余可用押货退货额度重新计算)
    - remark: 备注
    - returnMaxAmount: 服务中心退货最大额
    - storeCode: 店铺编号
    """

    url = "/mgmt/inventory/mortgageAmount/addOrUpdateMortgageAmountMaxStoreReturn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
