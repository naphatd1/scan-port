import streamlit as st
import pandas as pd
import plotly.express as px
from scanner import scan
from db import init_db, connect
from config import DANGEROUS_PORTS

init_db()

st.set_page_config(layout="wide")
st.title("🔐 Network Port Scanner Dashboard")

ip_range = st.text_input("Enter IP Range", "192.168.2.1-254")
port_range = st.text_input("Enter Port Range", "1-1024")

if st.button("Start Scan"):
    with st.spinner("Scanning..."):
        results = scan(ip_range, port_range)
        st.success("Scan complete!")

df = pd.read_sql("SELECT * FROM scan_results ORDER BY scan_time DESC", connect())

if not df.empty:
    st.subheader("📊 Scan Results")

    st.dataframe(df)

    # Dangerous Ports Alert
    danger_df = df[df['port'].isin(DANGEROUS_PORTS)]
    if not danger_df.empty:
        st.warning("🚨 Dangerous Ports Found!")
        st.dataframe(danger_df)

    # Ranking
    ip_ranking = df.groupby('ip')['port'].count().reset_index(name='open_ports')
    ip_ranking = ip_ranking.sort_values(by='open_ports', ascending=False)
    st.subheader("🏆 IPs with Most Open Ports")
    st.dataframe(ip_ranking)

    # Chart
    fig = px.bar(ip_ranking, x='ip', y='open_ports', title="Open Ports by IP")
    st.plotly_chart(fig, use_container_width=True)

    # Export
    st.download_button("📥 Download CSV", df.to_csv(index=False), file_name="scan_report.csv")
    st.download_button("📄 Export HTML", df.to_html(index=False), file_name="scan_report.html")
