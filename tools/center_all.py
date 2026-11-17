import argparse
import sys
import time
from pathlib import Path

# 상위 폴더(resilience-quad)의 hw 모듈을 불러오기 위한 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from hw.servo import HiwonderServoController


def main():
    parser = argparse.ArgumentParser(description="12개 서보 모터 영점(중앙 500) 정렬 스크립트")
    parser.add_argument("--port", default="COM3", help="시리얼 포트 (Windows: COM3, Jetson: /dev/ttyUSB0)")
    parser.add_argument("--sim", action="store_true", help="실물 보드 없이 시뮬레이션 모드로 실행")
    parser.add_argument("--count", type=int, default=12, help="서보 총 개수 (기본 12개)")
    args = parser.parse_args()

    ctrl = HiwonderServoController(port=args.port, sim=args.sim)
    print(f"=== 영점 정렬 시작 (모드: {'시뮬레이션' if args.sim else args.port}) ===")

    try:
        for servo_id in range(1, args.count + 1):
            ctrl.move_servo(servo_id=servo_id, position=500, duration_ms=600)
            time.sleep(0.05)
        print("=== 모든 서보 영점(500) 명령 전송 완료 ===")
    finally:
        ctrl.close()


if __name__ == "__main__":
    main()