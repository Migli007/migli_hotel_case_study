import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing


excel_file = r"C:\Users\migli\OneDrive\Desktop\ihg_file\ihg_data.xlsx"
df = pd.read_excel(excel_file, sheet_name='METRICS')  

# Filter hotel 
df_ukpil = df[df['HTL_CD'] == 'EXIUS']

df['STY_DT'] = pd.to_datetime(df['STY_DT'])
df_ukpil = df_ukpil.sort_values(by='STY_DT')

# Set the 'STY_DT' as index
df_ukpil.set_index('STY_DT', inplace=True)
df_ukpil_monthly_revenue = df_ukpil['RM_REV_AMT_LOC'].dropna()

# Simple Holt-Winters method
model = ExponentialSmoothing(df_ukpil_monthly_revenue, trend='add', seasonal='add', seasonal_periods=12)
model_fit = model.fit()

# Forecasting future months
forecast = model_fit.forecast(steps=3)

# Create the future dates for the forecast
forecast_dates = pd.date_range(df_ukpil_monthly_revenue.index[-1], periods=4, freq='M')[1:]

# historical data and the forecasted revenue
plt.figure(figsize=(10, 6))

plt.plot(df_ukpil_monthly_revenue, label='Historical Revenue', color='green')
plt.plot(forecast_dates, forecast, label='Forecasted Revenue', color='orange', linestyle='--')
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
plt.gcf().autofmt_xdate()  

# chart description
plt.title('Revenue Forecast for EXIUS Hotel')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.legend()


plt.show()
print(forecast)
