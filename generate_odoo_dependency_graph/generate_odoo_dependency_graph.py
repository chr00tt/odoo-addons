import os
import ast
from graphviz import Digraph
import sys

def get_module_dependencies(addons_path, module_name):
    """
    从 __manifest__.py 文件中解析模块的依赖关系
    """
    module_path = os.path.join(addons_path, module_name)
    if not os.path.exists(module_path):
        print(f"Module {module_name} not found")
        return []
    manifest_path = os.path.join(module_path, '__manifest__.py')
    if not os.path.exists(manifest_path):
        print(f"__manifest__.py not found in {module_name}")
        manifest_path = os.path.join(addons_path, module_name, '__openerp__.py')
        print(f"manifest_path: {manifest_path}")
    if not os.path.exists(manifest_path):
        return []

    try:
        with open(manifest_path, 'r', encoding='utf-8') as file:
            manifest_content = file.read()
        manifest_dict = ast.literal_eval(manifest_content)
        return manifest_dict.get('depends', [])
    except Exception as e:
        print(f"Error parsing {manifest_path}: {e}")
        return []

def get_includes(addons_path, module_name):
    if not module_name:
        return []

    includes = [module_name]

    # 获取 module_name 依赖的模块
    includes.extend(get_module_dependencies(addons_path, module_name))

    # 获取依赖 module_name 的模块
    for module in os.listdir(addons_path):
        dependencies = get_module_dependencies(addons_path, module)
        if module_name in dependencies:
            includes.append(module)

    print(f"includes: {includes}")

    return includes
    

def generate_dependency_graph(addons_path, module_name, output_file='dependency_graph.png'):
    """
    生成模块依赖图
    :param addons_path: Odoo 模块目录路径
    :param output_file: 输出文件名
    """
    dot = Digraph(comment='Odoo Module Dependency Graph')
    
    includes = get_includes(addons_path, module_name)
    excludes = [
        'google_',
        'l10n_',
        'test_',
    ]

    # 遍历模块目录
    for module in os.listdir(addons_path):
        if includes and module not in includes:
            continue
        if any([module.startswith(exclude) for exclude in excludes]):
            continue

        print(f"Processing module {module}")
        module_path = os.path.join(addons_path, module)
        if os.path.isdir(module_path):
            manifest_path = os.path.join(module_path, '__manifest__.py')
            if not os.path.exists(manifest_path):
                manifest_path = os.path.join(module_path, '__openerp__.py')
            if os.path.exists(manifest_path):
                # 添加模块节点
                dot.node(module, module)
                # 获取模块依赖
                dependencies = get_module_dependencies(addons_path, module)
                for dependency in dependencies:
                    # 添加依赖边
                    dot.edge(dependency, module)

    # 保存并生成图像
    dot.render(output_file, view=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} addons_path [module_name]")
        sys.exit(1)

    addons_path = sys.argv[1]
    module_name = sys.argv[2] if len(sys.argv) > 2 else None

    generate_dependency_graph(addons_path, module_name)
