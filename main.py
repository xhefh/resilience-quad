import argparse
from comm.keyboard import get_key
from control.gait import GaitPlanner
from detect.fault_detector import FaultDetector
from fsm.state_machine import RobotState, StateMachine
from hw.config import (
    FAULT_FOLD_ANGLES_DEG,
    LEG_NAMES,
    LEG_SERVO_IDS,
    PULSE_CENTER,
    deg_to_pulse,
)
from hw.servo import HiwonderServoController


def set_leg_angles(ctrl: HiwonderServoController, leg_id: int, angles_deg: tuple[float, float, float], duration_ms: int = 300):
    servo_ids = LEG_SERVO_IDS[leg_id]
    for joint_idx, (sid, deg) in enumerate(zip(servo_ids, angles_deg)):
        pulse = deg_to_pulse(leg_id, joint_idx, deg)
        ctrl.move_servo(sid, pulse, duration_ms)


def apply_pose(ctrl: HiwonderServoController, gait: GaitPlanner, state: RobotState, fault_leg: int | None = None):
    if state == RobotState.STAND:
        gait.reset()
        for sid in range(1, 13):
            ctrl.move_servo(sid, PULSE_CENTER, 400)

    elif state == RobotState.WALK:
        leg_angles = gait.get_walk_angles(dt=0.1)
        for leg_id, angles in leg_angles.items():
            set_leg_angles(ctrl, leg_id, angles, duration_ms=250)

    elif state == RobotState.DEGRADED and fault_leg is not None:
        print(f"[회복탄력성 모드] {fault_leg}번 다리 {LEG_NAMES[fault_leg]} 회피 자세 적용")
        set_leg_angles(ctrl, fault_leg, FAULT_FOLD_ANGLES_DEG, duration_ms=300)
        support_angles = gait.get_degraded_angles(fault_leg=fault_leg, dt=0.1)
        for leg_id, angles in support_angles.items():
            set_leg_angles(ctrl, leg_id, angles, duration_ms=300)

    elif state == RobotState.ESTOP:
        print("[비상 정지] 모든 구동 명령 즉시 중단! 해제하려면 [s](IDLE)를 누르세요.")


def main():
    parser = argparse.ArgumentParser(description="4족 보행 회복탄력성 로봇 통합 제어기")
    parser.add_argument("--port", default="COM3", help="시리얼 포트 (Windows: COM3, Jetson: /dev/ttyUSB0)")
    parser.add_argument("--sim", action="store_true", help="시뮬레이션 모드로 실행")
    args = parser.parse_args()

    fsm = StateMachine()
    gait = GaitPlanner()
    detector = FaultDetector()
    ctrl = HiwonderServoController(port=args.port, sim=args.sim)

    print("=== 키보드 조종 안내 ===")
    print("[1] 기립(STAND) | [2] 보행(WALK) | [r] 복구(RECOVER) | [s] 대기(IDLE)")
    print("[3] 0번(FL) 고장 | [4] 1번(FR) 고장 | [5] 2번(RL) 고장 | [6] 3번(RR) 고장")
    print("[Space] 비상정지(ESTOP) | [q] 종료")
    print(f"현재 상태: {fsm.state.value}\n")

    fault_key_map = {"3": 0, "4": 1, "5": 2, "6": 3}

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
            elif key in fault_key_map:
                detector.inject_manual_fault(fault_key_map[key])
                detected = detector.check_fault()
                if detected is not None:
                    fsm.transition("FAULT", fault_leg=detected)
            elif key == "r":
                detector.inject_manual_fault(None)
                fsm.transition("RECOVER")
            elif key == "s":
                detector.inject_manual_fault(None)
                fsm.transition("STOP")
            elif key == " ":
                fsm.transition("ESTOP")
            else:
                continue

            print(f"\n>>> 상태 전환: {fsm.state.value}")
            apply_pose(ctrl, gait, fsm.state, fsm.fault_leg)
    finally:
        ctrl.close()


if __name__ == "__main__":
    main()