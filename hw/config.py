# 다리 인덱스 정의
LEG_NAMES = {
    0: "FL (전좌)",
    1: "FR (전우)",
    2: "RL (후좌)",
    3: "RR (후우)",
}

# 다리별 서보 ID 매핑: [Hip(골반), Thigh(허벅지), Knee(무릎)]
LEG_SERVO_IDS: dict[int, tuple[int, int, int]] = {
    0: (1, 2, 3),    # FL
    1: (4, 5, 6),    # FR
    2: (7, 8, 9),    # RL
    3: (10, 11, 12), # RR
}

# 좌/우 대칭 장착에 따른 회전 방향 부호 (+1 또는 -1)
LEG_DIR_SIGNS: dict[int, tuple[int, int, int]] = {
    0: (1, 1, 1),
    1: (1, -1, -1),
    2: (1, 1, 1),
    3: (1, -1, -1),
}

# 서보별 안전 허용 범위 (펄스 0~1000 기준, 기구물 간섭 방지)
PULSE_MIN = 150
PULSE_MAX = 850
PULSE_CENTER = 500
PULSES_PER_DEG = 1000.0 / 240.0

# 고장 난 다리를 지면에서 들어 올려 접는 안전 회피 각도 (deg)
FAULT_FOLD_ANGLES_DEG = (0.0, 55.0, -75.0)


def deg_to_pulse(leg_id: int, joint_idx: int, angle_deg: float) -> int:
    """관절 각도(deg)를 방향 부호와 안전 한계를 적용해 서보 펄스(150~850)로 변환"""
    sign = LEG_DIR_SIGNS[leg_id][joint_idx]
    raw_pulse = PULSE_CENTER + (angle_deg * sign * PULSES_PER_DEG)
    return int(max(PULSE_MIN, min(PULSE_MAX, round(raw_pulse))))