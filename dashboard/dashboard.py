import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("Dashboard Bike Sharing 🚴")


st.markdown("""Dashboard ini menampilkan analisis pola penggunaan sepeda berdasarkan jam, musim, dan hari.""")

# Load data
day_df = pd.read_csv("day_cleaned.csv", parse_dates=["dteday"])
hour_df = pd.read_csv("hour_cleaned.csv", parse_dates=["dteday"])

# Sidebar
st.sidebar.header("Filter Data")

# Season mapping
season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

selected_season = st.sidebar.selectbox(
    "Pilih Musim",
    options=sorted(day_df["season"].unique()),
    format_func=lambda x: season_map[x]
)

# Working day mapping
workingday_map = {
    0: "Weekend/Holiday",
    1: "Working Day"
}

selected_workingday = st.sidebar.selectbox(
    "Tipe Hari",
    options=sorted(hour_df["workingday"].unique()),
    format_func=lambda x: workingday_map[x]
)

# Filter
filtered_day = day_df[day_df["season"] == selected_season].copy()
filtered_hour = hour_df[hour_df["workingday"] == selected_workingday].copy()


weekday_map = {
    0: "Sun", 1: "Mon", 2: "Tue",
    3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"
}

filtered_day["weekday_label"] = filtered_day["weekday"].map(weekday_map)

# Layout

# Metric
st.subheader("📊 Ringkasan")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rental", int(filtered_day["cnt"].sum()))
col2.metric("Rata-rata Rental", int(filtered_day["cnt"].mean()))
col3.metric("Max Rental", int(filtered_day["cnt"].max()))


# Visualisasi 1
st.subheader("📅 Penyewaan Berdasarkan Hari")

fig1, ax1 = plt.subplots(figsize=(12,6))

sns.barplot(
    data=filtered_day,
    x="weekday_label",
    y="cnt",
    order=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    ax=ax1
)

ax1.set_title("Rata-rata Penyewaan per Hari")
ax1.set_xlabel("Hari")
ax1.set_ylabel("Jumlah Penyewaan")

ax1.set_ylim(0, 8000) 

st.pyplot(fig1)

st.markdown("---")

# Visualisasi 2
st.subheader("⏰ Pola Penyewaan Berdasarkan Jam")

hourly_usage = filtered_hour.groupby("hr")["cnt"].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(12,6))

sns.lineplot(
    data=hourly_usage,
    x="hr",
    y="cnt",
    ax=ax2
)

ax2.set_title("Rata-rata Penyewaan per Jam")
ax2.set_xlabel("Jam")
ax2.set_ylabel("Jumlah Penyewaan")

ax2.set_ylim(0, 700)

st.pyplot(fig2)

st.markdown("---")


# Visualisasi 3
st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan")

weather_map = {
    1: "Clear",
    2: "Mist",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}

weather_usage = day_df.groupby("weathersit")["cnt"].mean().reset_index()
weather_usage["weather_label"] = weather_usage["weathersit"].map(weather_map)

fig3, ax3 = plt.subplots(figsize=(12,6))

sns.barplot(
    data=weather_usage,
    x="weather_label",
    y="cnt",
    ax=ax3
)

ax3.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
ax3.set_xlabel("Kondisi Cuaca")
ax3.set_ylabel("Jumlah Penyewaan")

ax3.set_ylim(0, 8000)

st.pyplot(fig3)

