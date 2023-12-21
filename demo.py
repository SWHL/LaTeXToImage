# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import cv2

from latex_to_image import LaTeXToImg

render = LaTeXToImg()

formula = "x^2 + y ^2 = 1"

img = render(formula)
cv2.imwrite("res.png", img)
print("ok")
