import os

from util.client import client

data = {
    "beginRestrictedDate": "",  # 受限/被控开始时间 yyyy-MM-dd HH:mm:ss
    "channelCode": "",  # 支付通道编码 101、微信支付;102、支付宝支付;103、银联;106、数字人民币 201、工商银行;202、建设银行;203、邮政储蓄银行;
    "companyCode": "",  # 受控/被控分公司编号
    "controlSource": 0,  # 管控来源 1、内部 2、外部单位
    "endRestrictedDate": "",  # 受限/被控开始时间 yyyy-MM-dd HH:mm:ss
    "from": 0,  # TODO: 添加参数说明
    "memberType": "",  # 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_queryCancelControlCashierConfig(data=data, headers=headers):
    """
    查询已取消管控列表
    /mgmt/fin/wallet/queryCancelControlCashierConfig

    参数说明:
    - beginRestrictedDate: 受限/被控开始时间 yyyy-MM-dd HH:mm:ss
    - channelCode: 支付通道编码 101、微信支付;102、支付宝支付;103、银联;106、数字人民币 201、工商银行;202、建设银行;203、邮政储蓄银行;
    - companyCode: 受控/被控分公司编号
    - controlSource: 管控来源 1、内部 2、外部单位
    - endRestrictedDate: 受限/被控开始时间 yyyy-MM-dd HH:mm:ss
    - memberType: 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/fin/wallet/queryCancelControlCashierConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
