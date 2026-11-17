import time

try:
    import serial
except ImportError:
    serial = None


class HiwonderServoController:
    FRAME_HEADER = 0x55
    CMD_SERVO_MOVE = 0x03

    def __init__(self, port: str = "COM3", baudrate: int = 115200, sim: bool = False):
        self.port = port
        self.baudrate = baudrate
        self.sim = sim
        self.ser = None

        if not self.sim:
            if serial is None:
                raise RuntimeError("pyserial이 설치되지 않았습니다. 'pip install pyserial'을 실행하세요.")
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.5)
            time.sleep(0.1)

    def move_servo(self, servo_id: int, position: int = 500, duration_ms: int = 500):
        """서보 ID(1~12)를 목표 위치(0~1000, 중앙=500)로 duration_ms 동안 이동"""
        position = max(0, min(1000, int(position)))
        duration_ms = max(20, min(30000, int(duration_ms)))

        if self.sim:
            print(f"[SIM] 서보 ID {servo_id:02d} -> 위치 {position} ({duration_ms}ms)")
            return

        # Hiwonder Serial Bus Servo 패킷 구성
        pos_l = position & 0xFF
        pos_h = (position >> 8) & 0xFF
        time_l = duration_ms & 0xFF
        time_h = (duration_ms >> 8) & 0xFF

        length = 7  # 파라미터 개수(5) + 2
        checksum = (~(servo_id + length + self.CMD_SERVO_MOVE + pos_l + pos_h + time_l + time_h)) & 0xFF

        packet = bytes([
            self.FRAME_HEADER,
            self.FRAME_HEADER,
            servo_id,
            length,
            self.CMD_SERVO_MOVE,
            pos_l,
            pos_h,
            time_l,
            time_h,
            checksum,
        ])
        self.ser.write(packet)

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()