import re
import bibtexparser
import pandas as pd
from fuzzywuzzy import process
from pybtex.database import parse_file

def extract_bib_entries(file_path):
    with open(file_path, 'r') as file:
        bib_string = file.read()

    bib_entries = re.findall(r'@inproceedings{[^}]+}', bib_string)
    return bib_entries

def find_closest_match(target_string, string_list):
    closest_match, similarity = process.extractOne(target_string, string_list)
    print(similarity)
    return closest_match

# # Example usage
# target_string = "Hello"
# string_list = ["Hallo", "Hola", "Hey", "Hi"]
# closest_match = find_closest_match(target_string, string_list)
# print(f"The closest match to '{target_string}' is: {closest_match}")

def extract_paper_bib(bibtex_file, paper_id):
    with open(bibtex_file, 'r') as file:
        bib_database = bibtexparser.load(file)
        entries = bib_database.entries
        for entry in entries:
            if 'ID' in entry and entry['ID'] == paper_id:
                return entry
    return None

def extract_row_by_bib(dataframe, bib):
    # t = find_closest_match(title, dataframe['title'].tolist())
    # print(t)
    biblistt = dataframe['bibtex'].values.tolist()
    for b in biblistt:
        if bib == b:
            # result = dataframe[dataframe['bibtex'] == bib]
            result = dataframe.loc[dataframe['bibtex'] == b]
    
            return result

def find_bib_entry(file_path, identifier):
    with open(file_path, 'r') as file:
        bib_string = file.read()

    pattern = r'@inproceedings{' + identifier + r',[^}]+}'
    bib_entry = re.search(pattern, bib_string)
    print(bibtex_file)

    if bib_entry:
        return bib_entry.group()
    else:
        return None



