import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "cardNoList": [],  # 会员卡号集合
    "commitEndTime": "",  # 提交结束时间，格式yyyy-MM
    "commitStartTime": "",  # 提交开始时间，格式yyyy-MM
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "phone": "",  # 注册手机号码
    "realname": "",  # 姓名
    "status": 0,  # 状态，1：生效中；2：已失效
    "type": 0,  # 类型，1：不可转分；2：不可被转分
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_getWeshopOrderPermissionList(data=data, headers=headers):
    """
    KOS转分权限列表
    /mgmt/weshop/getWeshopOrderPermissionList

    参数说明:
    - cardNo: 会员卡号
    - cardNoList: 会员卡号集合
    - commitEndTime: 提交结束时间，格式yyyy-MM
    - commitStartTime: 提交开始时间，格式yyyy-MM
    - pageNum: 页数
    - pageSize: 每页显示数
    - phone: 注册手机号码
    - realname: 姓名
    - status: 状态，1：生效中；2：已失效
    - type: 类型，1：不可转分；2：不可被转分
    """

    url = "/mgmt/weshop/getWeshopOrderPermissionList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
