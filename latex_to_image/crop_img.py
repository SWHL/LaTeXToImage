# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import cv2
import numpy as np


class CropByProject:
    """投影法裁剪"""

    def __init__(self, threshold=128):
        self.threshold = threshold

    def __call__(self, origin_img, margin=(0, 0, 0, 0)):
        # image = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)

        # 将图片二值化
        retval, img = cv2.threshold(
            origin_img, self.threshold, 255, cv2.THRESH_BINARY_INV
        )

        # 使文字增长成块
        closed = cv2.dilate(img, None, iterations=1)

        # 水平投影
        x0, x1 = self.get_project_loc(closed, direction="width")

        # 竖直投影
        y0, y1 = self.get_project_loc(closed, direction="height")

        h, w = img.shape[:2]
        x0 = max(x0 - margin[0], 0)
        y0 = max(y0 - margin[1], 0)
        x1 = min(x1 + margin[2], w)
        y1 = min(y1 + margin[3], h)

        return origin_img[y0:y1, x0:x1]

    @staticmethod
    def get_project_loc(img, direction):
        """获得裁剪的起始和终点索引位置
        Args:
            img (ndarray): 二值化后得到的图像
            direction (str): 'width/height'
        Raises:
            ValueError: 不支持的求和方向
        Returns:
            tuple: 起始索引位置
        """
        if direction == "width":
            axis = 0
        elif direction == "height":
            axis = 1
        else:
            raise ValueError(f"direction {direction} is not supported!")

        loc_sum = np.sum(img == 255, axis=axis)
        loc_range = np.argwhere(loc_sum > 0)
        i0, i1 = loc_range[0][0], loc_range[-1][0]
        return i0, i1


if __name__ == "__main__":
    croper = CropByProject()

    img_path = "/Users/joshuawang/projects/latex2img/res.png"
    img = cv2.imread(img_path)

    img = croper(img)
    h, w = img.shape[:2]

    img_half = img[: int(h / 2), :]
    img_half2 = img[int(h / 2) :, :]

    crop_im1 = croper(img_half)
    crop_im2 = croper(img_half2)
    cv2.imwrite("crop_im1.png", crop_im1)
    cv2.imwrite("crop_im2.png", crop_im2)
