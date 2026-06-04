import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "endTime": "",  # 查询结束时间
    "freightCouponStatus": 0,  # 运费补贴券状态  1:已使用 2:未使用 3:占用中 4:已失效
    "freightSubsidyCode": "",  # 运费补贴券编码
    "from": 0,  # TODO: 添加参数说明
    "memberType": 0,  # 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）；5->店员；6->子账号
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "shopCode": "",  # 服务中心编码
    "startTime": "",  # 查询开始时间
    "subsidyReason": 0,  # 运费补贴原因 1:押货退货  2:押货换货  3:展业包订购单退货  4:展业包订购单换货  5:顾客订单退货  6:顾客订单换货
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_freight_subsidy_queryFreightSubsidyManagerInfo(data=data, headers=headers):
    """
    运费补贴券管理查询接口(商城后台)
    /mgmt/fin/voucher/freight/subsidy/queryFreightSubsidyManagerInfo

    参数说明:
    - cardNo: 会员卡号
    - endTime: 查询结束时间
    - freightCouponStatus: 运费补贴券状态  1:已使用 2:未使用 3:占用中 4:已失效
    - freightSubsidyCode: 运费补贴券编码
    - memberType: 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）；5->店员；6->子账号
    - mobile: 手机号码
    - pageNum: 页数
    - pageSize: 每页显示数
    - shopCode: 服务中心编码
    - startTime: 查询开始时间
    - subsidyReason: 运费补贴原因 1:押货退货  2:押货换货  3:展业包订购单退货  4:展业包订购单换货  5:顾客订单退货  6:顾客订单换货
    """

    url = "/mgmt/fin/voucher/freight/subsidy/queryFreightSubsidyManagerInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
