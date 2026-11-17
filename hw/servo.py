import time

try:
    import serial
except ImportError:
    serial = None


class HiwonderServoController:
    FRAME_HEADER = 0x55
    CMD_SERVO_MOVE = 0x03
    CMD_SERVO_ID_WRITE = 0x0D

    def __init__(self, port: str = "COM3", baudrate: int = 115200, sim: bool = False):
        self.port = port
        self.baudrate = baudrate
        self.sim = sim
        self.ser = None

        if not self.sim:
            if serial is None:
                raise RuntimeError("pyserial이 설치되지 않았습니다. 'python -m pip install pyserial'을 실행하세요.")
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

    def set_servo_id(self, new_id: int, old_id: int = 0xFE):
        """서보 ID 변경 (old_id=0xFE 브로드캐스트 사용 시 반드시 서보 1개만 연결)"""
        new_id = max(1, min(253, int(new_id)))

        if self.sim:
            print(f"[SIM] 서보 ID 변경 패킷 전송: old={old_id} -> new={new_id}")
            return

        length = 4
        checksum = (~(old_id + length + self.CMD_SERVO_ID_WRITE + new_id)) & 0xFF

        packet = bytes([
            self.FRAME_HEADER,
            self.FRAME_HEADER,
            old_id,
            length,
            self.CMD_SERVO_ID_WRITE,
            new_id,
            checksum,
        ])
        self.ser.write(packet)

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()