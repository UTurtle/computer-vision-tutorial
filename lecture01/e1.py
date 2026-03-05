"""
E01 - Task 1: 이미지 불러오기 및 그레이스케일 변환

요구사항 요약:
- cv.imread()로 이미지 로드
- cv.cvtColor()로 grayscale 변환 (cv.COLOR_BGR2GRAY)
- np.hstack()로 원본 + grayscale 가로 연결
- cv.imshow(), cv.waitKey()로 출력 후 아무 키나 누르면 종료
"""

import sys
from pathlib import Path

import cv2 as cv
import numpy as np


def main() -> None:
    """입력 이미지를 로드해 grayscale과 나란히 출력하는 메인 루프."""
    if len(sys.argv) != 2:
        print("Usage: python e01_task1_image_gray.py <image_path>")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    if not image_path.is_file():
        print(f"Error: file not found: {image_path}")
        sys.exit(1)

    # OpenCV는 이미지를 기본적으로 BGR 채널 순서로 읽는다.
    img_bgr = cv.imread(str(image_path))
    if img_bgr is None:
        print(f"Error: cv.imread() failed: {image_path}")
        sys.exit(1)

    # BGR 이미지를 1채널 grayscale로 변환한다.
    img_gray = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY)

    # np.hstack()를 위해 grayscale(1채널)을 BGR(3채널)로 맞춘 뒤 가로 결합한다.
    img_gray_bgr = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)
    merged = np.hstack([img_bgr, img_gray_bgr])

    # 결과를 출력하고 아무 키 입력 시 창을 닫는다.
    cv.imshow("Original | Grayscale", merged)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
