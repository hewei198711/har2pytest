# coding:utf-8
import os
import re
import json
import urllib.request
from typing import Dict, Any, Optional

from .config import APIConfig
from .utils import extract_url_from_file
from .logger import logger


class SwaggerDocUpdater:
    """Swagger文档更新器类"""

    def __init__(self):
        """
        初始化Swagger文档更新器
        """
        self.swagger_cache = {}

    @staticmethod
    def determine_service_package(url: str) -> str:
        """
        根据URL的第一个字段判断属于哪个微服务包
        """
        return APIConfig.determine_service_package(url)

    def get_swagger_doc(self, service_base_url: str) -> Optional[Dict[str, Any]]:
        """
        获取Swagger API文档数据
        """
        if service_base_url in self.swagger_cache:
            return self.swagger_cache[service_base_url]

        doc_paths = [
            '/v3/api-docs',
            '/v2/api-docs',
            '/api-docs',
        ]

        for doc_path in doc_paths:
            try:
                logger.info(f"正在获取Swagger文档: {service_base_url}{doc_path}")

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json, text/plain, */*',
                }

                req = urllib.request.Request(f"{service_base_url}{doc_path}", headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    content = response.read().decode('utf-8')
                    data = json.loads(content)

                    if 'paths' in data:
                        self.swagger_cache[service_base_url] = data
                        logger.info(f"✓ 成功获取 {len(data['paths'])} 个API路径 (使用 {doc_path})")
                        return data
                    else:
                        logger.warning(f"❌ 文档格式不正确，缺少paths字段")
                        continue

            except Exception as e:
                logger.error(f"❌ 获取Swagger文档失败 {service_base_url}{doc_path}: {str(e)}")
                continue

        logger.error(f"❌ 尝试所有路径后仍然无法获取文档: {service_base_url}")
        return None

    def find_api_info_in_swagger(self, swagger_data: Dict[str, Any], api_path: str, method: str = 'GET') -> Dict[str, Any]:
        """
        在Swagger文档中查找特定API的信息
        """
        api_info = {
            'description': '',
            'parameters': {},
            'summary': ''
        }

        if not swagger_data or 'paths' not in swagger_data:
            return api_info

        paths = swagger_data['paths']

        path_data = None
        matched_path = None

        if api_path in paths:
            path_data = paths[api_path]
            matched_path = api_path
        elif api_path.startswith('/appStore'):
            stripped_path = api_path[9:]
            if stripped_path in paths:
                path_data = paths[stripped_path]
                matched_path = stripped_path
                logger.debug(f"去掉appStore前缀匹配: {stripped_path}")
        else:
            for path_key in paths.keys():
                if (api_path in path_key or path_key in api_path or
                    api_path in path_key or path_key in api_path):
                    path_data = paths[path_key]
                    matched_path = path_key
                    logger.debug(f"模糊匹配: {matched_path}")
                    break

        if not path_data:
            logger.info(f"未找到路径: {api_path}")
            return api_info

        if matched_path != api_path:
            logger.debug(f"找到匹配路径: {matched_path}")

        method_lower = method.lower()

        for http_method in [method_lower, 'get', 'post', 'put', 'delete']:
            if http_method in path_data:
                method_data = path_data[http_method]

                api_info['summary'] = method_data.get('summary', '')
                api_info['description'] = method_data.get('description', '') or method_data.get('summary', '')

                parameters = method_data.get('parameters', [])
                for param in parameters:
                    param_name = param.get('name', '')
                    param_desc = param.get('description', '')
                    if param_name:
                        api_info['parameters'][param_name] = param_desc

                    if 'schema' in param and '$ref' in param['schema']:
                        ref = param['schema']['$ref']
                        ref_name = ref.split('/')[-1]
                        if 'definitions' in swagger_data and ref_name in swagger_data['definitions']:
                            definition = swagger_data['definitions'][ref_name]
                            if 'properties' in definition:
                                for prop_name, prop_info in definition['properties'].items():
                                    prop_desc = prop_info.get('description', '')
                                    if prop_desc:
                                        api_info['parameters'][prop_name] = prop_desc

                if api_info['summary'] or api_info['description'] or api_info['parameters']:
                    break

        if not api_info['description'] and not api_info['summary']:
            api_info['description'] = path_data.get('description', '')
            if not api_info['description']:
                tags = path_data.get('get', {}).get('tags', []) or path_data.get('post', {}).get('tags', [])
                if tags:
                    api_info['description'] = f"标签: {', '.join(tags)}"

        return api_info

    def update_api_file(self, filepath: str, api_info: Dict[str, Any]) -> bool:
        """
        更新API文件，填充TODO信息
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            updated_content = content

            description = api_info['summary'] or api_info['description']
            if description:
                desc_pattern = r'TODO:\s*添加接口描述'
                if re.search(desc_pattern, updated_content):
                    updated_content = re.sub(desc_pattern, description, updated_content)
                    logger.info(f"✓ 更新接口描述: {description[:50]}...")

            if api_info['parameters']:
                param_patterns = [
                    r'"([^"]+)":\s*[^,]+,?\s*#\s*TODO:\s*添加参数说明',
                    r'\'([^\']+)\':\s*[^,]+,?\s*#\s*TODO:\s*添加参数说明',
                    r'(\w+):\s*[^,]+,?\s*#\s*TODO:\s*添加参数说明'
                ]

                matches = []
                for pattern in param_patterns:
                    matches.extend(re.finditer(pattern, updated_content))

                for match in matches:
                    param_name = match.group(1)

                    matched_desc = None
                    for swagger_param, desc in api_info['parameters'].items():
                        if swagger_param.lower() == param_name.lower():
                            matched_desc = desc
                            break

                    if matched_desc:
                        old_line = match.group(0)
                        new_line = old_line.replace(f'# TODO: 添加参数说明', f'# {matched_desc}')
                        updated_content = updated_content.replace(old_line, new_line)
                        logger.info(f"✓ 更新参数 {param_name}: {matched_desc[:30]}...")

            if updated_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                return True

        except Exception as e:
            logger.error(f"❌ 更新文件 {filepath} 失败: {str(e)}")

        return False

    def scan_and_update_apis(self, api_dir: str = "api"):
        """
        扫描并更新API目录中的所有文件
        """
        updated_files = []
        failed_files = []
        skipped_files = []

        for root, dirs, files in os.walk(api_dir):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    filepath = os.path.join(root, file)

                    try:
                        _, api_path = extract_url_from_file(filepath)
                        if not api_path:
                            logger.info(f"- 跳过文件（无法提取URL）: {filepath}")
                            skipped_files.append(filepath)
                            continue

                        service_package = self.determine_service_package(api_path)

                        if service_package not in APIConfig.SWAGGER_DOC_URLS():
                            logger.info(f"- 跳过文件（无对应文档）: {filepath} -> {service_package}")
                            skipped_files.append(filepath)
                            continue

                        doc_base_url = APIConfig.SWAGGER_DOC_URLS()[service_package]

                        swagger_data = self.get_swagger_doc(doc_base_url)
                        if not swagger_data:
                            logger.info(f"- 跳过文件（无法获取文档）: {filepath}")
                            failed_files.append(filepath)
                            continue

                        api_info = self.find_api_info_in_swagger(swagger_data, api_path)

                        if self.update_api_file(filepath, api_info):
                            updated_files.append(filepath)
                            logger.info(f"✓ 更新成功: {filepath}")
                        else:
                            logger.info(f"- 无需更新: {filepath}")

                    except Exception as e:
                        logger.error(f"❌ 处理文件失败 {filepath}: {str(e)}")
                        failed_files.append(filepath)

        logger.info(f"\n{'='*60}")
        logger.info(f"处理完成:")
        logger.info(f"✓ 成功更新: {len(updated_files)} 个文件")
        logger.info(f"- 无需更新: {len(skipped_files)} 个文件")
        logger.info(f"❌ 失败文件: {len(failed_files)} 个文件")

        if updated_files:
            logger.info(f"\n成功更新的文件:")
            for file in updated_files:
                logger.info(f"  - {file}")

        if failed_files:
            logger.error(f"\n失败的文件:")
            for file in failed_files:
                logger.error(f"  - {file}")
