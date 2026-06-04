import os

from util.client import client

data = {
    "code": "",  # 服务中心编号
    "endTime": "",  # 变更结束时间, yyyy-MM
    "leaderCardNo": "",  # 负责人卡号
    "leaderName": "",  # 负责人姓名
    "name": "",  # 服务中心名称
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "startTime": "",  # 变更开始时间, yyyy-MM
    "type": 0,  # 变更类型：1-新增，2-修改，3-结点，4-恢复资格
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_addressChange_page(data=data, headers=headers):
    """
    分页查询服务中心地址变更
    /mgmt/store/addressChange/page

    参数说明:
    - code: 服务中心编号
    - endTime: 变更结束时间, yyyy-MM
    - leaderCardNo: 负责人卡号
    - leaderName: 负责人姓名
    - name: 服务中心名称
    - startTime: 变更开始时间, yyyy-MM
    - type: 变更类型：1-新增，2-修改，3-结点，4-恢复资格
    """

    url = "/mgmt/store/addressChange/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
