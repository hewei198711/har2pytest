import os

from util.client import client

params = {
    "controlType": "",  # 控制类型 1顾客自购单退货 2云商下单退货
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_getBaseReturnConfigByStoreCode(params=params, headers=headers):
    """
    获取服务中心基础退货配置信息及押货余额信息
    /mgmt/inventory/return/config/getBaseReturnConfigByStoreCode

    参数说明:
    - controlType: 控制类型 1顾客自购单退货 2云商下单退货
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/return/config/getBaseReturnConfigByStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
