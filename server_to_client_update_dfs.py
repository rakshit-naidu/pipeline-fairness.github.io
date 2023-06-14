import pandas as pd
from bs4 import BeautifulSoup
# from google.colab import files

def get_df(html_text, save_file_name):

  # # Parse HTML text using Beautiful Soup
  # soup = BeautifulSoup(html_text, 'html.parser')

  # # Extract table data as list of lists
  # table_data = []
  # for row in soup.find_all('tr'):
  #     row_data = []
  #     for cell in row.find_all(['th', 'td', 'href']):
  #         row_data.append(cell.text.strip())
  #     table_data.append(row_data)

  # # Example list of lists with duplicates
  # my_list = table_data

  # # Create an empty set to keep track of unique lists
  # unique_set = set()

  # # Loop over each list in the original list of lists
  # for sublist in my_list:
  #     # Convert the sublist to a tuple, since lists are not hashable
  #     sublist_tuple = tuple(sublist)
  #     # Add the tuple to the set of unique tuples
  #     unique_set.add(sublist_tuple)

  # # Convert the set of unique tuples back to a list of lists
  # unique_list = [list(t) for t in unique_set]

  # # Print the resulting list of unique lists
  # print(unique_list)
  # # Convert table data to Pandas DataFrame
  # df = pd.DataFrame(unique_list[1:], columns=table_data[0])

  # # Print the resulting DataFrame
  # print(df)

  # Parse the HTML using BeautifulSoup
  soup = BeautifulSoup(html_text, 'html.parser')

  # Find the table element
  # table1 = soup.find(id="casestudy").find('table')
  table1 = soup.find(id="problemidentification").find('table')
  table2 = soup.find(id="measurement").find('table')
  table3 = soup.find(id="mitigation").find('table')

  print(table3)
  tables = [table1, table2, table3]
  # Use pandas to read the table into a DataFrame
  # df = pd.read_html(str(table))[0]

  # Print the resulting DataFrame
  # print(df)

  # assume the HTML table is stored in a variable called html_table

  # parse HTML using BeautifulSoup

  dfs = []

  for table in tables:
    # find the table and extract the header row and all data rows
    # table = soup.find('table')
    header_row = table.find('thead').find('tr')
    if table.find('tbody') is None:
      continue
    data_rows = table.find('tbody').find_all('tr')

    # extract the column headers from the header row
    headers = [header.text.strip() for header in header_row.find_all('th')]

    # initialize an empty list to store the table data
    table_data = []

    # iterate over the data rows, extract the cell values, and append to the table data list
    for row in data_rows:
        cell_values = [cell.text.strip() for cell in row.find_all('td')]
        # extract the paper link from the first cell using the href attribute
        link = row.find('a').get('href')
        cell_values.append(link)
        table_data.append(cell_values)

    # create a pandas dataframe from the table data and column headers
    # table_data['Paper link'] = 
    df1 = pd.DataFrame(table_data, columns=headers)
    dfs.append(df1)

  df_vertical = pd.concat(dfs, axis=0)

  return df_vertical


file_path = 'templates/datacollection/annotation.html'

with open(file_path, 'r') as file:
    file_contents = file.read()

file.close()

print(file_contents)

df1 = get_df(file_contents, "dc_annotation.csv")