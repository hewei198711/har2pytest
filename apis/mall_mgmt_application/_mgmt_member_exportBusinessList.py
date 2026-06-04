import os

from util.client import client

params = {
    "businessType": "",  # 顾客类型：1->云商；2->微店（云+）
    "cardNo": "",  # 会员卡号
    "channel": "",  # 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    "companyNo": "",  # 分公司编号
    "openCardTime": "",  # 开卡开始时间,开卡结束时间
    "registrationTime": "",  # 创建开始时间,创建结束时间
    "status": "",  # 状态：0->正常；1->异常
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_exportBusinessList(params=params, headers=headers):
    """
    批量导出云商微店
    /mgmt/member/exportBusinessList

    参数说明:
    - businessType: 顾客类型：1->云商；2->微店（云+）
    - cardNo: 会员卡号
    - channel: 注册渠道：1->H5；2->APP；3->小程序；4->PC；5->填表
    - companyNo: 分公司编号
    - openCardTime: 开卡开始时间,开卡结束时间
    - registrationTime: 创建开始时间,创建结束时间
    - status: 状态：0->正常；1->异常
    """

    url = "/mgmt/member/exportBusinessList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
