# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import numpy as np

from .crop_img import CropByProject
from .render_latex import RenderLaTeX


class LaTeXToImg:
    def __init__(
        self,
    ):
        self.cropper = CropByProject()
        self.latex = RenderLaTeX()

    def __call__(self, math: str) -> np.ndarray:
        img = self.latex(math)
        img = self.cropper(img)
        return img


