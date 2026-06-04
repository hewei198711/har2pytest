import os

from util.client import client

params = {
    "businessMode": 0,  # 保证金类型，1/1:3，2/85%
    "from": 0,  # TODO: 添加参数说明
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "shopType": 0,  # 网点类型
    "status": 0,  # 签署管理状态，0：已关闭，1：已开启
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportContractSignControlList(params=params, headers=headers):
    """
    导出服务中心签署控制管理列表
    /mgmt/store/exportContractSignControlList

    参数说明:
    - businessMode: 保证金类型，1/1:3，2/85%
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - pageNum: 页数
    - pageSize: 每页显示数
    - shopType: 网点类型
    - status: 签署管理状态，0：已关闭，1：已开启
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/store/exportContractSignControlList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
