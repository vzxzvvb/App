import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from pyparsing import empty
from streamlit_folium import st_folium
from streamlit_echarts import st_echarts

# 페이지 기본 설정
st.set_page_config(
    page_title= '장애인 이동보조수단 현황',
    page_icon= ':wheelchair:',
    layout='wide',
    menu_items= {
        'About' : '장애인의 이동보조수단 현황을 나타내는 대시보드입니다.'
    },
    initial_sidebar_state= 'expanded'
)


# 위 공백제거
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# 제목
st.markdown("<h1 style='text-align: center;'>전국 장애인 수와 이동보조수단 현황</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>시도별 장애인 현황</h2>", unsafe_allow_html=True)

st.write('전국 시도별 장애인 수를 지도시각화하여 장애인이 많이 거주하는 지역은 경기도이며 \n'
         '그 뒤로 서울 그 외 지방이 따르는 것을 알 수 있습니다.')

#2. 전체화면구성
empty1, con1, empty2 = st.columns([0.05,1.0,0.05])
empty1, tit1, empty2 = st.columns([0.05,1.0,0.05])
empty1, con2, empty2 = st.columns([0.05,1.0,0.05])
empty1, con3, empty2 = st.columns([0.05,1.0,0.05])
empty1, tit2, empty2 = st.columns([0.05,1.0,0.05])
empty1, con4, con5, con6, empty2 = st.columns([0.05,0.3,0.3,0.3,0.05])
empty1, tit3, empty2 = st.columns([0.05,1.0,0.05])
empty1, con7, con8, con9, empty2 = st.columns([0.05,0.3,0.3,0.3,0.05])


# 2-1. 가장 위 현황 (길쭉하게)
df1 = pd.read_csv('datas/시도별전체수급자수.csv', encoding='cp949')
df1.set_index('연월', drop=True, inplace=True)

# 2-2. 연령별성별 현황
df2 = pd.read_csv('datas/연령구간별성별.csv', encoding='cp949')
text = ['영유아','아동','청소년','청년','중년','장년','노년']
fig2 = go.Figure(
    layout=go.Layout(title=go.layout.Title(text="연령구간별 성별 수급자 수"))
)
fig2.add_trace(go.Bar(
    y=text,
    x=df2['합계(남)']*(-1),
    # 가운데 기본 값을 0으로 지정해주자
    base=0,
    name='남',
    orientation='h',
    marker=dict(
        color = 'rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 0.6)',width=3)
    )))
fig2.add_trace(go.Bar(
    y=text,
    x=df2['합계(여)'],
    # 가운데 기본 값을 0으로 지정해주자
    base=0,
    name='여', orientation='h',
    marker=dict(
        color='rgba(58, 71, 80, 0.6)',
        line=dict(color='rgba(58, 71, 80, 0.6)', width=3)
)))
fig2.update_layout(barmode='stack',
                    title_x = 0.35, title_y=0.83,
                    xaxis_title = "수급자 수",
                    yaxis_title = "연령 구간",
                    legend_title = "성별")

# 2-3. 시도별 장애유형 현황
df3 = pd.read_csv('datas/시도별장애유형별2.csv', encoding='cp949')
sido_geo = 'datas/Si_Do_map_utf8.json'


# 대전 중심으로 folium 맵 부르기
m = folium.Map(location=[36.45, 127.42],
                tiles='CartoDB positron',
                zoom_start=7)
# json map polygon 경계좌표값으로 구역별 색칠하기
# 칼라맵을 위해 Choropleth()함수에 값 설정해주기
folium.Choropleth(
    geo_data= sido_geo,
    data=df3,
    columns=['시도','시도별합계'],
    # json파일 열어보면 위경도가 딕셔너리형으로 묶여있는데 그 안에 CTP_KOR_NM에 ex.서울특별시를 키값으로 해주려함
    key_on='feature.properties.CTP_KOR_NM',
    fill_color='PuRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='장애인 수'
).add_to(m)

#2-4.






#2-5. 각 분석항목에 대한 전체현황 차트
# 도보(신호등, 횡단보도, 점자유무, 육교)

#st.write('<h3 ali>도보 보조시설</h3>', unsafe_allow_html=True)
# 신호등 (유무)
df4 = pd.read_csv('datas/03.신호등설치현황.csv', encoding='cp949')
data = [(df4['보조시설유무'], df4['보조시설유무']=='Z'),
        (df4['보조시설유무'], df4['보조시설유무']=='S'),
        (df4['보조시설유무'], df4['보조시설유무']=='V'),
        (df4['보조시설유무'], df4['보조시설유무']=='B')]

