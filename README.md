# Open-Meteo 날씨 수집기

진주와 대구의 현재 날씨를 Open-Meteo API에서 조회해 `data/weather.csv`에 누적합니다.

## 실행

```powershell
python weather_collector.py
```

CSV에는 수집 시각(한국 표준시), 지역, 좌표, 기온, 상대습도, 체감온도, 강수량, 날씨 코드와 사람이 읽을 수 있는 날씨 설명이 저장됩니다.