def extract_citations(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        citations = re.findall(r'\\cite\{([^}]*)\}', content)
        return citations

# Example usage
file_path = 'table.txt'
citations = extract_citations(file_path)
print(citations)

classify_papers = {
    "va-cb": [0,0,0],
    "va-g": [3,2,0],
    "pf-pt": [4,0,1],
    "pf-pa": [1,0,0],
    "pf-g": [11,0,0],
    "dc-s": [5,2,6],
    "dc-a": [4,3,1],
    "dc-fm": [3,1,0],
    "dc-rl": [0,0,0],
    "dc-g": [6,9,3],
    "dp-fc": [0,0,0],
    "dp-fs": [4,2,3],
    "dp-dc": [0,2,4],
    "dp-g": [4,6,12],
    "sm-hc": [2,1,1],
    "sm-of": [4,1,15],
    "sm-r": [0,0,2],
    "sm-h": [1,0,5],
    "sm-g": [8,5,70],
    "tv-ts": [0,0,0],
    "tv-em": [5,18,12],
    "tv-g": [2,7,4],
    "di-hh": [9,1,1],
    "di-mo": [0,1,0],
    "di-g": [9,6,7]

}

stage_names = {
    "va-cb": "Viability Assessments-Cost/Benefit",
    "va-g": "Viability Assessments-General",
    "pf-pt": "Problem Formulation-Prediction Target",
    "pf-pa": "Problem Formulation-Predictive Attributes",
    "pf-g": "Problem Formulation-General",
    "dc-s": "Data Collection-Sampling",
    "dc-a": "Data Collection-Annotation",
    "dc-fm": "Data Collection-Feature Measurement",
    "dc-rl": "Data Collection-Record Linkage",
    "dc-g": "Data Collection-General",
    "dp-fc": "Data Preprocessing-Feature Creation",
    "dp-fs": "Data Preprocessing-Feature Selection",
    "dp-dc": "Data Preprocessing-Data Cleaning (Omission)",
    "dp-g": "Data Preprocessing-General",
    "sm-hc": "Statistical Modeling-Hypothesis Class",
    "sm-of": "Statistical Modeling-Optimization Function",
    "sm-r": "Statistical Modeling-Regularizers",
    "sm-h": "Statistical Modeling-Hyperparameters",
    "sm-g": "Statistical Modeling-General",
    "tv-ts": "Testing and Validation-Train-test split",
    "tv-em": "Testing and Validation-Evaluation Metrics",
    "tv-g": "Testing and Validation-General",
    "di-hh": "Deployment and Integration-Human/Computer Handoff",
    "di-mo": "Deployment and Integration-Maintenance Oversight",
    "di-g": "Deployment and Integration-General"
}

print(len(citations))

df = pd.read_csv("Pipeline Fairness Lit Review - Copy of Sheet1.csv")
columns = ["Paper Title", "Authors", "Description", "Tags/Comments", "Conference Venue", "Year", "Paper link", "Additional resources"]
new_df = pd.DataFrame(columns=columns)

i = 0

m = 0
cols = 0

bib_list = extract_bib_entries('refs.bib')
# print(bib_list)
for k in classify_papers:
    l = classify_papers[k]
    for j in range(len(l)):

        num = l[j]
        for ind in range(i, i+l[j]):
            id = citations[ind]

            bibtex_file = 'refs.bib'
            paper_id = id
            
            # Finding the bib entry in the file
            # bib = find_bib_entry(bibtex_file, paper_id)
            # print(bib)

            for b in bib_list:
                if paper_id in b:
                    x = find_closest_match(b, bib_list)
                    bib = x

            if bib:
                print(bib)
                # print(f"The bib of the paper '{paper_id}' is: {bib}")
                
                # exactbib = find_closest_match(bib, bib_list)

                row = extract_row_by_bib(df, bib)
                print(row)

                if cols % 3 == 0:
                    tags = stage_names[k] + ", Problem Identification"

                elif cols % 3 == 1:
                    tags = stage_names[k] + ", Measurement"


                elif cols % 3 == 2:
                    tags = stage_names[k] + ", Mitigation"

                if row is None:

                    print(f"No paper with the identifier '{paper_id}' was found.")
                    print("YOLOOOOOOO")

                    new_row = {
                        "Paper Title": "YOLOOOOOOO",
                        "Authors": "YOLOOOOOOO",
                        "Description": "Description 1",
                        "Tags/Comments": "Tags 1",
                        "Conference Venue": "Venue 1",
                        "Year": "YOLOOOOOOO",
                        "Paper link": "Link 1",
                        "Additional resources": "Resources 1"
                    }
                    new_df = new_df.append(new_row, ignore_index=True)
                    continue


                

                
                # row['title'] = row['title'].values
                # # row['authors'] = row['authors'].astype('str') 
                # row['conference'] = row['conference'].values
                # row['year'] = row['year'].values
                # row['link'] = row['link'].values

                # print(row)

                # print(type(row["conference"]))
                # print(type(row["title"]))
                # print(type(row["year"]))
                
                row = row.astype(str)

                new_row = {
                    "Paper Title": row["title"].to_string(index=False),
                    "Authors": row["authors"].values.tolist(),
                    "Description": "N/A",
                    "Tags/Comments": tags,
                    "Conference Venue": row["conference"].to_string(index=False),
                    "Year": row["year"].to_string(index=False),
                    "Paper link": row["link"].to_string(index=False),
                    "Additional resources": "N/A"
                }
                new_df = new_df.append(new_row, ignore_index=True)





            else:
                print(f"No paper with the identifier '{paper_id}' was found.")
                print("YOLOOOOOOO")

                new_row = {
                    "Paper Title": "YOLOOOOOOO",
                    "Authors": "YOLOOOOOOO",
                    "Description": "Description 1",
                    "Tags/Comments": "Tags 1",
                    "Conference Venue": "Venue 1",
                    "Year": "YOLOOOOOOO",
                    "Paper link": "Link 1",
                    "Additional resources": "Resources 1"
                }
                new_df = new_df.append(new_row, ignore_index=True)

            
            m += ind

        


        i += l[j]
        cols += 1

print(i)

new_df.to_csv("updated_table.csv")


