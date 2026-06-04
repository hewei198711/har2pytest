import os

from util.client import client

data = {
    "backstageTransType": 0,  # 后端交易类型 1:充值 2:购货转入 3:退货转入 4:购货支付 5:提现 6:原路退款 7:信用额增加8:信用额扣减 9:还欠款 10:补银行流水 11:手工退款 12: 押货款与钱包互转 13:其他  14:定金转入 15:预售定金 16:定金返还17:信用额(兼容月结报表明细查询) 18:购货支付（签约购） 19:退货转入（签约购） 20:签约款汇入 21:签约款冻结 22:签约款支付 23:签约款解冻
    "creditEnable": False,  # 是否有信用额
    "flowEnable": False,  # 是否显示二级流水
    "from": 0,  # TODO: 添加参数说明
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "receptionTransType": 0,  # 前端交易类型 1:汇入,2:退货，3:购货 4:提现,5:退款,6:信用额,7:转款 8:其他 9 预售定金 10 定金返还 11 签约 12 解约 13 签约款支付
    "reportField": 0,  # 报表字段 1:本期汇款 2:本期使用 3：本期提现 4:信用额增减(兼容月结报表明细查询) 5:信用额扣减(兼容月结报表明细查询)
    "transMonthEnd": "",  # 交易月份结束
    "transMonthStart": "",  # 交易月份开始
    "walletId": 0,  # 钱包id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_exportWalletBillList(data=data, headers=headers):
    """
    完美钱包管理-钱包交易详情批量导出
    /mgmt/fin/wallet/exportWalletBillList

    参数说明:
    - backstageTransType: 后端交易类型 1:充值 2:购货转入 3:退货转入 4:购货支付 5:提现 6:原路退款 7:信用额增加8:信用额扣减 9:还欠款 10:补银行流水 11:手工退款 12: 押货款与钱包互转 13:其他  14:定金转入 15:预售定金 16:定金返还17:信用额(兼容月结报表明细查询) 18:购货支付（签约购） 19:退货转入（签约购） 20:签约款汇入 21:签约款冻结 22:签约款支付 23:签约款解冻
    - creditEnable: 是否有信用额
    - flowEnable: 是否显示二级流水
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - receptionTransType: 前端交易类型 1:汇入,2:退货，3:购货 4:提现,5:退款,6:信用额,7:转款 8:其他 9 预售定金 10 定金返还 11 签约 12 解约 13 签约款支付
    - reportField: 报表字段 1:本期汇款 2:本期使用 3：本期提现 4:信用额增减(兼容月结报表明细查询) 5:信用额扣减(兼容月结报表明细查询)
    - transMonthEnd: 交易月份结束
    - transMonthStart: 交易月份开始
    - walletId: 钱包id
    """

    url = "/mgmt/fin/wallet/exportWalletBillList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
