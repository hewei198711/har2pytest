import os

from util.client import client

data = {
    "beginFeeMonth": "",  # 开始月份
    "channelCode": "",  # 二级支付通道   CCB：中国建设银行;ICBC_TOB_WITHHOLD：工行签约代扣（新） WEIXIN:微信支付 ALIPAY:支付宝支付
    "endFeeMonth": "",  # 结束月份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_querySumFinPayChannelFee(data=data, headers=headers):
    """
    统计商城各支付通道合计信息
    /mgmt/fin/wallet/querySumFinPayChannelFee

    参数说明:
    - beginFeeMonth: 开始月份
    - channelCode: 二级支付通道   CCB：中国建设银行;ICBC_TOB_WITHHOLD：工行签约代扣（新） WEIXIN:微信支付 ALIPAY:支付宝支付
    - endFeeMonth: 结束月份
    """

    url = "/mgmt/fin/wallet/querySumFinPayChannelFee"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
