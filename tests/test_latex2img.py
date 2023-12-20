# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

from PIL import Image

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from latex_to_image import GetRenderImg

render = GetRenderImg()


def test_normal():
    formula = "x^2 + y ^2 = 1"
    img_formula = render(formula)

    assert img_formula.shape == (34, 162)
