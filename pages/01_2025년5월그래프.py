import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import re

st.set_page_config(layout="wide")

st.title("2025년 5월 기준 연령별 인구 현황")

# CSV 파일 로드
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 전처리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령별 컬럼 추출
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]

# 컬럼명 변경
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

# 정리된 데이터프레임 만들기
df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 괄호 안 숫자 제거 (예: '서울특별시(11)' → '서울특별시')
df_age['행정구역'] = df_age['행정구역'].apply(lambda x: re.sub(r'\([^)]*\)', '', x).strip())

# 상위 5개 행정구역
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 📊 원본 데이터 출력
st.subheader("📋 상위 5개 행정구역 원본 데이터")
st.dataframe(top5_df, use_container_width=True)

# 📈 선그래프 출력 (Streamlit 기본 기능 사용)
st.subheader("📈 연령별 인구 변화 (상위 5개 행정구역)")

for i, row in top5_df.iterrows():
    region = row['행정구역']
    age_data = row[2:].astype(str).str.replace(',', '').astype(int)
    age_df = pd.DataFrame({
        '연령': top5_df.columns[2:],
        '인구수': age_data.values
    }).set_index('연령')

    st.write(f"#### 📍 {region}")
    st.line_chart(age_df)

# 📍 지도 시각화
st.subheader("🗺️ 상위 5개 행정구역 위치 (핑크색 원)")

# 행정구역 이름 → 위도, 경도 매핑 (간단 버전 수동 작성)
location_dict = {
    "서울특별시": (37.5665, 126.9780),
    "부산광역시": (35.1796, 129.0756),
    "경기도": (37.4138, 127.5183),
    "대구광역시": (35.8714, 128.6014),
    "인천광역시": (37.4563, 126.7052),
    "경상남도": (35.4606, 128.2132),
    "경상북도": (36.5760, 128.5056),
    "대전광역시": (36.3504, 127.3845),
    "광주광역시": (35.1595, 126.8526),
    "울산광역시": (35.5384, 129.3114)
}

# Folium 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

for i, row in top5_df.iterrows():
    region = row['행정구역']
    if region in location_dict:
        lat, lon = location_dict[region]
        folium.CircleMarker(
            location=(lat, lon),
            radius=20,
            color='pink',
            fill=True,
            fill_opacity=0.4,
            popup=region
        ).add_to(m)
    else:
        st.warning(f"{region}의 위치 정보가 없어 지도에 표시되지 않았습니다.")

# 지도 표시
st_data = st_folium(m, width=700, height=500)
