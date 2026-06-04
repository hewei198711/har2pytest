import os

from util.client import client

data = {
    "endTime": "",  # 结束时间
    "msgType": "",  # 消息类型，与数据词典中消息类型绑定
    "pageNum": 0,  # 请求页码
    "pageSize": 0,  # 页的数量
    "startTime": "",  # 开始时间
    "status": "",  # 是否可用 :  0 否 ,1 : 是
    "templateCode": "",  # 模版code
    "templateName": "",  # 模板名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_manageTemplate_search(data=data, headers=headers):
    """
    站内信模板管理查询接口
    /mgmt/msgadmin/manageTemplate/search

    参数说明:
    - endTime: 结束时间
    - msgType: 消息类型，与数据词典中消息类型绑定
    - pageNum: 请求页码
    - pageSize: 页的数量
    - startTime: 开始时间
    - status: 是否可用 :  0 否 ,1 : 是
    - templateCode: 模版code
    - templateName: 模板名称
    """

    url = "/mgmt/msgadmin/manageTemplate/search"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
