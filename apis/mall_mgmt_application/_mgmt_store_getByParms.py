import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "leaderCardNo": "",  # 负责人卡号
    "leaderId": 0,  # 负责人Id
    "leaderName": "",  # 负责人姓名
    "storeCode": "",  # 店铺编号
    "storeName": "",  # 店铺名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getByParms(params=params, headers=headers):
    """
    根据常用条件查询服务中心
    /mgmt/store/getByParms

    参数说明:
    - companyCode: 分公司编号
    - leaderCardNo: 负责人卡号
    - leaderId: 负责人Id
    - leaderName: 负责人姓名
    - storeCode: 店铺编号
    - storeName: 店铺名称
    """

    url = "/mgmt/store/getByParms"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
