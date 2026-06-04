import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "isMark": 0,  # 是否有标识（默认为2）, 0/无标识，1/有标识, 2/全部
    "leaderNo": "",  # 负责人卡号
    "level": "",  # 服务中心等级 1普通服务中心 2五星服务中心 3五星旗舰服务中心 4无实体店，多个用逗号分隔
    "levelIsCancel": 0,  # 等级是否取消, 0/未取消，1/取消
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "provinceCode": "",  # 省份编码
    "shopType": 0,  # 网点类型
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreLevelResultList(params=params, headers=headers):
    """
    查询网点等级标志列表
    /mgmt/store/getStoreLevelResultList

    参数说明:
    - companyCode: 分公司编号
    - isMark: 是否有标识（默认为2）, 0/无标识，1/有标识, 2/全部
    - leaderNo: 负责人卡号
    - level: 服务中心等级 1普通服务中心 2五星服务中心 3五星旗舰服务中心 4无实体店，多个用逗号分隔
    - levelIsCancel: 等级是否取消, 0/未取消，1/取消
    - pageNum: 页码
    - pageSize: 每页页数
    - provinceCode: 省份编码
    - shopType: 网点类型
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/getStoreLevelResultList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
