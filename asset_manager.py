import os
import sys
from typing import Optional

class AssetManager:
    def resource_path(self, relative_path: str) -> str:
        # 判断是否为打包后的可执行环境
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def check_file(self, filename: str) -> Optional[str]:
        path = self.resource_path(filename)
        if os.path.exists(path):
            return path
        print(f"提示: 资源文件 '{filename}' 未找到。")
        return None