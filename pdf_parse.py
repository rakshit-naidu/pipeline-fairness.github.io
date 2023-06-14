import PyPDF2
import tabula

file_path = "Toward_a_pipeline_centric_view_of_Fairness_for_ML__A_Research_Agenda.pdf"

with open(file_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)

extracted_tables = []

for page_number in range(num_pages):
    tables = tabula.read_pdf(file_path, pages=page_number+1, multiple_tables=True)
    extracted_tables.extend(tables)

table_index = 0  # Select the desired table by its index
row_index, column_index = 0, 0

data_frame = extracted_tables[table_index]
cell_value = data_frame.iloc[row_index, column_index]

print(cell_value)