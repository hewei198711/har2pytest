import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "ctsName": "",  # 会员姓名
    "endTime": "",  # TODO: 添加参数说明
    "isAll": False,  # 是否展示全部数据,否则按 业务主题 设置的,展示状态进行展示
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 分页大小
    "planSceneId": 0,  # 业务主题ID
    "serverNo": "",  # 服务中心编号
    "shopkeeperId": 0,  # 服务中心管理员id
    "startTime": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_planSceneTheme_receiverList(data=data, headers=headers):
    """
    导入名单列表
    /mgmt/msgadmin/planSceneTheme/receiverList

    参数说明:
    - cardNo: 会员卡号
    - ctsName: 会员姓名
    - isAll: 是否展示全部数据,否则按 业务主题 设置的,展示状态进行展示
    - pageNum: 页码
    - pageSize: 分页大小
    - planSceneId: 业务主题ID
    - serverNo: 服务中心编号
    - shopkeeperId: 服务中心管理员id
    """

    url = "/mgmt/msgadmin/planSceneTheme/receiverList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
