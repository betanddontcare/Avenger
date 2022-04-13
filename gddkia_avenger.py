import requests, datetime, threading
from bs4 import BeautifulSoup
import pandas as pd

def giveMeIncidentsData():
    threading.Timer(1800, giveMeIncidentsData).start()
    start_url = "https://drogi.gddkia.gov.pl/informacje-drogowe/lista-utrudnien"
    download_html = requests.get(start_url)

    soup = BeautifulSoup(download_html.text, "html.parser") 
    with open('downloaded.html', 'w', encoding="utf-8") as file: file.write(soup.prettify())

    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    print(year, month, day, hour, minute)

    full_table = soup.select('table')[0]
    table_head = full_table.select('tr th')
    table_columns = ['Year', 'Month', 'Day', 'Hour', 'Minute']

    for element in table_head:
        column_label = element.get_text(separator=" ", strip=True)
        table_columns.append(column_label)

    table_rows = full_table.select('tr')
    table_data = []

    for index, element in enumerate(table_rows):
        if index > 0:
            row_list = [year, month, day, hour, minute]
            values = element.select('td')
            for value in values:
                if value['class'] == ['td8']:
                    img = value.select('img')
                    for i in img:
                        text = i['title']
                        text_a_split = text.split()
                        text_binded = " ".join(text_a_split)
                        row_list.append(text_binded)
                        break
                else:
                    row_list.append(value.text.strip())
            if row_list[7] == 'mazowieckie':
                table_data.append(row_list)

    df = pd.DataFrame(table_data, columns = table_columns)
    print(df)

    path = 'data.csv'

    save_to_file = open(path, 'a')
    save_to_file.write(df.to_csv(index=False))
    save_to_file.close()

giveMeIncidentsData()
