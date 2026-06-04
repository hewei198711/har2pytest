import os

from util.client import client

params = {
    "aboutMobile": "",  # 关联手机号
    "businessType": "",  # 顾客类型：1->云商；2->微店（云+）
    "cardNo": "",  # 会员卡号
    "channel": "",  # 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    "companyNo": "",  # 分公司编号
    "mobile": "",  # 注册手机号
    "openCardTime": "",  # 开卡开始时间,开卡结束时间
    "pageNum": "",  # 当前页
    "pageSize": "",  # 每页显示数
    "registrationTime": "",  # 创建开始时间,创建结束时间
    "status": "",  # 状态：0->正常；1->异常
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_getBusinessList(params=params, headers=headers):
    """
    获取云商微店列表
    /mgmt/member/getBusinessList

    参数说明:
    - aboutMobile: 关联手机号
    - businessType: 顾客类型：1->云商；2->微店（云+）
    - cardNo: 会员卡号
    - channel: 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    - companyNo: 分公司编号
    - mobile: 注册手机号
    - openCardTime: 开卡开始时间,开卡结束时间
    - pageNum: 当前页
    - pageSize: 每页显示数
    - registrationTime: 创建开始时间,创建结束时间
    - status: 状态：0->正常；1->异常
    """

    url = "/mgmt/member/getBusinessList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
