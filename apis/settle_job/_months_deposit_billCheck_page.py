from util.client import client

data = {
    "pageNum": 1,  # 第几页
    "pageSize": 20,  # 每页显示页数
    "storeCode": "914008",  # 服务中心编号
    "startMonth": "202604",  # 开始月份yyyyMM
    "endMonth": "202604",  # 结束月份yyyyMM
}

headers = {
    "channel": "pc",
    "client": "store",
    "content-type": "application/json;charset=UTF-8",
    "authorization": "请输入认证令牌",
}


def _months_deposit_billCheck_page(data=data, headers=headers):
    """
    85折押货保证金对账单分页列表
    /months/deposit/billCheck/page

    参数说明:
    - dto: dto
    - billType: 1->实时对账单，2->月结对账单
    - companyCode: 分公司code
    - discountLevel: 折扣系数等级  1-65%,2-70%,3-75%,4-85%
    - endMonth: 结束月份yyyyMM
    - filterShopType: 是否过滤网点类型：0否 1是
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - moneyType: 可用结余为负  0->是  1 ->否
    - notShopTypes: 网点类型
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - startMonth: 开始月份yyyyMM
    - storeCode: 服务中心编号
    """

    url = "/months/deposit/billCheck/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
