import argparse
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from hw.config import PULSE_MAX, PULSE_MIN
from hw.servo import HiwonderServoController


def main():
    parser = argparse.ArgumentParser(description="개별 서보 안전 가동범위 및 회전 방향 테스트")
    parser.add_argument("--id", type=int, required=True, help="테스트할 서보 ID (1~12)")
    parser.add_argument("--pos", type=int, required=True, help=f"목표 펄스 ({PULSE_MIN}~{PULSE_MAX}, 중앙=500)")
    parser.add_argument("--ms", type=int, default=500, help="이동 시간(ms)")
    parser.add_argument("--port", default="COM3", help="시리얼 포트")
    parser.add_argument("--sim", action="store_true", help="시뮬레이션 모드")
    args = parser.parse_args()

    safe_pos = max(PULSE_MIN, min(PULSE_MAX, args.pos))
    if safe_pos != args.pos:
        print(f"[경고] 안전 범위({PULSE_MIN}~{PULSE_MAX}) 초과로 {safe_pos}으로 자동 제한됩니다.")

    ctrl = HiwonderServoController(port=args.port, sim=args.sim)
    try:
        ctrl.move_servo(servo_id=args.id, position=safe_pos, duration_ms=args.ms)
        time.sleep(args.ms / 1000.0)
    finally:
        ctrl.close()


if __name__ == "__main__":
    main()