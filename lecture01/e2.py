"""
E01 - Task 2: 페인팅 붓 크기 조절 기능

요구사항 요약:
- 초기 붓 크기: 5
- '+' 입력: +1, '-' 입력: -1, 범위 1~15
- 좌클릭: 파란색, 우클릭: 빨간색
- 드래그로 연속 그리기
- 'q' 입력 시 종료
- cv.setMouseCallback(), cv.circle(), cv.waitKey(1) 사용
"""

import sys
from pathlib import Path
from typing import Tuple

import cv2 as cv
import numpy as np


class Painter:
    """마우스 페인팅 상태(캔버스, 붓 크기)와 그리기 동작을 관리한다."""

    def __init__(self, canvas_bgr: np.ndarray) -> None:
        """캔버스와 초기 붓 크기를 설정한다."""
        self.canvas = canvas_bgr
        self.brush_size = 5

    def _clamp_brush(self) -> None:
        """붓 크기를 요구 범위(1~15)로 제한한다."""
        self.brush_size = max(1, min(15, self.brush_size))

    def _draw(self, x: int, y: int, color_bgr: Tuple[int, int, int]) -> None:
        """지정 위치에 채워진 원을 그려 붓질을 표현한다."""
        cv.circle(self.canvas, (x, y), self.brush_size, color_bgr, thickness=-1)

    def on_mouse(self, event: int, x: int, y: int, flags: int, param) -> None:
        """
        마우스 콜백:
        - LButtonDown/RButtonDown: 즉시 1회 그리기
        - MouseMove + Button flag: 드래그 연속 그리기
        """
        if event == cv.EVENT_LBUTTONDOWN:
            self._draw(x, y, (255, 0, 0))  # Blue in BGR
            return

        if event == cv.EVENT_RBUTTONDOWN:
            self._draw(x, y, (0, 0, 255))  # Red in BGR
            return

        if event == cv.EVENT_MOUSEMOVE:
            if flags & cv.EVENT_FLAG_LBUTTON:
                self._draw(x, y, (255, 0, 0))
            elif flags & cv.EVENT_FLAG_RBUTTON:
                self._draw(x, y, (0, 0, 255))


def main() -> None:
    """이미지를 캔버스로 사용해 페인팅을 수행하는 메인 루프."""
    if len(sys.argv) != 2:
        print("Usage: python e01_task2_paint_brush.py <image_path>")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    if not image_path.is_file():
        print(f"Error: file not found: {image_path}")
        sys.exit(1)

    img = cv.imread(str(image_path))
    if img is None:
        print(f"Error: cv.imread() failed: {image_path}")
        sys.exit(1)

    # 마우스 이벤트는 비동기로 들어오므로 콜백 함수를 등록한다.
    win_name = "Painter"
    painter = Painter(img)

    cv.namedWindow(win_name)
    cv.setMouseCallback(win_name, painter.on_mouse)

    while True:
        cv.imshow(win_name, painter.canvas)

        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        # '+' 입력이 '='로 들어오는 키보드 레이아웃을 함께 처리한다.
        if key in (ord("+"), ord("=")):
            painter.brush_size += 1
            painter._clamp_brush()
            print(f"Brush size: {painter.brush_size}")

        # '-' 입력이 '_'로 들어오는 경우를 함께 처리한다.
        if key in (ord("-"), ord("_")):
            painter.brush_size -= 1
            painter._clamp_brush()
            print(f"Brush size: {painter.brush_size}")

    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
