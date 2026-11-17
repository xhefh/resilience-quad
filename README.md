# resilience-quad
4족 보행 회복탄력성 로봇 제어 및 고장 대응 시스템

## 폴더 구조
- `fsm/`: 로봇 상태 머신 (`IDLE`, `STAND`, `WALK`, `DEGRADED`, `ESTOP`)
- `hw/`: Hiwonder 시리얼 버스 서보 드라이버(`servo.py`) 및 ID·안전각도 설정(`config.py`)
- `control/`: 4족 정상 보행 및 3족 회복탄력성 보행 궤적 생성기 (`gait.py`)
- `detect/`: 다리 고장 감지기 (`fault_detector.py`)
- `tools/`: 서보 ID 부여(`set_id.py`), 영점 정렬(`center_all.py`), 개별 관절 테스트(`test_joint.py`)
- `comm/`: Windows/Linux 겸용 실시간 키보드 입력 모듈
- `main.py`: 통합 제어 실행 진입점

## 다리 및 서보 ID 매핑 규격
- 서보 펄스 범위: `0 ~ 1000` (중앙 영점 `500`, 안전 제한 `150 ~ 850`)

| 다리 인덱스 | 위치 | Hip (골반) | Thigh (허벅지) | Knee (무릎) |
| :---: | :---: | :---: | :---: | :---: |
| `0` | FL (전좌) | ID 1 | ID 2 | ID 3 |
| `1` | FR (전우) | ID 4 | ID 5 | ID 6 |
| `2` | RL (후좌) | ID 7 | ID 8 | ID 9 |
| `3` | RR (후우) | ID 10 | ID 11 | ID 12 |

## 실행 방법
```bash
# 1. 통합 시뮬레이션 모드
python main.py --sim

# 2. 서보 ID 개별 할당 (반드시 서보 1개만 연결 후 실행)
python tools/set_id.py --id 3 --sim

# 3. 전체 서보 영점(500) 정렬
python tools/center_all.py --sim

# 4. 개별 서보 가동범위 테스트
python tools/test_joint.py --id 1 --pos 600 --sim
```