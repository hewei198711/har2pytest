import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "openShopType": 0,  # 开店保证金金额 0 全部  1、 金额为0  2 、金额不为0
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "shopType": 0,  # 网点类型
    "specialType": 0,  # 特批押货金额 0 全部  1 、金额为0  2、 金额不为0
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名字
    "verifyStatus": 0,  # 1通过 2.未通过  3待审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportDepositSearchList(params=params, headers=headers):
    """
    保证金余额列表导出
    /mgmt/store/exportDepositSearchList

    参数说明:
    - companyCode: 分公司编号
    - openShopType: 开店保证金金额 0 全部  1、 金额为0  2 、金额不为0
    - shopType: 网点类型
    - specialType: 特批押货金额 0 全部  1 、金额为0  2、 金额不为0
    - storeCode: 服务中心编号
    - storeName: 服务中心名字
    - verifyStatus: 1通过 2.未通过  3待审核
    """

    url = "/mgmt/store/exportDepositSearchList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
