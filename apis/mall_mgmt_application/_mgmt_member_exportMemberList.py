import os

from util.client import client

params = {
    "channel": "",  # 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    "memberId": "",  # 会员ID
    "mobile": "",  # 手机号
    "registrationTime": "",  # 注册开始时间,注册结束时间
    "showType": "",  # 显示方式：1->全部，2->当月新增（当月已购货），3->当月未购货
    "status": "",  # 状态：0->正常；1->异常
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_exportMemberList(params=params, headers=headers):
    """
    批量导出普通顾客
    /mgmt/member/exportMemberList

    参数说明:
    - channel: 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    - memberId: 会员ID
    - mobile: 手机号
    - registrationTime: 注册开始时间,注册结束时间
    - showType: 显示方式：1->全部，2->当月新增（当月已购货），3->当月未购货
    - status: 状态：0->正常；1->异常
    """

    url = "/mgmt/member/exportMemberList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
