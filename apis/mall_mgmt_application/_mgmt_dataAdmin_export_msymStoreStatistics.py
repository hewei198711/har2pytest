import os

from util.client import client

data = {
    "adminType": 0,  # 管理员身份类型：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    "endCreateTime": "",  # 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "endOrderMonth": "",  # 结束业绩月份yyyyMM 202104
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "serialNo": "",  # 产品编码
    "set": 0,  # 顺序:0倒序;1正序
    "sortType": 0,  # 排序类型:0-下单订单数,1-支付订单数,2-退货订单数,3-取消订单数,4-下单订单金额,5-支付订单金额,6-退货订单金额
    "startCreateTime": "",  # 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    "startOrderMonth": "",  # 开始业绩月份yyyyMM 202104
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_msymStoreStatistics(data=data, headers=headers):
    """
    码上有名交付门店统计明细文件导出
    /mgmt/dataAdmin/export/msymStoreStatistics

    参数说明:
    - adminType: 管理员身份类型：1->普通顾客；2->优惠顾客；3->云商；4->微店（云+）
    - endCreateTime: 结束订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - endOrderMonth: 结束业绩月份yyyyMM 202104
    - serialNo: 产品编码
    - set: 顺序:0倒序;1正序
    - sortType: 排序类型:0-下单订单数,1-支付订单数,2-退货订单数,3-取消订单数,4-下单订单金额,5-支付订单金额,6-退货订单金额
    - startCreateTime: 开始订单时间,不传默认当月份,有传时精确到天,yyyy-MM-dd
    - startOrderMonth: 开始业绩月份yyyyMM 202104
    """

    url = "/mgmt/dataAdmin/export/msymStoreStatistics"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
