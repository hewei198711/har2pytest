import os

from util.client import client

params = {
    "aboutMobile": "",  # 关联手机号
    "cardNo": "",  # 会员卡号
    "certificatesNo": "",  # 证件号
    "channel": "",  # 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    "memberId": "",  # 会员ID
    "memberNo": "",  # 顾客编号
    "mobile": "",  # 手机号
    "pageNum": "",  # 当前页
    "pageSize": "",  # 每页显示数
    "realname": "",  # 真实姓名
    "registrationTime": "",  # 注册开始时间,注册结束时间
    "showType": "",  # 显示方式：1->全部，2->当月新增（当月已购货），3->当月未购货
    "status": "",  # 状态：0->正常；1->异常
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_getVipList(params=params, headers=headers):
    """
    获取优惠顾客列表
    /mgmt/member/getVipList

    参数说明:
    - aboutMobile: 关联手机号
    - cardNo: 会员卡号
    - certificatesNo: 证件号
    - channel: 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    - memberId: 会员ID
    - memberNo: 顾客编号
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页显示数
    - realname: 真实姓名
    - registrationTime: 注册开始时间,注册结束时间
    - showType: 显示方式：1->全部，2->当月新增（当月已购货），3->当月未购货
    - status: 状态：0->正常；1->异常
    """

    url = "/mgmt/member/getVipList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