option4={
    "title":{"text":"신호등"},
    "legend":{"top":"bottom"},
    "toolbox":{
        "show":True,
        "feature": {
            "mark": {"show": True},
            "dataView": {"show": True, "readOnly": False},
            "restore": {"show": True},
            "saveAsImage": {"show": True}
        }
    },
    "series":[
        {
            "name":"신호등 보조시설 설치현황",
            "type":"pie",
            "radius":[10,80], # [내부반지름, 외부반지름]
            "center":["50%","50%"],
            "roseType":"area",
            "itemStyle":{"borderRadius":8},
            "data":[
                {"value": df4[df4['보조시설유무']=='Z'].shape[0], "name":"모두 없음"},
                {"value": df4[df4['보조시설유무']=='S'].shape[0], "name":"보행자작동신호기만 있음"},
                {"value": df4[df4['보조시설유무']=='V'].shape[0], "name":"음향신호기만 있음"},
                {"value": df4[df4['보조시설유무']=='B'].shape[0], "name":"모두 있음"}
            ]
        }
    ]
}
# 횡단보도 보조시설 (유무)
df5 = pd.read_csv('datas/04.시도별횡단보도설치현황2.csv', encoding='cp949')
data = [(df5['보조시설유무'], df5['보조시설유무']=='Z'),
        (df5['보행자신호등유무'], df5['보행자신호등유무']=='Y'),
        (df5['보도턱낮춤여부'], df5['보도턱낮춤여부']=='Y'),
        (df5['점자블록유무'], df5['점자블록유무']=='Y'),
        (df5['보조시설유무'], df5['보조시설유무']=='ABC')]

option5={
    "title":{"text":"횡단보도"},
    "legend":{"top":"bottom"},
    "toolbox":{
        "show":True,
        "feature": {
            "mark": {"show": True},
            "dataView": {"show": True, "readOnly": False},
            "restore": {"show": True},
            "saveAsImage": {"show": True}
        }
    },
    "series":[
        {
            "name":"횡단보도 보조시설 설치현황",
            "type":"pie",
            "radius":[10,80], # [내부반지름, 외부반지름]
            "center":["50%","50%"],
            "roseType":"area",
            "itemStyle":{"borderRadius":8},
            "data":[
                {"value": df5[df5['보조시설유무']=='Z'].shape[0], "name":"모두 없음"},
                {"value": df5[df5['보행자신호등유무']=='Y'].shape[0], "name":"신호등있는 횡단보도"},
                {"value": df5[df5['보도턱낮춤여부']=='Y'].shape[0], "name":"보도턱 낮춤"},
                {"value": df5[df5['점자블록유무'] == 'Y'].shape[0], "name": "점자 블록"},
                {"value": df5[df5['보조시설유무'] == 'ABC'].shape[0], "name": "모두 있음"}
            ]
        }
    ]
}

# 육교 보조시설(유무)
df6 = pd.read_csv('datas/05.육교설치현황.csv', encoding='cp949')
data6 = [(df6['보조시설유무'], df6['보조시설유무']=='Z'),
         (df6['엘리베이터'], df6['엘리베이터']=='Y'),
         (df6['경사로'], df6['경사로']=='Y'),
         (df6['점자블럭'], df6['점자블럭']=='Y'),
         (df6['리프트'], df6['리프트']=='Y'),
         (df6['턱'], df6['턱']=='Y'),
         (df6['핸드레일'], df6['핸드레일']=='Y')]

option6={
    "title":{"text":"육교"},
    "legend":{"top":"bottom"},
    "toolbox":{
        "show":True,
        "feature": {
            "mark": {"show": True},
            "dataView": {"show": True, "readOnly": False},
            "restore": {"show": True},
            "saveAsImage": {"show": True}
        }
    },
    "series":[
        {
            "name":"육교 보조시설 설치현황",
            "type":"pie",
            "radius":[10,80], #[내부반지름, 외부반지름]
            "center":["50%","50%"],
            "roseType":"area",
            "itemStyle":{"borderRadius":8},
            "data":[
                {"value": df6[df6['보조시설유무']=='Z'].shape[0], "name":"모두 없음"},
                {"value": df6[df6['엘리베이터']=='Y'].shape[0], "name":"엘리베이터"},
                {"value": df6[df6['경사로']=='Y'].shape[0], "name":"경사로"},
                {"value": df6[df6['점자블럭']=='Y'].shape[0], "name":"점자블럭"},
                {"value": df6[df6['리프트']=='Y'].shape[0], "name":"리프트"},
                {"value": df6[df6['턱']=='Y'].shape[0], "name":"턱"},
                {"value": df6[df6['핸드레일']=='Y'].shape[0], "name":"핸드레일"}
            ]
        }
    ]
}

