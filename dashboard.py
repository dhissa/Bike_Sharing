import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

days_df = pd.read_csv("https://raw.githubusercontent.com/dhissa/bikesharingdata/refs/heads/main/day.csv")
days_df.head()

hours_df = pd.read_csv("https://raw.githubusercontent.com/dhissa/bikesharingdata/refs/heads/main/hour.csv")
hours_df.head()

#Mengubah beberapa detail tentang kolom pada days_df
days_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_condition',
    'hum' : 'humidity',
    'cnt': 'count'
}, inplace=True)

days_df.head()

#Mengubah beberapa detail tentang kolom pada hours_df
hours_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_condition',
    'hum':'humidity',
    'cnt': 'count',
    'hr' : 'hour'
}, inplace=True)

hours_df.head()

# Mengubah angka pada days_df menjadi keterangan
days_df['season'] = days_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
days_df['month'] = days_df['month'].map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                                         7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
days_df['weekday'] = days_df['weekday'].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
days_df['weather_condition'] = days_df['weather_condition'].map({1: 'Clear', 2: 'Misty/Cloudy', 
                                                                 3: 'Light Snow/Rain', 4: 'Snow + Fog'})

# Mengubah angka pada hours_df menjadi keterangan
hours_df['season'] = hours_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
hours_df['month'] = hours_df['month'].map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                                         7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
hours_df['weekday'] = hours_df['weekday'].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
hours_df['weather_condition'] = hours_df['weather_condition'].map({1: 'Clear', 2: 'Misty/Cloudy',
                                                                   3: 'Light Snow/Rain', 4: 'Snow + Fog'})
 

# Menyiapkan hourly_rent_df
def create_hourly_rent_df(df):
    hourly_rent_df = df.groupby(by='hour').agg({
        'count': 'sum'
    }).reset_index()
    return hourly_rent_df
                                                                                                                                    
# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season').agg({
        'count': 'sum'
    }).reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_condition').agg({
        'count': 'sum'
    })
    return weather_rent_df

# Membuat komponen filter
min_date = pd.to_datetime(days_df['dateday']).dt.date.min()
max_date = pd.to_datetime(days_df['dateday']).dt.date.max()
 
with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Timeline',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = days_df[(days_df['dateday'] >= str(start_date)) & 
                (days_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
hourly_rent_df = create_hourly_rent_df(hours_df)
daily_rent_df = create_daily_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

#Membuat Dashboard
#Judul
st.header('Bike Sharing Dashboard')

#Sub Judul
st.subheader('Bike Sharing User')

#Total User
col1 = st.columns(1)

with col1[0]:
  total_user = daily_rent_df["count"].sum()
  st.metric("Total User", value=total_user)
  
# Fungsi untuk visualisasi berdasarkan musim
def plot_seasonal_sharing():
    hours_df.groupby(by='season').agg({
    'count': ['min', 'max', 'mean', 'sum']
})

    plt.figure(figsize=(10, 5))
    colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="count", 
        y="season",
        hue='season',
        data=days_df.sort_values(by="count", ascending=False),
        palette=colors_,
        errorbar=None
    )

    plt.title("Number of Bike Sharing by Season", loc="center", fontsize=15)
    plt.ylabel("Season")
    plt.xlabel("Count")
    plt.tick_params(axis='y', labelsize=12)

    # Tampilkan plot
    st.pyplot(plt)

# Fungsi untuk visualisasi rata-rata peminjaman per jam
def plot_hourly_sharing():
    rent_hours = hours_df.groupby('hour')['count'].mean()
    
    plt.figure(figsize=(12, 6))
    plt.bar(rent_hours.index, rent_hours.values, color='#1f77b4')

    plt.title('Average Rent per Hours')
    plt.xlabel('Time')
    plt.ylabel('Average Rent')
    plt.xticks(range(0, 24))
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for index, value in enumerate(rent_hours.values):
     plt.text(index, value, f'{value:.1f}', ha='center', va='bottom')

    #Tampilkan plot
    st.bar_chart(rent_hours)
    
# Fungsi untuk visualisasi peminjaman setiap hari
def plot_daily_sharing():
    
    hours_df.groupby(by='weekday').agg({
    'count': ['min', 'max', 'mean', 'sum']
    })

    fig, ax = plt.subplots(figsize=(20, 5))

    sns.pointplot(
        data=hours_df, 
        x='hour', 
        y='count', 
        hue='weekday', 
        ax=ax,
        palette='Set1' 
    )

    ax.set(title='Count of Bikes During Weekdays and Weekend', xlabel='Hour of Day', ylabel='Total Bike Count')
    ax.legend(title='Day of Week', loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.xticks(range(24))

    # Tampilkan plot
    st.pyplot(plt)


# Fungsi untuk visualisasi peminjaman berdasarkan cuaca
def plot_weather_sharing():
    hours_df.groupby(by='weather_condition').agg({
    'count': ['min', 'max', 'mean', 'sum']
    })

    plt.figure(figsize=(10,5))

    sns.barplot(
        y='count',
        x='weather_condition',
        hue='weather_condition',
        data=hours_df.sort_values(by='count', ascending=False),
        errorbar=None
    )

    plt.title("Number of Bike Sharing by Weather Condition", loc="center", fontsize=15)
    plt.ylabel("Count")
    plt.xlabel("Weather")
    plt.tick_params(axis='x', labelsize=12)
    plt.show()

    # Tampilkan plot
    st.pyplot(plt)

# Memanggil fungsi untuk setiap visualisasi
st.subheader('Hourly Sharing')
plot_hourly_sharing()
st.write('Jumlah rata-rata peminjaman sepeda tertinggi adalah pada pukul 17.00 dan pada pukul 18.00')

st.subheader('Seasonal Sharing')
plot_seasonal_sharing()
st.write('Jumlah peminjaman sepeda paling banyak terjadi pada musim gugur')

st.subheader('Daily Sharing')
plot_daily_sharing()
st.write('Pada Weekdays waktu yang memiliki jumlah peminjaman sepeda paling banyak adalah pada pukul 08.00 dan 17.00, sedangkan pada Weekend, jumlah peminjaman sepeda paling banyak adalah pada siang hari sekitar pukul 12.00 - 16.00')

st.subheader('Weather Condition Sharing')
plot_weather_sharing()
st.write('Jumlah peminjaman sepeda paling banyak adalah saat kondisi cuaca cerah')

st.caption('Copyright (c) Dhissa Ashila 2024')