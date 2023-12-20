# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from PIL import Image

from latex_to_image import LaTeXToImg

render = LaTeXToImg()

formula = "x^2 + y ^2 = 1"

img_formula = render(formula)
img_formula = Image.fromarray(img_formula)
img_formula.save("res2.png")
print("ok")
