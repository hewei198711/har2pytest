import os

from util.client import client

params = {
    "companyCode": "",  # 公司编码
    "configType": 0,  # 配置类型：1-企业电子发票, 2-数字人名币
    "enableStatus": False,  # 启动状态: 0-禁用, 1-启用
    "pageNum": 0,  # 页 默认1
    "pageSize": 0,  # 每页数量 默认10
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_pageCompanyEnableConfig(params=params, headers=headers):
    """
    分页查询列表 企业电子发票/数字人名币
    /mgmt/sys/pageCompanyEnableConfig

    参数说明:
    - companyCode: 公司编码
    - configType: 配置类型：1-企业电子发票, 2-数字人名币
    - enableStatus: 启动状态: 0-禁用, 1-启用
    - pageNum: 页 默认1
    - pageSize: 每页数量 默认10
    """

    url = "/mgmt/sys/pageCompanyEnableConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
