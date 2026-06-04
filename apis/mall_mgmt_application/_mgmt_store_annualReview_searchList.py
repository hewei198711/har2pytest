import os

from util.client import client

data = {
    "endCommitTime": "",  # 提交时间(结束) 格式 yyyy-MM-dd
    "id": 0,  # TODO: 添加参数说明
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "reviewIsOpen": 0,  # 年审状态开关  0 开启 1 关闭 默认关闭
    "reviewTypes": "",  # 需年审模块, 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审，多个逗号隔开
    "startCommitTime": "",  # 提交时间(开始) 格式 yyyy-MM-dd
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_annualReview_searchList(data=data, headers=headers):
    """
    年审控制列表
    /mgmt/store/annualReview/searchList

    参数说明:
    - endCommitTime: 提交时间(结束) 格式 yyyy-MM-dd
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - reviewIsOpen: 年审状态开关  0 开启 1 关闭 默认关闭
    - reviewTypes: 需年审模块, 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审，多个逗号隔开
    - startCommitTime: 提交时间(开始) 格式 yyyy-MM-dd
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/store/annualReview/searchList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
