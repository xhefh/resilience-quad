import argparse
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from hw.servo import HiwonderServoController


def main():
    parser = argparse.ArgumentParser(description="Hiwonder 서보 ID 부여 스크립트 (서보 1개만 연결 후 실행)")
    parser.add_argument("--id", type=int, required=True, help="새로 부여할 서보 ID (1~12)")
    parser.add_argument("--old-id", type=int, default=0xFE, help="기존 서보 ID (기본 254=전체 브로드캐스트)")
    parser.add_argument("--port", default="COM3", help="시리얼 포트")
    parser.add_argument("--sim", action="store_true", help="시뮬레이션 모드")
    args = parser.parse_args()

    if not (1 <= args.id <= 12):
        raise ValueError("서보 ID는 1~12 사이여야 합니다.")

    ctrl = HiwonderServoController(port=args.port, sim=args.sim)
    try:
        ctrl.set_servo_id(new_id=args.id, old_id=args.old_id)
        time.sleep(0.2)
        # 변경 확인용 영점(500) 이동 테스트
        ctrl.move_servo(servo_id=args.id, position=500, duration_ms=400)
        print(f"=== 서보 ID {args.id}번 할당 및 영점 확인 완료 ===")
    finally:
        ctrl.close()


if __name__ == "__main__":
    main()