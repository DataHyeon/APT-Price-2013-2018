# %%
# Module
import pandas as pd
import numpy as np
import os
import re
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import missingno as msno
import warnings
from plotnine import *

# %%
# Setting Warning MSG
warnings.filterwarnings(action = "ignore")

# Setting DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)
pd.options.display.float_format = '{:,.0f}'.format

# Setting Font
mpl.rcParams['axes.unicode_minus'] = False
data = np.random.randint(-100, 100, 50).cumsum()

print(f'폰트 설치 위치 : {mpl.__file__}')
print(f'폰트 설정 위치 : {mpl.get_configdir()}')
print(f'폰트 캐시 위치 : {mpl.get_cachedir()}')
print(f'폰트 설정 파일 위치 : {mpl.matplotlib_fname()}')
print(f'현재 폰트 / 사이즈 : {plt.rcParams["font.family"]} / {plt.rcParams["font.size"]}')

font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf') 
nanum_font_list = [_ for _ in font_list if 'Nanum' in _]

font_path = nanum_font_list[0]

## Check Font
# %%
# fm.FontProperties
fontprop = fm.FontProperties(fname=font_path, size=18)

data = np.random.randint(-100,100,50).cumsum()
plt.plot(range(50), data, 'r')
plt.title('시간별 가격 추이')
plt.ylabel('주식 가격')
plt.xlabel('시간(분)')

# %%
# global font
plt.rcParams['font.family'] = 'Nanum Brush Script'
plt.rcParams['font.size'] = 18

data = np.random.randint(-100,100,50).cumsum()
plt.plot(range(50), data, 'r')
plt.title('시간별 가격 추이')
plt.ylabel('주식 가격')
plt.xlabel('시간(분)')

# %%
# Load Data
os.listdir('./../Input_data')
pre_sale = pd.read_csv('./../Input_data/전국_평균_분양가격_2018.6월_.csv', encoding='cp949')
pre_sale.shape

# %%
# 결측치 확인
print(pre_sale.isnull().sum())
# missingno 시각화
msno.matrix(pre_sale, figsize=(18,6)) # 분양가격에 결측치 존재

# Basic Information
print(pre_sale.head())
print(pre_sale.tail())
print(pre_sale.info())

# 분양 가격의 데이터 타입 : object ; => int
# 연도, 월에 대한 데이터 타입 변경 : int =>  str
pre_sale_price = pre_sale.iloc[:, -1]
type(pre_sale_price)

pre_sale['연도'] = pre_sale['연도'].astype(str)
pre_sale['월'] = pre_sale['월'].astype(str)

pre_sale['분양가격'] = pd.to_numeric(pre_sale_price, errors='coerce')

# 평당 분양 가격 컬럼 추가
pre_sale['평당분양가격'] = pre_sale['분양가격'] * 3.3

# 결측치 재확인
print(pre_sale.isnull().sum()) # 뷴양가격을 수치화 하면서 Nan 값 증가

# %%
# 세부 데이터 확인
# 분양 가격에 대한 컬럼(수치형) 데이터 요약통계량 확인
print(pre_sale.describe())

# 수치형이 아닌 데이터 컬럼에 대해서 확인
print(pre_sale.describe(include=[np.object]))

# 2017년도 데이터 확인
pre_sale_2017 = pre_sale.loc[pre_sale['연도'] == '2017']
pre_sale_2017.shape 

# 연도별 기준 전국 평균 분양 가격 확인(요약통계량)
pre_sale.groupby(pre_sale.연도).describe().T

# 규모별 기준 전국 평균 분양가격 확인(평당분양가격, 연도 관련 피벗테이블 생성)
pre_sale.pivot_table('평당분양가격', '규모구분', '연도')

# 규모가 전체로 되어있는 금액으로 연도별 변동금액 확인
# 연도별 각 지역의 변동액 확인
region_year_all = pre_sale.loc[pre_sale['규모구분']=='전체']
region_year = region_year_all.pivot_table('평당분양가격', '지역명', '연도').reset_index()
region_year['변동액(2015~2018)'] = (region_year['2018'] - region_year['2015']).astype(int)
region_year = region_year.sort_values(['변동액(2015~2018)']).reset_index(drop=True)
region_year = region_year.rename(columns={'변동액(2015~2018)': '변동액'})

