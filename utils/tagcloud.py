import ast
from backend.service import SolrService
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from pathlib import Path
from backend.solr import (
    SolrDocuments,
    config
)
import os
from os import path


def update_tagcloud():
    solrservice = SolrDocuments(config.documents_solr)
    q_keywords = solrservice.search("*:*", fl='keywords')
    docs = q_keywords.docs
    all_keywords =[]

    for dictionaries in docs:
        for keywords,list_values in dictionaries.items():
            for list_contents in list_values:
                convert_dictionary = ast.literal_eval(list_contents)
                all_keywords.append(convert_dictionary['value'])

    distinct = list(dict.fromkeys(all_keywords))
    string = " ".join(str(x) for x in distinct)
    print(string)

    wordcloud = WordCloud(width=1200 , height=700,max_font_size=100, max_words=1000,
                          background_color="white").generate(string)

    #TODO: Save image in the Assets folder so it can be updated everytime
    #path_to_save = r"..\..\frontend\src\assets\img"
    plt.figure()
    plt.axis("off")
    plt.imshow(wordcloud, interpolation="bilinear")
    #wordcloud.to_file(path.join(path_to_save,"tag_cloud.png"))
    wordcloud.to_file("tag_cloud.png")

