import os

from util.client import client

params = {
    "cancelType": 0,  # 取消类型: 1、结点取消，2、转让取消，3、违规取消，4、不达标取消，5、冻结取消，6、转云取消
    "companyCode": "",  # 分公司编码
    "isCancel": 0,  # 是否取消: 1、是，0、否
    "leaderNo": "",  # 负责人卡号
    "level": "",  # 网点等级 1服务中心 2五星服务中心 3五星旗舰服务中心 4无实体店，多个用逗号分隔
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "provinceCode": "",  # 省份编码
    "shopType": 0,  # 网点类型
    "storeCode": "",  # 服务中心编号
    "year": 0,  # 年份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreLevelList(params=params, headers=headers):
    """
    查询网点等级列表
    /mgmt/store/getStoreLevelList

    参数说明:
    - cancelType: 取消类型: 1、结点取消，2、转让取消，3、违规取消，4、不达标取消，5、冻结取消，6、转云取消
    - companyCode: 分公司编码
    - isCancel: 是否取消: 1、是，0、否
    - leaderNo: 负责人卡号
    - level: 网点等级 1服务中心 2五星服务中心 3五星旗舰服务中心 4无实体店，多个用逗号分隔
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - provinceCode: 省份编码
    - shopType: 网点类型
    - storeCode: 服务中心编号
    - year: 年份
    """

    url = "/mgmt/store/getStoreLevelList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
