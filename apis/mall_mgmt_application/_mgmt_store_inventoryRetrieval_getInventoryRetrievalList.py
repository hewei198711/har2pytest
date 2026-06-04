import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "endSubmitTime": "",  # 结束提交时间,格式yyyy-MM-dd HH:mm:ss
    "leaderCardNo": "",  # 负责人卡号
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "startSubmitTime": "",  # 起始提交时间,格式yyyy-MM-dd HH:mm:ss
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "submitterNo": "",  # 提交人工号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_inventoryRetrieval_getInventoryRetrievalList(params=params, headers=headers):
    """
    获取库存检索列表
    /mgmt/store/inventoryRetrieval/getInventoryRetrievalList

    参数说明:
    - companyCode: 分公司编号
    - endSubmitTime: 结束提交时间,格式yyyy-MM-dd HH:mm:ss
    - leaderCardNo: 负责人卡号
    - pageNum: pageNum
    - pageSize: pageSize
    - startSubmitTime: 起始提交时间,格式yyyy-MM-dd HH:mm:ss
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - submitterNo: 提交人工号
    """

    url = "/mgmt/store/inventoryRetrieval/getInventoryRetrievalList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
