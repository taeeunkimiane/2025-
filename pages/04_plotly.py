import pandas as pd
import streamlit as st
import plotly.express as px

# 데이터 불러오기 (cp949로 인코딩된 CSV)
@st.cache_data
def load_data():
    df_sum = pd.read_csv("people_sum.csv", encoding="cp949")
    df_gender = pd.read_csv("people_gender.csv", encoding="cp949")
    return df_sum, df_gender

df_sum, df_gender = load_data()

# 지역 리스트
regions = df_sum['행정구역'].unique().tolist()
st.title("\U0001F4CA 2025년 5월 인구 피라미드 시각화")
selected_region = st.selectbox("\U0001F4CD 지역을 선택하세요", regions)

# 연령대 필터
age_min, age_max = st.slider("\U0001F39A️ 연령대 범위 선택", 0, 100, (0, 100))

# 선택한 지역 필터링
df_region_gender = df_gender[df_gender['행정구역'] == selected_region]

# 열 이름에서 연령 추출
male_cols = [col for col in df_region_gender.columns if "남_" in col and "세" in col]
female_cols = [col for col in df_region_gender.columns if "여_" in col and "세" in col]
ages = [int(col.split('_')[-1].replace("세", "").replace("이상", "")) for col in male_cols]

# 연령 필터 적용
filtered_indexes = [i for i, age in enumerate(ages) if age_min <= age <= age_max]
filtered_ages = [ages[i] for i in filtered_indexes]
males = [-int(str(df_region_gender[male_cols[i]].values[0]).replace(',', '')) for i in filtered_indexes]
females = [int(str(df_region_gender[female_cols[i]].values[0]).replace(',', '')) for i in filtered_indexes]

# 시각화용 데이터프레임 생성
df_plot = pd.DataFrame({
    "연령": filtered_ages * 2,
    "인구수": males + females,
    "성별": ["남성"] * len(males) + ["여성"] * len(females)
})

# 인구 피라미드 시각화
fig = px.bar(df_plot, x="인구수", y="연령", color="성별", orientation="h",
             title=f"\U0001F4CD {selected_region} 인구 피라미드", height=800)
st.plotly_chart(fig, use_container_width=True)
