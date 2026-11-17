class FaultDetector:
    """서보 피드백(온도/전압/위치 오차) 및 IMU 기반 다리 고장 감지기"""

    def __init__(self):
        self.manual_fault_leg: int | None = None

    def inject_manual_fault(self, leg_id: int | None):
        """키보드 테스트용 수동 고장 주입 (0~3 또는 None)"""
        self.manual_fault_leg = leg_id

    def check_fault(self, servo_telemetry: dict | None = None) -> int | None:
        """
        고장 다리 번호(0~3) 반환, 정상이면 None 반환.
        추후 servo_telemetry(위치 추종 오차, 과전류 등) 분석 로직 연결.
        """
        if self.manual_fault_leg is not None:
            return self.manual_fault_leg
        return None