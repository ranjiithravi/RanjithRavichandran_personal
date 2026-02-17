"""
A script to calculate chit related numbers
Author: Ranjith Ravichandran
Created: 17 Feb 2026
"""

import pandas as pd
from datetime import date
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

chit_start = date(2025, 7, 10)
chit_duration = 20 # 20 months
chit_end = chit_start + pd.DateOffset(months=chit_duration)

print('chit start:', chit_start)
print('chit end:', chit_end)

current_date = date.today()
current_month = date(current_date.year, current_date.month, 1)
current_month = current_month.strftime("%b %Y")
print('current month:', current_month)

chit_amounts_soFar = [37400, 37600, 38250, 39200, 39300,
                      39750, 40500, 41150] # amounts paid so far

def list_months_years_pandas(start_date, end_date):
    """Generates a list of 'Month Year' strings using pandas date_range."""
    # Generate a range of dates with 'ME' frequency (Month End)
    date_range = pd.date_range(start=start_date, end=end_date, freq='ME')
    # Format the dates into "Month Year" strings
    return date_range.strftime("%b %Y").tolist()


def chit_amount_prediction(paid_amounts, chit_full_duration):
    """Calculates chit amount prediction based on linear extrapolation from amounts paid so far"""
    paid_months = np.arange(1, len(paid_amounts) + 1)
    future_months = np.arange(len(paid_months)+1, chit_duration+1, 1)
    total_months = np.concatenate((paid_months, future_months))

    fit = interp1d(paid_months, paid_amounts, kind='linear', fill_value='extrapolate')

    return fit(total_months)

chit_months = list_months_years_pandas(chit_start, chit_end)
# print('list of chit months:', chit_months)

chit_amounts_fullDuration = chit_amount_prediction(chit_amounts_soFar, chit_duration)

# print chit amounts for each month
for i in range(len(chit_months)):
    chit_month = chit_months[i]
    chit_amount = chit_amounts_fullDuration[i]
    print('chit month:', chit_month, '--> chit amount:', chit_amount)

# plot for comparison
plt.figure(figsize=(12, 8))
plt.scatter(chit_months[0:len(chit_amounts_soFar)], chit_amounts_soFar, color='k', label='actual amount paid so far')
plt.plot(chit_months, chit_amounts_fullDuration, color='red', label='full duration extrapolated')
plt.axvline(x=current_month, color='k', linestyle='--', label='current month')
plt.legend()
plt.title("Chit amount")
plt.xlabel("Months")
plt.ylabel("Amount in INR")
plt.grid(True)
plt.show()
