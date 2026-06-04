import os

from util.client import client

data = {
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "orderQrCodestatus": 0,  # 订单详情活码是否隐藏,0-否，1-是
    "pageNum": 0,  # 页码 默认1
    "pageSize": 0,  # 页数 默认10
    "status": 0,  # 活码状态，0-禁用，1-启用
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "storeQrCodestatus": 0,  # 门店导航活码是否隐藏,0-否，1-是
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_qrcode_searchQrCode(data=data, headers=headers):
    """
    活码搜索
    /mgmt/store/qrcode/searchQrCode

    参数说明:
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - orderQrCodestatus: 订单详情活码是否隐藏,0-否，1-是
    - pageNum: 页码 默认1
    - pageSize: 页数 默认10
    - status: 活码状态，0-禁用，1-启用
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - storeQrCodestatus: 门店导航活码是否隐藏,0-否，1-是
    """

    url = "/mgmt/store/qrcode/searchQrCode"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
