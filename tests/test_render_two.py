# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import numpy as np
from PIL import Image, ImageChops

from latex_to_image.main import LaTeX2Img

render = LaTeX2Img()

formula1 = r"=e^{-\lambda}\sum_{k=0}^{\infty}\frac{\left(-2\lambda\right)^{k}}{k!}"
formula2 = r"= e ^ { - \lambda } \sum _ { k = 0 } ^ { \infty } \frac { \left( - 2 \lambda \right) ^ { k } } { k ! }"

img1, img2 = render(formula1, formula1)

img1_np = Image.fromarray(img1)
img2_np = Image.fromarray(img2)

diff = ImageChops.difference(img1_np, img2_np)

diff.show()

np.testing.assert_allclose(img1, img2, rtol=1e-3, atol=1e-5)
np.testing.assert_array_equal(img1, img2)

print("ok")
