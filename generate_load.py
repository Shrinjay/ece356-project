import pandas as pd
import os
import io

csvs = os.listdir('./full_history')
financial_csvs = os.listdir('./archive')

financial_df_cols = [
    'Year',
    'Revenue',
    'Revenue Growth',
    'Cost of Revenue',
    'Gross Profit',
    'R&D Expenses',
    'SG&A Expense',
    'Operating Expenses',
    'Operating Income',
    'Interest Expense',
]

financial_df = pd.DataFrame(data={
    'Year': [],
    'Revenue': [],
    'Growth': [],
    'Revenue Growth': [],
    'Cost Of Revenue': [],
    'Gross Profit': [],
    'R&D Expenses': [],
    'SG&A Expenses': [],
    'Operating Expenses': [],
    'Operating Income': [],
    'Interest Expense': [],
})

insert_f_per_stock = {}

for filename in financial_csvs:
    df = pd.read_csv(os.path.join(os.getcwd(), 'archive', filename), index_col=0)
    year = filename.split('_')[0]
    df['Year'] = year
    financial_df = pd.concat([financial_df, df])
    financial_df = financial_df[financial_df_cols]
    financial_df = financial_df.dropna()


id = 1
csv_len = len(csvs)

insert_per_stock = []
outfile = io.open("load2.sql", "w")

for filename in csvs:
    trading_df = pd.read_csv(os.path.join(os.getcwd(), 'full_history', filename))

    ticker = filename.split('.')[0]

    insert_commands = [f"INSERT INTO Stock (ID, Symbol) VALUES({id}, '{ticker}');"]

    financial_df_for_stock = financial_df[financial_df.index == ticker]

    for _, row in trading_df.iterrows():
        date = row['date']
        volume = row['volume']
        open = row['open']
        high = row['high']
        low = row['low']
        close = row['close']
        adjclose = row['adjclose']

        insert_trade = f"""
INSERT INTO TradingData
    (stockID, `Date`, Volume, `Open`, High, Low, `Close`, AdjustedClose)
    VALUES({id}, STR_TO_DATE('{date}', '%Y-%m-%d'), {volume}, {open}, {high}, {low}, {close}, {adjclose});"""

        insert_commands.append(insert_trade)

    for _, row in financial_df_for_stock.iterrows():
        year = row['Year']
        revenue = row['Revenue']
        revenue_growth = row['Revenue Growth']
        cost_of_revenue = row['Cost of Revenue']
        gross_profit = row['Gross Profit']
        rd_expenses = row['R&D Expenses']
        sga_expenses = row['SG&A Expense']
        opex = row['Operating Expenses']
        operating_income = row['Operating Income']
        interest_expense = row['Interest Expense']

        insert_fin = f"""
        INSERT INTO FinancialData
        (stockID, `Year`, Revenue, RevenueGrowth, CostofRevenue, GrossProfit, RDExpenses, SGAExpenses, OperatingExpenses, OperatingIncome, InterestExpense)
        VALUES({id}, {year}, {revenue}, {revenue_growth}, {cost_of_revenue}, {gross_profit}, {rd_expenses}, {sga_expenses}, {opex}, {operating_income}, {interest_expense});
        """

        insert_commands.append(insert_fin)

    insert_commands.append('\n')

    insert_statements = '\n'.join(insert_commands)
    outfile.write(insert_statements)

    id += 1

    print(f"Generated {ticker}, {id}/{csv_len}")

outfile.close()


