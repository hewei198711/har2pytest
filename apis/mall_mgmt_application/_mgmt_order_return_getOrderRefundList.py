import os

from util.client import client

data = {
    "applyBeginTime": "",  # 申请退货开始时间
    "applyEndTime": "",  # 申请退货结束时间
    "creatorCard": "",  # 开单人卡号
    "financeCompanyCode": "",  # 财务分公司编号
    "from": 0,  # TODO: 添加参数说明
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payType": 0,  # 付款方式，101：微信；102：支付宝；103：银联；201：工商银行；202：建设银行；203：邮政存蓄银行；204：交通银行；205：平安代扣；800：完美钱包 801: 完美钱包+工商银行支付  802:完美钱包+建设银行支付   803:完美钱包+交通银行支付  804:完美钱包+银联支付  805:完美钱包+微信支付  806:完美钱包+支付宝支付  807:完美钱包+邮政储蓄银行支付  808:完美钱包+平安代扣支付
    "refundBeginTime": "",  # 申请退款开始时间
    "refundEndTime": "",  # 申请退款结束时间
    "refundStatus": 0,  # 退款进度 2->退款中 4->待对账校验 5->成功退款到钱包
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_getOrderRefundList(data=data, headers=headers):
    """
    管理后台-顾客订单退款失败记录查询
    /mgmt/order/return/getOrderRefundList

    参数说明:
    - applyBeginTime: 申请退货开始时间
    - applyEndTime: 申请退货结束时间
    - creatorCard: 开单人卡号
    - financeCompanyCode: 财务分公司编号
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - payType: 付款方式，101：微信；102：支付宝；103：银联；201：工商银行；202：建设银行；203：邮政存蓄银行；204：交通银行；205：平安代扣；800：完美钱包 801: 完美钱包+工商银行支付  802:完美钱包+建设银行支付   803:完美钱包+交通银行支付  804:完美钱包+银联支付  805:完美钱包+微信支付  806:完美钱包+支付宝支付  807:完美钱包+邮政储蓄银行支付  808:完美钱包+平安代扣支付
    - refundBeginTime: 申请退款开始时间
    - refundEndTime: 申请退款结束时间
    - refundStatus: 退款进度 2->退款中 4->待对账校验 5->成功退款到钱包
    """

    url = "/mgmt/order/return/getOrderRefundList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