low_region = region_year.iloc[0,np.r_[0,-1]]
high_region = region_year.iloc[-1,np.r_[0,-1]]

print(f'\n2015년에서 2018년 지역별 변동액\n가장 큰 곳 : {low_region["지역명"]}\n변동액 : {low_region["변동액"]}(천원)\n가장 적은 곳 : {high_region["지역명"]}\n변동액 : {high_region["변동액"]}(천원)')

# %%
# 연도별 변동 그래프 시각화
fontprop = fm.FontProperties(fname=font_path, size=8)
(ggplot(region_year_all, aes(x='지역명', y='평당분양가격', fill='연도'))
 + geom_bar(stat='identity', position='dodge')
 + ggtitle('2015-2018년 신규 민간 아파트 분양가격')
 + theme(text=element_text(fontproperties=fontprop),
         figure_size=(8,4))
)

# %%
# 지역별 평당 분양 가격 합계
pre_sale.pivot_table('평당분양가격', '규모구분', '지역명')

# %%
# 규모별 지역 평당 분양 가격 시각화
fontprop = fm.FontProperties(fname=font_path, size=8)
(ggplot(pre_sale)
 + aes(x='지역명', y='평당분양가격', fill='규모구분')
 + geom_bar(stat='identity', position='dodge')
 + ggtitle('규모별 신규 민간 아파트 분양가격')
 + theme(text=element_text(fontproperties=fontprop),
         figure_size=(8,4))
 )

# %%
# 지역별 시각화
fontprop = fm.FontProperties(fname=font_path, size=8)
(ggplot(pre_sale)
 + aes(x='연도', y='평당분양가격', fill='규모구분')
 + geom_bar(stat='identity', position='dodge')
 + facet_wrap('지역명')
 + theme(text=element_text(fontproperties=fontprop),
         axis_text_x=element_text(rotation=70),
         figure_size=(12, 12))
)

# %%
# 전국 이상치 확인 시각화 ; BoxPlot
(ggplot(pre_sale)
 + aes(x='지역명', y='평당분양가격', fill='규모구분')
 + geom_boxplot()
 + ggtitle('전국 규모별 신규 민간 아파트 분양가격 BoxPlot')
 + theme(text=element_text(fontproperties=fontprop),
         figure_size=(12, 6))
)

# %%
# 서울 지역 이상치 확인 시각화 ; BoxPlot
(ggplot(pre_sale.loc[pre_sale['지역명']=='서울'])
 + aes(x='지역명', y='평당분양가격', fill='규모구분')
 + geom_boxplot()
 + ggtitle('서울 규모별 신규 민간 아파트 분양가격 BoxPlot')
 + theme(text=element_text(fontproperties=fontprop))
)

# %%
# 제주 지역 이상치 확인 시각화 ; BoxPlot
(ggplot(pre_sale.loc[pre_sale['지역명']=='제주'])
 + aes(x='지역명', y='평당분양가격', fill='규모구분')
 + geom_boxplot()
 + ggtitle('제주 규모별 신규 민간 아파트 분양가격 BoxPlot')
 + theme(text=element_text(fontproperties=fontprop))
)

# %%
# 울산 지역 이상치 확인 시각화 ; BoxPlot
(ggplot(pre_sale.loc[pre_sale['지역명']=='울산'])
 + aes(x='지역명', y='평당분양가격', fill='규모구분')
 + geom_boxplot()
 + ggtitle('울산 규모별 신규 민간 아파트 분양가격 BoxPlot')
 + theme(text=element_text(fontproperties=fontprop))
)

# %%
# 서울, 제주, 울산 지역 비교 이상치 확인 시각화 ; BoxPlot
(ggplot(pre_sale.loc[(pre_sale['지역명']=='서울') | (pre_sale['지역명']=='제주') | (pre_sale['지역명']=='울산')])
 + aes(x='지역명', y='평당분양가격', fill='규모구분')
 + geom_boxplot()
 + ggtitle('울산 규모별 신규 민간 아파트 분양가격 BoxPlot')
 + theme(text=element_text(fontproperties=fontprop))
)

# %%
# To CSV
df_to_csv = pre_sale[['지역명', '연도', '월', '평당분양가격']].loc[pre_sale['규모구분']=='전체']
df_to_csv.to_csv('2015-2018.csv', index=False)