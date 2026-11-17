# resilience-quad
4족 보행 회복탄력성 로봇 제어 및 고장 대응 시스템

## 폴더 구조
- `fsm/`: 로봇 상태 머신 (`IDLE`, `STAND`, `WALK`, `DEGRADED`, `ESTOP`)
- `hw/`: Hiwonder 시리얼 버스 서보 드라이버
- `tools/`: 전체 서보 영점(500) 정렬 스크립트
- `comm/`: Windows/Linux 겸용 실시간 키보드 입력 모듈
- `main.py`: 통합 제어 실행 진입점

## 실행 방법
```bash
# 시뮬레이션 모드
python main.py --sim

# 전체 서보 영점 정렬 (실물 연결 시 --sim 제거 후 포트 지정)
python tools/center_all.py --sim
```