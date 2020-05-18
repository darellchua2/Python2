import bs4 as bs
import urllib.request
import csv
import requests
from PIL import Image
from io import BytesIO
import os
import pandas as pd
import re



def CreateFolder(folder_name):
    try:
        os.mkdir(folder_name)
    except OSError:
        print ("Creation of the directory '%s' failed, the file already exist" % folder_name)


def DownloadImage(url,filename,ext = "png"):
    createFolder(("downloads"))
    output_filename = filename + "." + ext
    urllib.request.urlretrieve(url, output_filename)
    response = requests.get(url)
    name = f"test.png"
    filename = f"./downloads/{name}"
    img = Image.open(BytesIO(response.content))
    img.save(filename)
    img = ""


def OutputHTMLFileSummary(url,html_tag,output_file):
    a = []
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'html.parser')
    # print(soup.encode("utf-8"))
    f = csv.writer(open(output_file, "w", encoding="utf-8"))
    links = soup.find_all(html_tag)
    counter = 0.0
    for link in links:
        counter +=1
        print(link)
        f.writerow([str(link)])

def OutputHTMLFileSummaryIMG(url,html_tag,output_file):
    a = []
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'html.parser')
    # print(soup.encode("utf-8"))
    f = csv.writer(open(output_file, "w", encoding="utf-8"))
    links = soup.find_all(html_tag)
    for link in links:
        print(link)
        if link == a:
            pass
        else:
            f.writerow([link.name, link.title, link["src"], link.text, str(link)])


url1 = 'https://yugipedia.com/wiki/Set_Card_Lists:Deck_Build_Pack:_Mystic_Fighters_(OCG-JP)'
url2 = 'https://yugipedia.com/wiki/Set_Card_Galleries:Deck_Build_Pack:_Mystic_Fighters_(OCG-JP)'
url3 = 'https://yugipedia.com/wiki/Mathmech_Sigma'
#
# html_tag = "tr"
output_file1 = "DBMF - CardList - tr1.csv" #change this to your own file output
output_file2 = "DBMF - Card - MathMech - a.csv" #change this to your own file output
output_file6 = "DBMF - CardList - tr1.csv" #change this to your own file output
output_file7 = "DBMF - CardGallery - img.csv" #change this to your own file output
output_file1_2 = "DBMF - CardList - tr2.csv" #change this to your own file output


def OutputCardList(url,html_tag,output_file,sub_tag):
    lists = []
    counter = 0
    df = pd.DataFrame(columns = ("CODE","Card Name","Card Name(Japanese)", "Rarity","Card Type","Status"))
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'html.parser')
    f = csv.writer(open(output_file, "w", encoding="utf-8"))
    links = soup.find_all(html_tag)
    for link in links:
        counter += 1
        lists.append([f.text.strip().replace("\xa0\n\t", "") for f in link.find_all(sub_tag)])
    for i in range(len(lists)):
        if i/2 != 0 and i>1:
            lists[i][1] = lists[i][1].strip('"')
            df.loc[i] = lists[i]
            df.to_csv(output_file)
    print(df)
    return df

# df1 = OutputCardList(url1,"tr",output_file6,"td")

def OutputCardGallery(url,html_tag,output_file,check_string):
    df = pd.DataFrame(columns = ("Card Name","Card URL"))
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'html.parser')
    f = csv.writer(open(output_file, "w", encoding="utf-8"))
    links = soup.find_all(html_tag)
    counter = 0
    for i in range(len(links)):
        # print(type(tag["src"]))
        img_src = links[i]["src"]
        if check_string in img_src:
            img_src = img_src.replace('/thumb','')
            img_src_splitlist = img_src.rsplit('/',2)
            card_name = img_src_splitlist[1].split('-',1)
            card_name[0] = re.sub(r"(\w)([A-Z])", r"\1 \2", card_name[0])
            new_list = [card_name[0],img_src_splitlist[0] + "/" + img_src_splitlist[1]]
            print(new_list)
            df.loc[counter] = new_list
            counter += 1
    df.to_csv(output_file)
    print(df)
    return df

# df2 = OutputCardGallery(url2,"img",output_file7,"DBMF")
#
# df_new = pd.merge(df1,df2,on = ["Card Name"])
# df_new.to_csv("OVERALL.CSV")

OutputHTMLFileSummary(url3,"a",output_file2)

