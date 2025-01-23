
from llm_engine.functions import get_tables_from_html

# Opening the html file
files: list = ["pr-19181588-docusign-announces-fourth-quarter-and-fiscal-year-2023-financial-results.html"
    ,"pr-19218897-gamestop-reports-fourth-quarter-and-fiscal-year-2022-results.html"
    ,"pr-19197623-lennar-reports-first-quarter-2023-results.html"
    ,"pr-19218951-nike-inc-reports-fiscal-2023-third-quarter-results.html"
    ,"pr-19201467-adobe-reports-record-revenue-in-q1-fiscal-2023.html"
    ,"pr-19220586-shoe-carnival-reports-fourth-quarter-and-fiscal-2022-results.html"
    ,"pr-19203115-dollar-general-corporation-reports-fourth-quarter-and-fiscal-year-2022-results.html"
    ,"pr-19220702-winnebago-industries-reports-second-quarter-fiscal-2023-results.html"
    ,"pr-19205259-fedex-corp-reports-third-quarter-results.html"
    ,"pr-19220732-petco-health-wellness-company-inc-reports-fourth-quarter-and-full-year-2022-earnings-issues.html"
    ,"pr-19207045-xpeng-reports-fourth-quarter-and-fiscal-year-2022-unaudited-financial-results.html"
     "pr-19316190-harsco-corporation-reports-first-quarter-2023-results.html"]
path: str = f"/home/diman82/Documents/git/python/openai-pr-summarization/test/resources/pr_tables/{files[6]}"

content: str = open(path, "r").read()

list_tables: list = get_tables_from_html(content, filter_criteria = 'diluted earnings')
table_delimiter: str = "\n\n".join(list_tables)
print(f"table_delimiter: {table_delimiter}")

