import os

from util.client import client

data = {
    "applyReason": "",  # 申请原因
    "applyVoucherPic": [],  # 申请凭证
    "companyCode": "",  # 分公司编号
    "companyName": "",  # 分公司名称
    "leaderCardNo": "",  # 负责人卡号
    "leaderName": "",  # 负责人姓名
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_store_other_addOtherApply(data=data, headers=headers):
    """
    添加其他申请记录
    /appStore/web/store/other/addOtherApply

    参数说明:
    - applyReason: 申请原因
    - applyVoucherPic: 申请凭证
    - companyCode: 分公司编号
    - companyName: 分公司名称
    - leaderCardNo: 负责人卡号
    - leaderName: 负责人姓名
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/appStore/web/store/other/addOtherApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
