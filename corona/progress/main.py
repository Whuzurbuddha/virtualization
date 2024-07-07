import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

import sys
sys.path.append('/home/alexander/devel/python')
from database_access import data_handler


class Database:
    def __init__(self):
        filepath = data_handler.Data.path
        data = data_handler.read_json(filepath)
        self.connection = mysql.connector.connect(
            host=data["host"],
            port=data["port"],
            user=data["user"],
            password=data["password"],
            database="corona"
        )

    def execute_sql(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result


def get_data():
    db = Database()
    query = "select * from robert_koch_institut_corona_verlauf order by LAST_UPDATE;"
    data = db.execute_sql(query)
    return data


def add_cases_plot(data):
    plt.style.use('ggplot')

    date = [entry[0] for entry in data]
    cases = [entry[3] for entry in data]
    deaths = [entry[5] for entry in data]

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 8))

    # Plotting the bar chart for cases on the first subplot
    ax1.bar(date, cases, width=0.5, color='skyblue', edgecolor='darkblue', linewidth=0.7, label='Cases')
    ax1.set_ylabel('Cases per 100k')
    ax1.set_title('COVID-19 Cases and Deaths Over Time')
    ax1.legend()

    # Plotting the line chart for deaths on the second subplot
    ax2.plot(date, deaths, color='red', linewidth=2, label='Deaths')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Deaths')
    ax2.legend()

    # Formatting the date axis
    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m.%Y'))
    plt.xticks(rotation=45)

    # Setting y-axis ticks to avoid overlap
    ax2.yaxis.set_major_locator(MaxNLocator(prune='lower', nbins=10))

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    add_cases_plot(get_data())
