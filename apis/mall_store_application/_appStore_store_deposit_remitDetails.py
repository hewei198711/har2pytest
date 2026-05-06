from util.client import client

data = {
    "pageNum": 1,  # 第几页
    "pageSize": 20,  # 每页显示页数
    "storeCode": "914008",  # 店铺编号
}

headers = {
    "channel": "pc",
    "client": "store",
    "content-type": "application/json;charset=UTF-8",
    "authorization": "请输入认证令牌",
}


def _appStore_store_deposit_remitDetails(data=data, headers=headers):
    """
    获取服务中心押货保证金汇退明细
    /appStore/store/deposit/remitDetails

    参数说明:
    - dto: dto
    - companyCode: 分公司code
    - dealType: 交易类型 1、汇押货款 2、退押货款、3、其他、4、不影响押货保证金  5、押货保证金转移
    - handleType: 手工/自动类型  1、自动处理  2、手工处理
    - inputEndTime: 录入结束时间(格式yyyy-MM-dd)
    - inputStartTime: 录入开始时间(格式yyyy-MM-dd)
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - payAccountBankName: 付款银行
    - sourceType: 款项类型 1->汇押货款、3->其他、7->手工增加押货款、8->手工退押货款、9->押货保证金转移、14->无法识别款退款、15->无法识别款不处理、24->转销售
    - storeCode: 店铺编号
    - sysEndTime: 系统到账结束时间(格式yyyy-MM-dd)
    - sysStartTime: 系统到账开始时间(格式yyyy-MM-dd)
    - verifyEndTime: 审核结束时间(格式yyyy-MM-dd)
    - verifyStartTime: 审核开始时间(格式yyyy-MM-dd)
    """

    url = "/appStore/store/deposit/remitDetails"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
