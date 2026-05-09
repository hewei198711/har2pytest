import os

from util.client import client

data = {
    "batchNo": 0,  # 处理批次号
    "cardNo": "",  # 顾客卡号
    "companyCode": "",  # 分公司编码
    "extChannelCode": [],  # 外部接口通道
    "feeMonth": "",  # 月份
    "feeType": 0,  # 手续费类型，101：微信；102：支付宝；103：银联；107：银联无感付；108：银联自动扣款； 201：工商银行；202：建设银行；203：邮政存蓄银行；204：交通银行；205：平安代扣 206：工行分期付；207：工商银行（新）；
    "from": 0,  # TODO: 添加参数说明
    "leaderCardNo": "",  # 负责人卡号
    "memberType": 0,  # 会员类型 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）；5->店员；6->子账号
    "operateTypePageCode": "",  # 手续费页签操作编码 operateTypeCode001:普通顾客 operateTypeCode002:优惠顾客 operateTypeCode003:云商/云+  operateTypeCode004:云商/云+(工行分期付) operateTypeCode005:云商/云+(银联定期付) operateTypeCode006:云商/云+(银联签约付) operateTypeCode007:云商/云+(数字人民币)
    "operatorStatusCode": 0,  # 处理状态 处理状态编码（0未处理，1已处理）
    "orderNo": "",  # 订单编号 -（运营后台查询筛选条件）
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_finance_fee_queryFinWalletFee(data=data, headers=headers):
    """
    手续费明细表查询(运营后台)
    /appStore/finance/fee/queryFinWalletFee

    参数说明:
    - batchNo: 处理批次号
    - cardNo: 顾客卡号
    - companyCode: 分公司编码
    - extChannelCode: 外部接口通道
    - feeMonth: 月份
    - feeType: 手续费类型，101：微信；102：支付宝；103：银联；107：银联无感付；108：银联自动扣款； 201：工商银行；202：建设银行；203：邮政存蓄银行；204：交通银行；205：平安代扣 206：工行分期付；207：工商银行（新）；
    - leaderCardNo: 负责人卡号
    - memberType: 会员类型 会员类别：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）；5->店员；6->子账号
    - operateTypePageCode: 手续费页签操作编码 operateTypeCode001:普通顾客 operateTypeCode002:优惠顾客 operateTypeCode003:云商/云+  operateTypeCode004:云商/云+(工行分期付) operateTypeCode005:云商/云+(银联定期付) operateTypeCode006:云商/云+(银联签约付) operateTypeCode007:云商/云+(数字人民币)
    - operatorStatusCode: 处理状态 处理状态编码（0未处理，1已处理）
    - orderNo: 订单编号 -（运营后台查询筛选条件）
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/appStore/finance/fee/queryFinWalletFee"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
