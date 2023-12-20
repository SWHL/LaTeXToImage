<div align="center">
  <div align="center">
    <h1><b> LaTeX To Image</b></h1>
  </div>
  <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
  <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Mac%2C%20Win-pink.svg"></a>
  <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <a href="https://github.com/RapidAI/TableStructureRec/blob/c41bbd23898cb27a957ed962b0ffee3c74dfeff1/LICENSE"><img alt="GitHub" src="https://img.shields.io/badge/license-Apache 2.0-blue"></a>

</div>

### 简介
该仓库是用于将LaTeX的公式借助LaTeX工具转换为对应的图像。


### 安装
1. 安装texlive
- Ubuntu
    ```bash
    # Ubuntu
    sudo apt-get install texlive-full

    # 确认是否安装成功
    $ pdflatex --help
    Usage: pdftex [OPTION]... [TEXNAME[.tex]] [COMMANDS]
    or: pdftex [OPTION]... \FIRST-LINE
    or: pdftex [OPTION]... &FMT ARGS
    Run pdfTeX on TEXNAME, usually creating TEXNAME.pdf.
    ```
- MacOS
推荐安装[MacTex](https://tug.org/mactex/mactex-download.html)


2. 安装运行环境


### 使用



### 参考代码
- [LaTeX-OCR](https://github.com/lukas-blecher/LaTeX-OCR/blob/main/pix2tex/dataset/latex2png.py)
- [latex2image](https://pypi.org/project/latex2image/#description)