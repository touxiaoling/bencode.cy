from setuptools import setup, Extension
from Cython.Build import cythonize
import platform

if platform.system() == "Windows":  # Windows（MSVC）
    extra_compile_args = [
        "/O2",  # 最高优化级别
        "/Ot",  # 优先速度优化
        "/arch:AVX2",  # 启用AVX2指令集（根据CPU支持调整）
    ]
    extra_link_args = []
else:
    extra_compile_args = [
        "-O3",  # 激进优化
        #        "-march=native",  # 针对本地CPU优化
        "-ffast-math",  # 快速数学运算
        "-funroll-loops",  # 循环展开
    ]
    extra_link_args = []  # 链接器通常无需额外参数，特殊场景可加（如-lm链接数学库）


ext_modules = [
    Extension(
        name="bencode._bencodec",  # 生成的模块名
        sources=["bencode/_bencode.py"],  # 你的Cython源码文件
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )
]

setup(
    name="bencode.cy",
    packages=["bencode"],
    # ext_modules =cythonize("bencode.py")
    ext_modules=cythonize(ext_modules, annotate=True, language_level="3"),  # annotate生成优化分析报告
)
