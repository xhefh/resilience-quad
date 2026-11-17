from enum import Enum


class RobotState(Enum):
    IDLE = "IDLE"          # 대기 (초기 상태)
    STAND = "STAND"        # 기립 (영점 자세)
    WALK = "WALK"          # 정상 4족 보행
    DEGRADED = "DEGRADED"  # 고장 감지 후 3족 보행 (회복탄력성 모드)
    ESTOP = "ESTOP"        # 비상 정지


class StateMachine:
    def __init__(self):
        self.state = RobotState.IDLE
        self.fault_leg: int | None = None  # 고장 난 다리 번호 (0~3)

    def transition(self, event: str, fault_leg: int | None = None) -> RobotState:
        # 어떤 상태에서든 비상 정지 신호가 오면 즉시 ESTOP 전환
        if event == "ESTOP":
            self.state = RobotState.ESTOP
            return self.state

        if self.state == RobotState.IDLE and event == "START":
            self.state = RobotState.STAND
        elif self.state == RobotState.STAND and event == "WALK":
            self.state = RobotState.WALK
        elif self.state in (RobotState.STAND, RobotState.WALK) and event == "FAULT":
            self.fault_leg = fault_leg
            self.state = RobotState.DEGRADED
        elif self.state == RobotState.DEGRADED and event == "RECOVER":
            self.fault_leg = None
            self.state = RobotState.WALK
        elif event == "STOP":
            self.fault_leg = None
            self.state = RobotState.IDLE

        return self.state


if __name__ == "__main__":
    fsm = StateMachine()
    print("1. 초기 상태:", fsm.state.value)
    print("2. 기립 명령:", fsm.transition("START").value)
    print("3. 보행 시작:", fsm.transition("WALK").value)
    print("4. 다리 고장:", fsm.transition("FAULT", fault_leg=1).value, f"(고장 다리: {fsm.fault_leg}번)")
    print("5. 비상 정지:", fsm.transition("ESTOP").value)