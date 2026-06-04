import os

from util.client import client

params = {
    "channel": "",  # 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    "memberId": "",  # 会员ID
    "mobile": "",  # 手机号
    "pageNum": "",  # 当前页
    "pageSize": "",  # 每页显示数
    "registrationTime": "",  # 注册开始时间,注册结束时间
    "showType": "",  # 显示方式：1->全部，2->当月新增（当月已购货），3->当月未购货
    "status": "",  # 状态：0->正常；1->异常
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_getMemberList(params=params, headers=headers):
    """
    获取普通顾客列表
    /mgmt/member/getMemberList

    参数说明:
    - channel: 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    - memberId: 会员ID
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页显示数
    - registrationTime: 注册开始时间,注册结束时间
    - showType: 显示方式：1->全部，2->当月新增（当月已购货），3->当月未购货
    - status: 状态：0->正常；1->异常
    """

    url = "/mgmt/member/getMemberList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