#버스 보조시설(유무)
df7 = pd.read_csv('datas/시내버스.csv', encoding='cp949')
df8 = pd.read_csv('datas/저상버스.csv', encoding='cp949')
data7 = [(int(df7["합계(시내)"].values[0]), int(df7.iloc[9][1])),
         (int(df8["합계(저상)"].values[0]), int(df8.iloc[9][1]))]

option7={
    "title":{"text":"버스"},
    "legend":{"top":"bottom"},
    "toolbox":{
        "show":True,
        "feature": {
            "mark": {"show": True},
            "dataView": {"show": True, "readOnly": False},
            "restore": {"show": True},
            "saveAsImage": {"show": True}
        }
    },
    "series":[
        {
            "name":"2021년 시내버스 저상버스 도입 대수 현황입니다.",
            "type":"pie",
            "radius":[10,100], #[내부반지름, 외부반지름]
            "center":["50%","50%"],
            "roseType":"area",
            "itemStyle":{"borderRadius":8},
            "data":[
                {"value": int(df7.iloc[9][1]), "name":"시내 버스"},
                {"value": int(df8.iloc[9][1]), "name":"저상 버스"}
            ]
        }
    ]
}

#전철 보조시설(유무)
sub = pd.read_csv('datas/03.API_역사별_엘리베이터_현황.csv', encoding='cp949')
whl = pd.read_csv('datas/휠체어있는것.csv', encoding='cp949')


data8 = [(sub['승강기 상태'], sub[sub['승강기 상태']=='운행'].shape[0]),
         (whl['역명'], whl['역명'].shape[0])]

option8={
    "title":{"text":"전철 휠체어"},
    "legend":{"top":"bottom"},
    "toolbox":{
        "show":True,
        "feature": {
            "mark": {"show": True},
            "dataView": {"show": True, "readOnly": False},
            "restore": {"show": True},
            "saveAsImage": {"show": True}
        }
    },
    "series":[
        {
            "name":"휠체어 보조시설 설치현황",
            "type":"pie",
            "radius":[10,80], # [내부반지름, 외부반지름]
            "center":["50%","50%"],
            "roseType":"area",
            "itemStyle":{"borderRadius":8},
            "data":[
                {"value": sub[sub['승강기 상태']=='운행'].shape[0], "name":"전체역"},
                {"value": whl['역명'].shape[0], "name":"휠체어"}
            ]
        }
    ]
}


# 장애인용 차량운행
df9 = pd.read_csv('datas/교통약자이동지원_차트용.csv', encoding='cp949')
data9 = [(df9['슬로프형차량'], df9['슬로프형차량'].sum()),
         (df9['리프트형차량'], df9['리프트형차량'].sum()),
         (df9['일반차량'], df9['일반차량'].sum())]

option9={
    "title":{"text":"장애인용 차량"},
    "legend":{"top":"bottom"},
    "toolbox":{
        "show":True,
        "feature": {
            "mark": {"show": True},
            "dataView": {"show": True, "readOnly": False},
            "restore": {"show": True},
            "saveAsImage": {"show": True}
        }
    },
    "series":[
        {
            "name":"전국 장애인용 차량 운행 현황",
            "type":"pie",
            "radius":[10,80], #[내부반지름, 외부반지름]
            "center":["50%","50%"],
            "roseType":"area",
            "itemStyle":{"borderRadius":8},
            "data":[
                {"value": int(df9['슬로프형차량'].sum()), "name":"슬로프형차량"},
                {"value": int(df9['리프트형차량'].sum()), "name":"리프트형차량"},
                {"value": int(df9['일반차량'].sum()), "name":"일반차량"}
            ]
        }
    ]
}


## 레이아웃 실행
with empty1 :
    empty()

with con2 :
    st.line_chart(
        df1[['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시',
            '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도',
            '경상남도', '제주특별자치도']]
    )
with tit1 :
    st.markdown("<h3 style='text-align: center;'>시도별 10년간 장애인 현황 </h3>", unsafe_allow_html=True)
with con1 :
    st_folium(m,
              width=600,
              height=700)
# 연령별성별 수급자 수
with con3 :
    st.plotly_chart(fig2,
                    width=700,
                    height=700,
                    object_fit='cover')
    st.write('연령구간별로 나누어 장애인연금 수급자 수를 성별로 나타내었습니다')
with tit2 :
    st.subheader('도보 보조시설')

with con4 :
    st_echarts(options=option4, height="300px")
with con5 :
    st_echarts(options=option5, height="300px")
with con6 :
    st_echarts(options=option6, height="300px")

with tit3 :
    st.subheader('교통 보조시설')
with con7 :
    st_echarts(options=option7, height="300px")
with con8 :
    st_echarts(options=option8, height="300px")
with con9 :
    st_echarts(options=option9, height="300px")
with empty2 :
    empty()