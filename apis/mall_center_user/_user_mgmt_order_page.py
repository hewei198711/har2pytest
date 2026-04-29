from util.client import client

data = {
    "orderNo": None,  # 兑换流水号
    "companyWord": None,  # 业务分公司编码/名称
    "orderStatusList": [],  # 订单状态 1->待支付 2->待发货 3->待收货(已发货) 4->已取消 5->已退货 6->待核销 99->已完成
    "customerPhone": None,  # 顾客手机号
    "customerCard": None,  # 顾客卡号
    "customerName": None,  # 顾客姓名
    "exchangeNoWord": None,  # 兑换品编码/名称
    "customerType": 1,  # 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店 5->云+子账号
    "customerSourceList": [],  # 顾客来源平台:0->商城mall；1->健康health；2->学堂edu；4->荟友趣
    "creatorCard": None,  # 开单人卡号
    "expressType": None,  # 配送方式 1->服务中心自提 2->公司配送
    "orderWay": None,  # 下单方式 1->自购订单 2->代购订单
    "exchangeTimeBegin": None,  # 兑换时间-开始
    "exchangeTimeEnd": None,  # 兑换时间-结束
    "commitTimeBegin": None,  # 提交时间-开始
    "commitTimeEnd": None,  # 提交时间-结束
    "payTimeBegin": None,  # 付款时间-开始
    "payTimeEnd": None,  # 付款时间-结束
    "cancelTimeBegin": None,  # 取消时间-开始
    "cancelTimeEnd": None,  # 取消时间-结束
    "hxTimeBegin": None,  # 核销时间-开始
    "hxTimeEnd": None,  # 核销时间-结束
    "pageNum": 1,  # TODO: 添加参数说明
    "pageSize": 10,  # TODO: 添加参数说明
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": "请输入认证令牌",
}


def _user_mgmt_order_page(data=data, headers=headers):
    """
    分页查询兑换订单列表
    /user/mgmt/order/page

    参数说明:
    - req: req
    - cancelTimeBegin: 取消时间-开始
    - cancelTimeEnd: 取消时间-结束
    - commitTimeBegin: 提交时间-开始
    - commitTimeEnd: 提交时间-结束
    - companyWord: 业务分公司编码/名称
    - creatorCard: 开单人卡号
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - customerSource: 顾客来源平台:0->商城mall；1->健康health；2->学堂edu；4->荟友趣
    - customerSourceList: 顾客来源平台:0->商城mall；1->健康health；2->学堂edu；4->荟友趣
    - customerType: 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店 5->云+子账号
    - exchangeNoWord: 兑换品编码/名称
    - exchangeTimeBegin: 兑换时间-开始
    - exchangeTimeEnd: 兑换时间-结束
    - expressType: 配送方式 1->服务中心自提 2->公司配送
    - financeCompanyWord: 财务分公司编码/名称
    - hxTimeBegin: 核销时间-开始
    - hxTimeEnd: 核销时间-结束
    - orderNo: 兑换流水号
    - orderStatus: 订单状态 1->待支付 2->待发货 3->待收货(已发货) 4->已取消 5->已退货 6->待核销 99->已完成
    - orderStatusList: 订单状态 1->待支付 2->待发货 3->待收货(已发货) 4->已取消 5->已退货 6->待核销 99->已完成
    - orderWay: 下单方式 1->自购订单 2->代购订单
    - payTimeBegin: 付款时间-开始
    - payTimeEnd: 付款时间-结束
    """

    url = "/user/mgmt/order/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
