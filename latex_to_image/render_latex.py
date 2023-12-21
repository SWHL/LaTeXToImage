# -*- encoding: utf-8 -*-
# mostly taken from http://code.google.com/p/latexmath2png/
# install preview.sty
import os
import re
import shlex
import subprocess
import tempfile
import traceback
from pathlib import Path
from typing import Union

import cv2


class RenderLaTeX:
    def __init__(self, dpi=200):
        self.dpi = dpi
        self.BASE = r"""\documentclass[12pt]{article}\usepackage{fontspec,unicode-math}\thispagestyle{empty}\setmathfont{Latin Modern Math}\begin{document}$%s$\end{document}"""

    def __call__(self, math: str):
        work_dir, tex_file = self.generate_tmp(math)
        try:
            pdf_file = self.render_by_xelatex(work_dir, tex_file)
            img = self.convert_pdf_to_png(pdf_file)
            return img
        except Exception as e:
            traceback.print_exc()
            return None
        finally:
            self.clear_files(tex_file)

    def generate_tmp(self, math):
        workdir = tempfile.gettempdir()
        fd, tex_file = tempfile.mkstemp(".tex", "eq", workdir, True)
        with os.fdopen(fd, "w+") as f:
            document = self.BASE % (math)
            f.write(document)
        return workdir, tex_file

    def render_by_xelatex(self, work_dir, in_file) -> Path:
        cmd = f"xelatex -interaction errorstopmode -file-line-error -output-directory {work_dir} {in_file}"
        sout, _ = self.run_cmd(cmd)

        pdf_file: Path = Path(in_file).with_suffix(".pdf")
        expression = pdf_file.parent / rf"{pdf_file.stem}.p\ndf \((\d+)? page"
        flag = self.is_success(
            text=sout,
            expression=str(expression),
        )
        if flag:
            return pdf_file
        raise LaTeXError("xelatex meets error.")

    def convert_pdf_to_png(self, pdf_file):
        png_file: Path = Path(pdf_file).with_suffix(".png")
        cmd = f"convert -background white -flatten -density {self.dpi} -colorspace gray {pdf_file} -quality 90 {png_file}"
        _, return_code = self.run_cmd(cmd)
        if return_code != 0:
            raise LaTeXError(f"PDF to png error\n{cmd}\n{pdf_file}")
        img = cv2.imread(str(png_file))
        return img

    @staticmethod
    def run_cmd(shell_cmd: str):
        with subprocess.Popen(
            shlex.split(shell_cmd),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        ) as p:
            sout, serr = p.communicate()
            return sout, p.returncode

    @staticmethod
    def is_success(text, expression=None):
        try:
            pattern = re.compile(expression)
            results = re.findall(pattern, text)
            if int(results[0]) != 1:
                return False
            return True
        except Exception:
            traceback.print_exc()
            return False

    @staticmethod
    def clear_files(in_file: Union[str, Path]) -> None:
        invalid_files = Path(in_file).parent.glob(f"{Path(in_file).stem}*")
        for file_path in invalid_files:
            file_path.unlink()


class LaTeXError(Exception):
    pass
