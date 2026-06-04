import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "dataMonth": "",  # 销售呈报月份
    "dataMonthEnd": "",  # 达标月份止-用于导入列表查询
    "dataMonthStart": "",  # 达标月份起-用于导入列表查询
    "endTime": "",  # 活动结束时间, 格式为 yyyy-MM-dd HH:mm:ss
    "mobile": "",  # 会员电话
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "promotionName": "",  # 活动名称
    "promotionType": 0,  # 活动类型:1-抢购, 2-换购, 不传-查询所有
    "realname": "",  # 会员姓名
    "startTime": "",  # 活动开始时间, 格式为 yyyy-MM-dd HH:mm:ss
    "storeCode": "",  # 服务中心编号 注意：活动清单页面无此查询条件
    "validity": 0,  # 资格有效期:1-有效, 2-无效, 不传-查询所有  注意：导入数据页面无此查询条件
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_monthly_pagePromotion(params=params, headers=headers):
    """
    分页查询活动月结数据
    /mgmt/prmt/monthly/pagePromotion

    参数说明:
    - cardNo: 会员卡号
    - dataMonth: 销售呈报月份
    - dataMonthEnd: 达标月份止-用于导入列表查询
    - dataMonthStart: 达标月份起-用于导入列表查询
    - endTime: 活动结束时间, 格式为 yyyy-MM-dd HH:mm:ss
    - mobile: 会员电话
    - promotionName: 活动名称
    - promotionType: 活动类型:1-抢购, 2-换购, 不传-查询所有
    - realname: 会员姓名
    - startTime: 活动开始时间, 格式为 yyyy-MM-dd HH:mm:ss
    - storeCode: 服务中心编号 注意：活动清单页面无此查询条件
    - validity: 资格有效期:1-有效, 2-无效, 不传-查询所有  注意：导入数据页面无此查询条件
    """

    url = "/mgmt/prmt/monthly/pagePromotion"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
