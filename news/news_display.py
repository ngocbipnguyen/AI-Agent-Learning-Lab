import streamlit as st


def show_metrics(df):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Tổng số tin", len(df))

    with col2:
        st.metric("Số lĩnh vực", df["Lĩnh vực"].nunique())

    with col3:
        st.metric("Số nguồn tin", df["Nguồn"].nunique())


def show_chart(df):
    chart_data = df["Lĩnh vực"].value_counts()

    st.subheader("Thống kê tin tức theo lĩnh vực")
    st.bar_chart(chart_data)


def download_news(df):
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Tải tin tức về máy",
        data=csv,
        file_name="technology_news.csv",
        mime="text/csv"
    )