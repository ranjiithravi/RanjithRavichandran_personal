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

plot_fig = True
capital_amount = 1000000
commission_amount = 50000
chit_start = date(2025, 7, 10)
chit_duration = 20 # 20 months
monthly_amount = capital_amount/chit_duration
chit_end = chit_start + pd.DateOffset(months=chit_duration)
print('chit start:', chit_start)
print('chit end:', chit_end)

current_date = date.today()
current_month = date(current_date.year, current_date.month, 1)
current_month = current_month.strftime("%b %Y")
print('current month:', current_month)

chit_amounts_soFar = [37400, 37600, 38250, 39200, 39300,
                      39750, 40500, 41150] # amounts paid so far

dtype = [('month', 'U20'), ('amount', 'f4')]
chit_history = np.array([('Jul 2025', 37400), ('Aug 2025', 37600), ('Sep 2025', 38250), ('Oct 2025', 39200), ('Nov 2025', 39300),
                         ('Dec 2025', 39750), ('Jan 2026', 40500), ('Feb 2026', 41150), ('Mar 2026', np.nan), ('Apr 2026', np.nan),
                         ('May 2026', np.nan), ('Jun 2026', np.nan), ('Jul 2026', np.nan), ('Aug 2026', np.nan), ('Sep 2026', np.nan),
                         ('Oct 2026', np.nan), ('Nov 2026', np.nan), ('Dec 2026', np.nan), ('Jan 2027', np.nan), ('Feb 2027', 50000)], dtype=dtype)


def list_months_years_pandas(start_date, end_date):
    """Generates a list of 'Month Year' strings using pandas date_range."""
    # Generate a range of dates with 'ME' frequency (Month End)
    date_range = pd.date_range(start=start_date, end=end_date, freq='ME')
    # Format the dates into "Month Year" strings
    return date_range.strftime("%b %Y").tolist()


def chit_amount_prediction(paid_amounts, chit_full_duration):
    """Calculates chit amount prediction based on linear extrapolation from amounts paid so far"""
    paid_months = np.arange(1, len(paid_amounts) + 1)
    future_months = np.arange(len(paid_months)+1, chit_full_duration+1, 1)
    total_months = np.concatenate((paid_months, future_months))

    fit = interp1d(paid_months, paid_amounts, kind='linear', fill_value='extrapolate')

    return fit(total_months)


def direct_interestCalc(net_amount, draw_month, chit_full_duration, rate):
    """Calculate direct interest"""
    rem_months = chit_full_duration - draw_month
    interest = net_amount*rate/12*rem_months

    return interest

def cumulative_interestCalc(capitals, net_amount, draw_month, chit_full_duration, rate):
    """Calculate interest for decreasing capital after chit withdrawal"""
    rem_months = chit_full_duration-draw_month
    interest_cum = 0
    for i in np.arange(rem_months):
        interest = net_amount*rate/12
        # print(net_amount, interest)
        net_amount = net_amount - capitals[draw_month + i]

        interest_cum += interest

    return interest_cum

def cumulative_interestCalc_fullCapital(capital, monthly_chit, draw_month, chit_full_duration, rate):
    """Calculate interest for decreasing capital after chit withdrawal"""
    rem_months = chit_full_duration-draw_month
    interest_cum = 0
    for i in np.arange(rem_months):
        interest = capital*rate/12
        # print(f'month {draw_month+i}: capital {capital}, interest {interest}')
        capital = capital - monthly_chit

        interest_cum += interest

    return interest_cum

def cumulative_interestCalc_deposit(monthly_chit, chit_full_duration, rate):
    """Calculate bank deposit interest for monthly contributions"""
    interest_cum = 0
    capital = monthly_chit
    for i in np.arange(chit_full_duration):
        interest = capital*rate/12
        # print(f'month {i+1}: capital {capital}, interest {np.round(interest, 1)}')
        capital = capital + monthly_chit

        interest_cum += interest

    return interest_cum


# chit_months = list_months_years_pandas(chit_start, chit_end)
# print('list of chit months:', chit_months)

chit_months = chit_history['month']
chit_amounts = pd.Series(chit_history['amount'])

# chit_amounts_fullDuration = chit_amount_prediction(chit_amounts_soFar, chit_duration)
chit_amounts_fullDuration = chit_amounts.interpolate(method='linear')

# print chit amounts for each month
for i in range(len(chit_months)):
    chit_month = chit_months[i]
    chit_amount = chit_amounts_fullDuration[i]
    print('chit month:', chit_month, '--> chit amount:', chit_amount)

print()
print('====================================================')
print('========= calculate profit related numbers =========')
print('====================================================')
print()

draw_month = 20
print(f'chit amount paid for {draw_month}th month ({chit_months[draw_month-1]}): {chit_amounts_fullDuration[draw_month-1]}')
accrued_capital = sum(chit_amounts_fullDuration[0:draw_month])
print(f'accrued capital at {draw_month}th month: {accrued_capital}')

less_amount = capital_amount - (chit_amounts_fullDuration[draw_month-1]*chit_duration) + commission_amount
drawn_capital = capital_amount - less_amount
print(f'less amount when drawing at {draw_month}th month: {less_amount}')
print(f'drawn capital when drawing at {draw_month}th month: {drawn_capital}')

total_amount_paid = sum(chit_amounts_fullDuration)
difference_capital = drawn_capital - total_amount_paid
print(f'total amount paid at the end of chit duration (all months): {total_amount_paid}')
print(f'difference in capital (drawn - amount paid all months): {difference_capital}')

# net_capital = drawn_capital - accrued_capital
# print(f'net capital when drawn at {draw_month}th month: {net_capital}')

# cumulative_interest = cumulative_interestCalc(chit_amounts_fullDuration, drawn_capital, draw_month, chit_duration, 0.24)
# print(f'cumulative interest: {cumulative_interest}')

cumulative_interest_fullCapital = cumulative_interestCalc_fullCapital(capital_amount, monthly_amount, draw_month, chit_duration, 0.24)
print(f'cumulative interest full capital: {cumulative_interest_fullCapital}')

cumulative_deposit_interest = cumulative_interestCalc_deposit(monthly_amount, chit_duration, 0.07)
print(f'cumulative deposit interest: {cumulative_deposit_interest}')

# direct_interest = direct_interestCalc(drawn_capital, draw_month, chit_duration, 0.24)
# print(f'direct interest: {direct_interest}')

net_profit = difference_capital + cumulative_interest_fullCapital - cumulative_deposit_interest
print(f'net profit: {net_profit}')

# plot for comparison
if plot_fig:
    plt.figure(figsize=(12, 8))
    # plt.scatter(chit_months[0:len(chit_amounts_soFar)], chit_amounts_soFar, color='k',
    plt.scatter(chit_months, chit_amounts, color='k',
                label='actual amount paid so far')
    plt.plot(chit_months, chit_amounts_fullDuration, color='red', label='full duration extrapolated')
    plt.axvline(x=current_month, color='k', linestyle='--', label='current month')
    plt.legend()
    plt.title("Chit payment history")
    plt.xlabel("Months")
    plt.ylabel("Amount in INR")
    plt.grid(True)
    plt.show()
