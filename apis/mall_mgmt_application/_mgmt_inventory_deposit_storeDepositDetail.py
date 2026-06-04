import os

from util.client import client

data = {
    "dealType": [],  # 交易类型 1->汇押货款、2->退押货款、3->其他、4->押货使用, 5->押货退货, 6->交付月结差额转入 ,9->押货保证金转移 10->其他扣款(运费和拼箱费) 11->商城订单(购物款汇总), 12->商城隔月订单(购物款取消支付汇总) , 13->商城订单(产品交付调减保证金汇总) 14->商城隔月订单(产品交付取消保证金调减汇总), 15 ->押货使用(签约购) , 16->签约专用款冻结, 17->签约专用款解冻, 20->信誉额, 21->产品调价,22->押货调整, 23->签约专用款(差额) 24->扣减押货款(转销售)
    "endDay": "",  # 交易日期yyyy-MM-dd
    "endMonth": 0,  # 交易结束月份yyyyMM
    "isShowSecond": False,  # 是否显示二级流水  true ： 是  false ： 否
    "moneyType": [],  # 款项类型  1->汇押货款、3->其他、7->手工增加押货款、8->手工退押货款、9->押货保证金转移 24->转销售
    "mortgageOrderNoOrBusinessNo": "",  # 押货单号or流水号
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "reportType": [],  # 报表字段   1 ->本期汇/退款  2->本期押货/退押   3-> 交付差额转入  4 ->其他扣款(运费和拼箱费) 5->本期购物款汇总 6->本期产品交付调减保证金汇总 7->信誉额
    "startDay": "",  # 交易日期yyyy-MM-dd
    "startMonth": 0,  # 交易开始月份yyyyMM
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_deposit_storeDepositDetail(data=data, headers=headers):
    """
    85折账款管理 -- 服务中心押货保证详情
    /mgmt/inventory/deposit/storeDepositDetail

    参数说明:
    - dealType: 交易类型 1->汇押货款、2->退押货款、3->其他、4->押货使用, 5->押货退货, 6->交付月结差额转入 ,9->押货保证金转移 10->其他扣款(运费和拼箱费) 11->商城订单(购物款汇总), 12->商城隔月订单(购物款取消支付汇总) , 13->商城订单(产品交付调减保证金汇总) 14->商城隔月订单(产品交付取消保证金调减汇总), 15 ->押货使用(签约购) , 16->签约专用款冻结, 17->签约专用款解冻, 20->信誉额, 21->产品调价,22->押货调整, 23->签约专用款(差额) 24->扣减押货款(转销售)
    - endDay: 交易日期yyyy-MM-dd
    - endMonth: 交易结束月份yyyyMM
    - isShowSecond: 是否显示二级流水  true ： 是  false ： 否
    - moneyType: 款项类型  1->汇押货款、3->其他、7->手工增加押货款、8->手工退押货款、9->押货保证金转移 24->转销售
    - mortgageOrderNoOrBusinessNo: 押货单号or流水号
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - reportType: 报表字段   1 ->本期汇/退款  2->本期押货/退押   3-> 交付差额转入  4 ->其他扣款(运费和拼箱费) 5->本期购物款汇总 6->本期产品交付调减保证金汇总 7->信誉额
    - startDay: 交易日期yyyy-MM-dd
    - startMonth: 交易开始月份yyyyMM
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/deposit/storeDepositDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
