from logging import FileHandler
from logging import Formatter
from logging import INFO as INFO_LEVEL
from logging import getLogger
from pathlib import Path
from platform import system
from time import localtime
from time import strftime
from rich.console import Console
from utils.StringUtil import StringUtil

__all__ = [
    'BaseLogger',
    'LoggerManager',
]


# 彩色交互提示颜色设置，支持标准颜色名称、Hex、RGB 格式
MASTER = "b #fff200"
PROMPT = "b turquoise2"
GENERAL = "b bright_white"
PROGRESS = "b bright_magenta"
ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"


class ColorfulConsole(Console):
    def print(self, *args, style=GENERAL, highlight=False, **kwargs):
        super().print(*args, style=style, highlight=highlight, **kwargs)

    def input(self, prompt_="", *args, **kwargs):
        return super().input(
            f"[{PROMPT}]{prompt_}[/{PROMPT}]", *args, **kwargs)


class BaseLogger:
    """不记录日志，空白日志记录器"""

    def __init__(self, main_path: Path, root="", folder="", name=""):
        self.log = None  # 记录器主体
        self.console = ColorfulConsole()
        self._root, self._folder, self._name = self.init_check(
            main_path=main_path,
            root=root,
            folder=folder,
            name=name,
        )
        self.run()

    def init_check(
            self,
            main_path: Path,
            root=None,
            folder=None,
            name=None) -> tuple:
        root = self.check_root(root, main_path)
        folder = self.check_folder(folder)
        name = self.check_name(name)
        return root, folder, name

    def check_root(self, root: str, default: Path) -> Path:
        if not root:
            return default
        if (r := Path(root)).is_dir():
            return r
        self.console.print(f"日志储存路径 {root} 无效，程序将使用项目根路径作为储存路径")
        return default

    def check_name(self, name: str) -> str:
        if not name:
            return "%Y-%m-%d %H.%M.%S"
        try:
            _ = strftime(name, localtime())
            return name
        except ValueError:
            self.console.print(f"日志名称格式 {name} 无效，程序将使用默认时间格式：年-月-日 时.分.秒")
            return "%Y-%m-%d %H.%M.%S"

    @staticmethod
    def check_folder(folder: str) -> str:
        return StringUtil().filter_dir_name(folder, "Log")

    def run(self, *args, **kwargs):
        pass

    def info(self, text: str, output=True, **kwargs):
        if output:
            self.console.print(text, style=INFO, **kwargs)

    def warning(self, text: str, output=True, **kwargs):
        if output:
            self.console.print(text, style=WARNING, **kwargs)

    def error(self, text: str, output=True, **kwargs):
        if output:
            self.console.print(text, style=ERROR, **kwargs)


class LoggerManager(BaseLogger):
    """日志记录"""
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(self, main_path: Path, root="", folder="", name=""):
        super().__init__(main_path, root, folder, name)

    def run(
            self,
            format_="%(asctime)s[%(levelname)s]:  %(message)s", filename=None):
        if not (dir_ := self._root.joinpath(self._folder)).exists():
            dir_.mkdir()
        file_handler = FileHandler(
            dir_.joinpath(
                f"{filename}.log" if filename else f"{strftime(self._name, localtime())}.log"),
            encoding=self.encode)
        formatter = Formatter(format_, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        self.log = getLogger(__name__)
        self.log.addHandler(file_handler)
        self.log.setLevel(INFO_LEVEL)

    def info(self, text: str, output=True, **kwargs):
        if output:
            self.console.print(text, style=INFO, **kwargs)
        self.log.info(text.strip())

    def warning(self, text: str, output=True, **kwargs):
        if output:
            self.console.print(text, style=WARNING, **kwargs)
        self.log.warning(text.strip())

    def error(self, text: str, output=True, **kwargs):
        if output:
            self.console.print(text, style=ERROR, **kwargs)
        self.log.error(text.strip())


if __name__ == "__main__":
    logger = LoggerManager(
        main_path=Path(__file__).resolve().parent.parent,
        folder="logTest",
        name="%Y-%m-%d",
    )

    logger.warning("test111")
