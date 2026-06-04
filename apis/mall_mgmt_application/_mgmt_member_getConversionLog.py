import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "conversionTime": "",  # 转换开始时间,转换结束时间
    "fromMemberType": "",  # 原会员标识：1->普通顾客；2->优惠顾客；3->云商；4->微店
    "memberId": "",  # 会员ID
    "mobile": "",  # 手机号码
    "pageNum": "",  # 当前页
    "pageSize": "",  # 每页显示数
    "toMemberType": "",  # 目标会员标识：1->普通顾客；2->优惠顾客；3->云商；4->微店
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_getConversionLog(params=params, headers=headers):
    """
    获取身份转换日志
    /mgmt/member/getConversionLog

    参数说明:
    - cardNo: 会员卡号
    - conversionTime: 转换开始时间,转换结束时间
    - fromMemberType: 原会员标识：1->普通顾客；2->优惠顾客；3->云商；4->微店
    - memberId: 会员ID
    - mobile: 手机号码
    - pageNum: 当前页
    - pageSize: 每页显示数
    - toMemberType: 目标会员标识：1->普通顾客；2->优惠顾客；3->云商；4->微店
    """

    url = "/mgmt/member/getConversionLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
