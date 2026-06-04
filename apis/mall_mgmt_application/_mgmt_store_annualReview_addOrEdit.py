import os

from util.client import client

data = {
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "reviewIsOpen": 0,  # 年审状态开关  0 开启 1 关闭 默认关闭
    "reviewTypes": "",  # 需年审模块, 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审, 多个逗号隔开
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_annualReview_addOrEdit(data=data, headers=headers):
    """
    年审控制新增/编辑
    /mgmt/store/annualReview/addOrEdit

    参数说明:
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - reviewIsOpen: 年审状态开关  0 开启 1 关闭 默认关闭
    - reviewTypes: 需年审模块, 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审, 多个逗号隔开
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/store/annualReview/addOrEdit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
