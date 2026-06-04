import os

from util.client import client

params = {
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "orderQrCodestatus": 0,  # 订单详情活码是否隐藏,0-否，1-是
    "status": 0,  # 活码状态，0-禁用，1-启用
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
    "storeQrCodestatus": 0,  # 门店导航活码是否隐藏,0-否，1-是
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_qrcode_exportStoreQrCodeList(params=params, headers=headers):
    """
    导出服务中心活码列表
    /mgmt/store/qrcode/exportStoreQrCodeList

    参数说明:
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - orderQrCodestatus: 订单详情活码是否隐藏,0-否，1-是
    - status: 活码状态，0-禁用，1-启用
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    - storeQrCodestatus: 门店导航活码是否隐藏,0-否，1-是
    """

    url = "/mgmt/store/qrcode/exportStoreQrCodeList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
