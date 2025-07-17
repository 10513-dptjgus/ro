import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import re

# 페이지 설정
st.set_page_config(page_title="2025년 5월 연령별 인구 시각화", layout="wide")

st.title("2025년 5월 기준 연령별 인구 현황 및 지도 시각화")

# CSV 읽기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# ▶ 행정구역 괄호 제거: 예) 서울특별시(11) → 서울특별시
df['행정구역'] = df['행정구역'].str.replace(r"\s*\(\d+\)", "", regex=True).str.strip()

# ▶ 총인구수 숫자형 변환
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(",", "").astype(int)

# ▶ 연령별 컬럼 전처리
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_") and ("세" in col or "100세 이상" in col)]
new_columns = []
for col in age_columns:
    if "100세 이상" in col:
        new_columns.append("100세 이상")
    else:
        new_columns.append(col.replace("2025년05월_계_", "").replace("세", "") + "세")

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# ▶ 총인구수 기준 상위 5개 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# ▶ 원본 데이터 출력
st.subheader("📊 상위 5개 행정구역 원본 데이터")
st.dataframe(top5_df, use_container_width=True)

# ▶ 선그래프 출력
st.subheader("📈 상위 5개 행정구역 연령별 인구 변화 (세로: 연령 / 가로: 인구수)")
for _, row in top5_df.iterrows():
    region = row['행정구역']
    age_data = row[2:].astype(str).str.replace(',', '').astype(int)
    age_df = pd.DataFrame({
        '연령': top5_df.columns[2:],
        '인구수': age_data.values
    }).set_index('연령')
    st.write(f"#### 📍 {region}")
    st.line_chart(age_df.T)

# ▶ 행정구역별 좌표 정의 (JSON 없이 수동 설정)
region_coords = {
    "경기도": [37.4138, 127.5183],
    "서울특별시": [37.5665, 126.9780],
    "부산광역시": [35.1796, 129.0756],
    "경상남도": [35.4606, 128.2132],
    "인천광역시": [37.4563, 126.7052],
    "대구광역시": [35.8714, 128.6014],
    "경상북도": [36.5760, 128.5056],
    "대전광역시": [36.3504, 127.3845],
    "광주광역시": [35.1595, 126.8526],
    "울산광역시": [35.5384, 129.3114]
}

# ▶ Folium 지도 생성
st.subheader("🗺️ 상위 5개 행정구역 인구 지도")
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

for _, row in top5_df.iterrows():
    region = row['행정구역']
    pop = row['총인구수']
    coords = region_coords.get(region)
    if coords:
        folium.Circle(
            location=coords,
            radius=pop / 300,  # 원 크기 조절
            color='deeppink',
            fill=True,
            fill_color='pink',
            fill_opacity=0.5,
            popup=f"{region} : {pop:,}명",
            tooltip=region
        ).add_to(m)
    else:
        st.warning(f"❗ '{region}' 지역의 좌표 정보가 없습니다. 지도에 표시되지 않습니다.")

# ▶ 지도 출력
st_folium(m, width=900, height=600)

