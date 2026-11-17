import argparse
from comm.keyboard import get_key
from fsm.state_machine import RobotState, StateMachine
from hw.servo import HiwonderServoController


def apply_pose(ctrl: HiwonderServoController, state: RobotState, fault_leg: int | None = None):
    """현재 로봇 상태에 맞춰 12개 서보 목표 위치 전송"""
    if state == RobotState.STAND:
        for sid in range(1, 13):
            ctrl.move_servo(sid, 500, 400)
    elif state == RobotState.WALK:
        # 정상 보행 테스트용 샘플 각도(다리 0번 관절 소폭 이동)
        ctrl.move_servo(1, 560, 300)
        ctrl.move_servo(2, 440, 300)
    elif state == RobotState.DEGRADED:
        # 고장 다리(예: 1번 다리 = 서보 4, 5, 6번)를 위로 접어 올림
        print(f"[회복탄력성 모드] {fault_leg}번 다리 회피 자세 적용")
        ctrl.move_servo(4, 700, 300)
        ctrl.move_servo(5, 700, 300)
    elif state == RobotState.ESTOP:
        print("[비상 정지] 모든 구동 명령 즉시 중단!")


def main():
    parser = argparse.ArgumentParser(description="4족 보행 회복탄력성 로봇 통합 제어기")
    parser.add_argument("--port", default="COM3", help="시리얼 포트 (Windows: COM3, Jetson: /dev/ttyUSB0)")
    parser.add_argument("--sim", action="store_true", help="시뮬레이션 모드로 실행")
    args = parser.parse_args()

    fsm = StateMachine()
    ctrl = HiwonderServoController(port=args.port, sim=args.sim)

    print("=== 키보드 조종 안내 ===")
    print("[1] 기립(STAND) | [2] 보행(WALK) | [f] 1번 다리 고장(DEGRADED)")
    print("[r] 복구(RECOVER) | [s] 대기(IDLE) | [Space] 비상정지(ESTOP) | [q] 종료")
    print(f"현재 상태: {fsm.state.value}\n")

    try:
        while True:
            key = get_key()
            if not key:
                continue

            if key == "q":
                print("프로그램을 종료합니다.")
                break
            elif key == "1":
                fsm.transition("START")
            elif key == "2":
                fsm.transition("WALK")
            elif key == "f":
                fsm.transition("FAULT", fault_leg=1)
            elif key == "r":
                fsm.transition("RECOVER")
            elif key == "s":
                fsm.transition("STOP")
            elif key == " ":
                fsm.transition("ESTOP")
            else:
                continue

            print(f"\n>>> 상태 전환: {fsm.state.value}")
            apply_pose(ctrl, fsm.state, fsm.fault_leg)
    finally:
        ctrl.close()


if __name__ == "__main__":
    main()