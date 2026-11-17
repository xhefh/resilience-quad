import math


class GaitPlanner:
    """4족 정상 보행 및 3족 회복탄력성 보행 궤적 생성기 (IK 연동 인터페이스)"""

    def __init__(self):
        self.phase = 0.0

    def reset(self):
        self.phase = 0.0

    def get_walk_angles(self, dt: float = 0.1) -> dict[int, tuple[float, float, float]]:
        """정상 4족 보행 시 다리(0~3)별 목표 각도(deg) 반환: {leg_id: (hip, thigh, knee)}"""
        self.phase = (self.phase + dt * 2.0 * math.pi) % (2.0 * math.pi)
        swing = 15.0 * math.sin(self.phase)
        lift = max(0.0, 20.0 * math.sin(self.phase))

        # 트롯(Trot) 보행 대각선 쌍: (0, 3) vs (1, 2)
        return {
            0: (0.0, swing, -lift),
            1: (0.0, -swing, -max(0.0, -20.0 * math.sin(self.phase))),
            2: (0.0, -swing, -max(0.0, -20.0 * math.sin(self.phase))),
            3: (0.0, swing, -lift),
        }

    def get_degraded_angles(self, fault_leg: int, dt: float = 0.1) -> dict[int, tuple[float, float, float]]:
        """고장 다리를 제외한 나머지 3개 다리 지지·보행 각도 반환"""
        self.phase = (self.phase + dt * 1.5 * math.pi) % (2.0 * math.pi)
        angles: dict[int, tuple[float, float, float]] = {}
        for leg_id in range(4):
            if leg_id == fault_leg:
                continue
            # 정상 3개 다리 무게중심 보정 기본 자세 (추후 3족 보행 IK로 교체)
            angles[leg_id] = (0.0, 5.0, -10.0)
        return angles