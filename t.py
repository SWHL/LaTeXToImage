import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from pdf2image import convert_from_path


def latex(tex, output_file, dpi=300, bgcolor="#FFFFFF", fgcolor="#000000"):
    converter = LatexConverter(
        tex, output_file, dpi=dpi, bgcolor=bgcolor, fgcolor=fgcolor
    )
    converter.convert()


def latex_by_mpl(tex, output_file, dpi=300, bgcolor="white", fgcolor="black"):
    tex = "$ " + tex + " $"
    mpl.rcParams["text.usetex"] = True
    mpl.rcParams["text.latex.preamble"] = r"\usepackage{{amsmath}}"
    plt.rcParams.update({"mathtext.fontset": "cm"})
    fig = plt.figure(figsize=(10, 10), dpi=100)

    t = fig.text(
        0, 0, tex, horizontalalignment="left", verticalalignment="bottom", fontsize=30
    )

    r = fig.canvas.get_renderer()

    bbox = t.get_tightbbox(r)
    w, h = (bbox.width / r.dpi, bbox.height / r.dpi)

    fig = plt.figure(figsize=(1.1 * w, 1.1 * h), dpi=dpi)
    t = fig.text(
        0,
        0,
        tex,
        fontsize=30,
        verticalalignment="bottom",
        horizontalalignment="left",
        bbox={"facecolor": bgcolor, "edgecolor": bgcolor},
        color=fgcolor,
    )

    fig.savefig(output_file, transparent=False)


class LatexExpection(Exception):
    pass


class CropException(Exception):
    pass


class ConversionException(Exception):
    pass


class LatexConverter:
    def __init__(self, tex, output_file, bgcolor, fgcolor, dpi):
        self.cwd = Path.cwd()
        self.output = output_file
        self.dpi = dpi
        self.bgcolor = self._translate_color(bgcolor)
        self.fgcolor = self._translate_color(fgcolor)
        self.file_base, self.file_extension = os.path.splitext(output_file)
        self.tex = tex

    def convert(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            os.chdir(tmp_dir)
            self.write_latex_file()
            self.tex_to_pdf()
            self.pdf_to_image()

    def write_latex_file(self):
        with open(self.file_base + ".tex", "w") as f:
            f.write("\\documentclass{article}")
            f.write("\\thispagestyle{empty}")
            f.write("\\usepackage{amsmath,amssymb,amsfonts,amsthm}")
            f.write("\\usepackage{xcolor}")
            f.write("\\definecolor{fgcolor}{RGB}{%s, %s, %s}" % self.fgcolor)
            f.write("\\definecolor{bgcolor}{RGB}{%s, %s, %s}" % self.bgcolor)
            f.write("\\begin{document}")
            f.write("\\color{fgcolor}")
            f.write("\\pagecolor{bgcolor}")
            f.write("\\begin{eqnarray*}")
            f.write(self.tex)
            f.write("\\end{eqnarray*}")
            f.write("\\end{document}")

    def tex_to_pdf(self):
        rc = subprocess.call(
            ["pdflatex", "-halt-on-error", self.file_base + ".tex"],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
        if rc != 0:
            raise LatexExpection("Invalid Latex Expression")

        rc = subprocess.call(
            ["pdfcrop", self.file_base + ".pdf"],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
        if rc != 0:
            raise CropException("Cannot crop pdf file")

        pdf = str(self.file_base) + ".pdf"
        shutil.move(self.file_base + "-crop.pdf", Path.cwd() / pdf)

    def pdf_to_image(self):
        pdf = str(self.file_base) + ".pdf"
        try:
            pages = convert_from_path(pdf, dpi=self.dpi)
            pages[0].save(
                self.file_base + self.file_extension, self.file_extension[1:].upper()
            )
            shutil.move(
                self.file_base + self.file_extension,
                self.cwd / (str(self.file_base) + self.file_extension),
            )
            shutil.move(pdf, self.cwd / (str(self.file_base) + ".pdf"))
        except:
            print(
                'Unable to convert image (is "poppler" installed?). Falling back on PDF instead.'
            )
            shutil.move(pdf, self.cwd / (str(self.file_base) + ".pdf"))

    def _translate_color(self, color):
        assert re.match("#[0-9A-Fa-f]{6}", color)
        red, green, blue = int(color[1:3], 16), int(color[3:5], 16), int(color[5:], 16)
        return red, green, blue


if __name__ == "__main__":
    converter = LatexConverter(
        r"\frac{\partial}{\partial z}",
        "test.png",
        dpi=100,
        bgcolor="#ffffff",
        fgcolor="#000000",
    )
    converter.convert()
