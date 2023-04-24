import streamlit as st
from streamlit_folium import st_folium
import folium

st.title("위성영상 재난탐지 실습")
m = folium.Map(location=[37.5, 126.9], zoom_start=7)
st_folium(m, width=1024)

#streamlit run test.py --server.port 30002 --server.fileWatcherType none