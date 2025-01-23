from bs4 import BeautifulSoup



def removeTable(soup: BeautifulSoup):
    for table in soup.find_all("table"):
        table.extract()

def getTextFromHTML(soup: BeautifulSoup) -> list:
    lst: list = []
    for tag in soup.find_all():
        if tag.name in ('p', 'li'):
            for arg in tag.contents:
                if arg.name in ("br", "a", "span"):
                    continue
                else:
                    lst.append(arg)
    return lst

def getCleanText(lst: list) -> list:
    cleanList = []
    for line in lst:
        txt: str = line.text.strip()
        if txt in ("",",",".",":",";",".\n","\n") or \
                any(txt.lower().startswith(x) for x in ["e-mail", "telephone", "table", "chart", "photo", "contacts"]):
            continue
        if txt.lower().startswith("about"):
            break
        else:
            cleanList.append(txt)
    return cleanList

path = "/home/diman82/Documents/git/python/openai-pr-summarization/test/resources/Executive_Announcements/Laxman_Narasimhan.html"
HTMLFile = open(path, "r")

# Reading the file
index = HTMLFile.read()

# Creating a BeautifulSoup object and specifying the parser
soup: BeautifulSoup = BeautifulSoup(index, 'lxml')

removeTable(soup)
lst: list = getTextFromHTML(soup)
# lst = [lst[-7],lst[-6],lst[-5],lst[-4],lst[-3],lst[-2],lst[-1]]
cleanList: list = getCleanText(lst)

print(cleanList)
print('\n'.join(cleanList))