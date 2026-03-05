"""
E01 - Task 3: ROI(관심영역) 선택 및 추출/저장

요구사항 요약:
- 이미지 표시 후 마우스로 클릭/드래그하여 사각형 ROI 선택
- 드래그 중 사각형을 화면에 시각화
- 버튼을 놓으면 ROI를 추출하여 별도 창에 출력
- 'r': 선택 리셋, 's': ROI 저장, 'q': 종료
"""

import sys
from pathlib import Path
from typing import Optional, Tuple

import cv2 as cv
import numpy as np


def load_image_or_exit(image_path: Path) -> np.ndarray:
    """경로에서 이미지를 로드하고 실패 시 즉시 종료한다."""
    if not image_path.is_file():
        print(f"Error: file not found: {image_path}")
        sys.exit(1)

    img = cv.imread(str(image_path))
    if img is None:
        print(f"Error: cv.imread() failed: {image_path}")
        sys.exit(1)

    return img


class RoiSelector:
    """마우스 드래그 기반 ROI 선택 상태를 관리하고 ROI를 추출한다."""

    def __init__(self, image_bgr: np.ndarray) -> None:
        """원본 이미지와 표시용 버퍼, ROI 선택 상태를 초기화한다."""
        self.image = image_bgr
        self.display = image_bgr.copy()

        self.selecting = False
        self.start_xy: Optional[Tuple[int, int]] = None
        self.end_xy: Optional[Tuple[int, int]] = None

        self.roi: Optional[np.ndarray] = None
        self.roi_window_open = False

    def reset(self) -> None:
        """ROI 선택 상태 및 표시 버퍼를 초기화하고 ROI 창을 닫는다."""
        self.display = self.image.copy()
        self.selecting = False
        self.start_xy = None
        self.end_xy = None
        self.roi = None

        if self.roi_window_open:
            cv.destroyWindow("ROI")
            self.roi_window_open = False

    def _update_display_rectangle(self) -> None:
        """드래그 중 사각형 표시를 위해 원본을 복사 후 rectangle을 그린다."""
        self.display = self.image.copy()
        if self.start_xy is None or self.end_xy is None:
            return

        x0, y0 = self.start_xy
        x1, y1 = self.end_xy
        cv.rectangle(self.display, (x0, y0), (x1, y1), (0, 255, 0), 2)

    def _finalize_roi(self) -> None:
        """
        드래그 방향과 무관하게 좌표를 (min,max)로 정규화하고,
        numpy 슬라이싱으로 ROI를 추출하여 별도 창에 출력한다.
        """
        if self.start_xy is None or self.end_xy is None:
            self.roi = None
            return

        x0, y0 = self.start_xy
        x1, y1 = self.end_xy

        x_min, x_max = sorted([x0, x1])
        y_min, y_max = sorted([y0, y1])

        if x_max <= x_min or y_max <= y_min:
            self.roi = None
            return

        self.roi = self.image[y_min:y_max, x_min:x_max].copy()

        cv.imshow("ROI", self.roi)
        self.roi_window_open = True

    def save_roi(self, out_path: Path) -> None:
        """현재 ROI를 파일로 저장하며, 저장 실패 시 즉시 종료한다."""
        if self.roi is None:
            print("ROI is not selected. Nothing to save.")
            return

        ok = cv.imwrite(str(out_path), self.roi)
        if not ok:
            print(f"Error: cv.imwrite() failed: {out_path}")
            sys.exit(1)

        print(f"Saved ROI: {out_path}")

    def on_mouse(
        self,
        event: int,
        x: int,
        y: int,
        flags: int,
        param,
    ) -> None:
        """
        마우스 콜백:
        - LButtonDown: 시작점 설정, 드래그 시작
        - MouseMove: 드래그 중이면 끝점 갱신 및 사각형 표시
        - LButtonUp: 드래그 종료, ROI 확정 및 추출
        """
        if event == cv.EVENT_LBUTTONDOWN:
            self.selecting = True
            self.start_xy = (x, y)
            self.end_xy = (x, y)
            self._update_display_rectangle()
            return

        if event == cv.EVENT_MOUSEMOVE and self.selecting:
            self.end_xy = (x, y)
            self._update_display_rectangle()
            return

        if event == cv.EVENT_LBUTTONUP and self.selecting:
            self.selecting = False
            self.end_xy = (x, y)
            self._update_display_rectangle()
            self._finalize_roi()


def main() -> None:
    """윈도우/콜백을 구성하고 키 입력(r/s/q)을 처리하는 메인 루프."""
    if len(sys.argv) != 2:
        print("Usage: python e01_task3_roi_select.py <image_path>")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    img = load_image_or_exit(image_path)

    win_name = "ROI Selector"
    selector = RoiSelector(img)

    cv.namedWindow(win_name)
    cv.setMouseCallback(win_name, selector.on_mouse)

    out_path = Path("roi_saved.png")

    while True:
        cv.imshow(win_name, selector.display)

        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        if key == ord("r"):
            selector.reset()

        if key == ord("s"):
            selector.save_roi(out_path)

    cv.destroyAllWindows()


if __name__ == "__main__":
    main()