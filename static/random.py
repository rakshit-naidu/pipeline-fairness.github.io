import pandas as pd
from bs4 import BeautifulSoup

html_text = """
<!DOCTYPE html>
<html>
<head>
	<title>DATA COLLECTION : ANNOTATION</title>
	<style>
		.post-container {
    margin: 20px 20px 0 0;  
    border: 5px solid #333;
    overflow: auto
}
.post-thumb {
    float: left
}
.post-thumb img {
    display: block;
    width: 200px;
    height: auto;
}
.post-content {
    margin-left: 210px
}
.post-title {
    font-weight: bold;
    font-size: 200%;
    padding: 9px;
    background: #ccc
}

.tabs {
  margin-top: 20px;
}

.tabs ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: space-between;
}

.tabs li {
  flex: 1;
  text-align: center;
}

.tabs li a {
  display: block;
  padding: 10px;
  background-color: #f2f2f2;
  color: #333;
  text-decoration: none;
  border: 1px solid #ccc;
  border-bottom: none;
}

.tabs li.active a {
  background-color: #fff;
  border-color: #ccc;
}

.tab-content {
  display: none;
}

.tab-content.active {
  display: block;
}

.tab-content table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1px;
}

.tab-content table th,
.tab-content table td {
  padding: 5px;
  text-align: center;
  border: 1px solid #ccc;
}
	</style>
</head>
<body>

	

  <div class="post-container">
    <h3 class="post-title">DATA COLLECTION : ANNOTATION</h3>
    <div class="post-thumb"><img src="/static/floppy.png" alt="DATA COLLECTION"/></div>
    <div class="post-content">
        <p>Collecting or compiling data to train the model. This involves making choices—or implicitly
          accepting previously made choices—about how to sample, label, link, and omit data. Some questions include—
          What population will we sample to build our model? How will we collect this data? How will we measure our
          prediction task? How will we define a positive label based on the prediction task? Who will label our data? How
          will we link across data sources?</p>
    </div>
  </div>
    <div class="tabs">
      <ul>
        <li><a href="#casestudy">Case Study</a></li>
        <li><a href="#problemidentification">Problem Identification</a></li>
        <li><a href="#measurement">Measurement</a></li>
        <li><a href="#mitigation">Mitigation</a></li>
      </ul>
      <div class="tab-content" id="casestudy">
        <table>
          <thead>
            <tr>
              <th>Paper Title</th>
              <th>Authors</th>
              <th>Description</th>
              <th>Tags/Comments</th>
              <th>Conference Venue</th>
              <th>Year</th>
              <th>Paper link</th>
              <th>Additional resources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Learning with Noisy Labels Revisited: A Study Using Real-World Human Annotations</td>
              <td>Jiaheng Wei, Zhaowei Zhu, Hao Cheng, Tongliang Liu, Gang Niu, Yang Liu</td>
              <td>N/A</td>
              <td>Data Sampling, Case Study</td>
              <td>ICLR</td>
              <td>2022</td>
              <td><a href="https://openreview.net/forum?id=TBWA6PLJZQm">Learning with Noisy Labels Revisited</a></td>
              <td>None</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="tab-content" id="problemidentification">
        <table>
          <thead>
            <tr>
              <th>Paper Title</th>
              <th>Authors</th>
              <th>Description</th>
              <th>Tags/Comments</th>
              <th>Conference Venue</th>
              <th>Year</th>
              <th>Paper link</th>
              <th>Additional resources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Fair Classification with Group-Dependent Label Noise</td>
              <td>Jialu Wang, Yang Liu, Caleb Levy</td>
              <td>N/A</td>
              <td>Data Collection, Annotation, Problem Identification</td>
              <td>FAccT</td>
              <td>2021</td>
              <td><a href="https://dl.acm.org/doi/10.1145/3442188.3445915">Fair Classification with Group-Dependent Label Noise</a></td>
              <td>None</td>
            </tr>
            <tr>
                <td>Assessing Annotator Identity Sensitivity via Item Response Theory: A Case Study in a Hate Speech Corpus</td>
                <td>Pratik S. Sachdeva, Renata Barreto, Claudia von Vacano, Chris J. Kennedy</td>
                <td>N/A</td>
                <td>Data Collection, Annotation, Problem Identification</td>
                <td>FAccT</td>
                <td>2022</td>
                <td><a href="https://dl.acm.org/doi/10.1145/3531146.3533216">Assessing Annotator Identity Sensitivity via Item Response Theory</a></td>
                <td>None</td>
              </tr>
            </tbody>
        </table>
      </div>
      <div class="tab-content" id="measurement">
        <table>
          <thead>
            <tr>
              <th>Paper Title</th>
              <th>Authors</th>
              <th>Description</th>
              <th>Tags/Comments</th>
              <th>Conference Venue</th>
              <th>Year</th>
              <th>Paper link</th>
              <th>Additional resources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Can Less be More? When Increasing-to-Balancing Label Noise Rates Considered Beneficial</td>
              <td>Yang Liu and Jialu Wang</td>
              <td>N/A</td>
              <td>Data Collection, Annotation, Measurement</td>
              <td>NeurIPS</td>
              <td>2021</td>
              <td><a href="https://proceedings.neurips.cc//paper/2021/hash/91e50fe1e39af2869d3336eaaeebdb43-Abstract.html">Can Less be More?</a></td>
              <td>None</td>
            </tr>
            <tr>
                <td>Measuring Representational Harms in Image Captioning</td>
                <td>Angelina Wang, Solon Barocas, Kristen Laird, Hanna Wallach</td>
                <td>N/A</td>
                <td>Data Collection, Annotation, Measurement</td>
                <td>FAccT</td>
                <td>2022</td>
                <td><a href="https://dl.acm.org/doi/10.1145/3531146.3533099">Measuring Representational Harms in Image Captioning</a></td>
                <td>None</td>
              </tr>
          </tbody>
        </table>
      </div>
      <div class="tab-content" id="mitigation">
        <table>
          <thead>
            <tr>
              <th>Paper Title</th>
              <th>Authors</th>
              <th>Description</th>
              <th>Tags/Comments</th>
              <th>Conference Venue</th>
              <th>Year</th>
              <th>Paper link</th>
              <th>Additional resources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Towards fairer datasets: filtering and balancing the distribution of the people subtree in the ImageNet hierarchy</td>
              <td>Kaiyu Yang, Klint Qinami, Li Fei-Fei, Jia Deng, Olga Russakovsky</td>
              <td>N/A</td>
              <td>Data Collection, Annotation, Mitigation</td>
              <td>FAccT</td>
              <td>2020</td>
              <td><a href="https://dl.acm.org/doi/10.1145/3351095.3375709">Towards fairer datasets</a></td>
              <td>None</td>
            </tr>
          </tbody>
        </table>
    </div>
  </div>
    
    <!-- JavaScript for the tabs -->
    <script>
      const tabLinks = document.querySelectorAll('.tabs li a');
      const tabContents = document.querySelectorAll('.tab-content');

      tabLinks.forEach((link) => {
        link.addEventListener('click', (e) => {
          e.preventDefault();

          const targetId = e.target.getAttribute('href').substr(1);

          tabLinks.forEach((link) => {
            link.parentNode.classList.remove('active');
          });

          tabContents.forEach((content) => {
            content.classList.remove('active');
          });

          e.target.parentNode.classList.add('active');
          document.getElementById(targetId).classList.add('active');
        });
      });
    </script>
  </body>
</html>
"""

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
table = soup.find('table')

# Use pandas to read the table into a DataFrame
df = pd.read_html(str(table))[0]

# Print the resulting DataFrame
print(df)