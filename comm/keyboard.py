import sys

if sys.platform == "win32":
    import msvcrt

    def get_key() -> str:
        """Windows 터미널에서 Enter 없이 키 1개를 즉시 입력받음"""
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):  # 방향키 등 특수키 건너뛰기
            msvcrt.getch()
            return ""
        return ch.decode("utf-8", errors="ignore").lower()
else:
    import termios
    import tty

    def get_key() -> str:
        """Linux(Jetson) 터미널에서 Enter 없이 키 1개를 즉시 입력받음"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.lower()