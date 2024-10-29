import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import platform
import matplotlib.pyplot as plt

# 폰트 설정 함수 (Streamlit Cloud에서 폰트가 없을 경우 기본 폰트를 사용)
def set_font():
    try:
        # NanumGothic 폰트가 있는 경우 설정하고, 없으면 기본 폰트 사용
        font_path = "NanumGothic.ttf"
        if not os.path.exists(font_path):
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 오류 해결
        else:
            from matplotlib import font_manager as fm
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
    except Exception as e:
        st.warning(f"폰트 설정 실패: {e}")
        plt.rcParams['font.family'] = 'sans-serif'

# 폰트 설정 적용
set_font()

# Streamlit 코드 시작
st.title("🌡️ 통합국 온도 모니터링 대시보드")

uploaded_file = st.file_uploader("📁 CSV 파일을 업로드하세요:", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    data['날짜'] = pd.to_datetime(data['날짜'])
    data = data.dropna(subset=['온도'])
    data = data[data['온도'] > 0]

    unique_locations = sorted(data['통합국명'].unique())
    selected_location = st.selectbox("📍 통합국명을 선택하세요:", ["전체"] + unique_locations)

    if selected_location == "전체":
        filtered_data = data
    else:
        filtered_data = data[data['통합국명'] == selected_location]

    # 최근 1개월 데이터 필터링
    one_month_ago = datetime.now() - timedelta(days=30)
    month_data = filtered_data[filtered_data['날짜'] >= one_month_ago]
    
    # month_data가 비어있지 않을 경우에만 idxmax 및 idxmin 사용
    if not month_data.empty:
        max_temp_row = month_data.loc[month_data['온도'].idxmax()]
        min_temp_row = month_data.loc[month_data['온도'].idxmin()]
        st.write("최고 온도:", max_temp_row['온도'], "날짜:", max_temp_row['날짜'])
        st.write("최저 온도:", min_temp_row['온도'], "날짜:", min_temp_row['날짜'])
    else:
        st.warning("최근 1개월 동안 온도 데이터가 없습니다.")
