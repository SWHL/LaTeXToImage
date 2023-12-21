# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from typing import Optional

import cv2
import numpy as np

from .crop_img import CropByProject
from .render_latex import RenderLaTeX


class LaTeXToImg:
    def __init__(
        self,
    ):
        self.cropper = CropByProject()
        self.latex = RenderLaTeX()

    def __call__(self, math: Optional[str] = None) -> np.ndarray:
        if len(math.strip()) <= 0 or math is None:
            raise ValueError("The input of formula must have value.")

        img = self.latex(math)
        img = self.cropper(img)
        return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("math", type=str, default=None)
    parser.add_argument("save_path", type=str, default="res.png")
    args = parser.parse_args()

    render = LaTeXToImg()
    img = render(args.math)
    if img is not None:
        cv2.imwrite(args.save_path, img)
        print(f"The image has been saved in {args.save_path} .")
    else:
        print("The result of render formula is empty.")


if __name__ == "__main__":
    main()
