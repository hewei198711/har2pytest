import os

from util.client import client

data = {
    "businessModel": "",  # 经营模式 1:3 / 85%
    "effectTime": "",  # 生效时间
    "id": 0,  # 分配量ID,新增时为空
    "isCover": 0,  # 是否覆盖 0 不覆盖 ，1 覆盖
    "loseEffectTime": "",  # 失效时间
    "maxNum": 0,  # 最大可押数量
    "packing": "",  # 规格
    "productCode": "",  # 商品编号
    "productName": "",  # 商品名称
    "storeCode": "",  # 店铺编号
    "storeName": "",  # 店铺编号
    "unit": "",  # 单位
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distribution_addOrUpdateDistribution(data=data, headers=headers):
    """
    添加或更新分配量
    /mgmt/inventory/distribution/addOrUpdateDistribution

    参数说明:
    - businessModel: 经营模式 1:3 / 85%
    - effectTime: 生效时间
    - id: 分配量ID,新增时为空
    - isCover: 是否覆盖 0 不覆盖 ，1 覆盖
    - loseEffectTime: 失效时间
    - maxNum: 最大可押数量
    - packing: 规格
    - productCode: 商品编号
    - productName: 商品名称
    - storeCode: 店铺编号
    - storeName: 店铺编号
    - unit: 单位
    """

    url = "/mgmt/inventory/distribution/addOrUpdateDistribution"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
