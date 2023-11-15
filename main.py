import os
import collections
import json
import copy

from markdown_it import MarkdownIt
from mdit_plain.renderer import RendererPlain
import regex
import wordcloud
import matplotlib
import pkuseg
from pypinyin import lazy_pinyin

# get all markdown files
file_list: list[str] = []
for filepath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        if filename.endswith(".md"):
            file_list.append(os.path.join(filepath, filename))

# read sentences
sentence_list: list[str] = []
pattern = regex.compile("\\p{Han}+")
parser: MarkdownIt = MarkdownIt(renderer_cls=RendererPlain)
for file in file_list:
    plain_data: str = parser.render(open(file, "r").read())
    sentences = plain_data.split("\n")
    for sentence in sentences:
        if pattern.search(sentence):
            sentence_list.append(sentence)

# read common worlds
common_word_lines = open("现代汉语常用词表.txt","r").readlines()
common_word_set: set[str] = set()
for common_word_line in common_word_lines:
    common_word_set.add(pattern.findall(common_word_line)[0])

# cut sentences
seg = pkuseg.pkuseg(model_name="default_v2") # download from https://github.com/lancopku/pkuseg-python/releases/download/v0.0.25/default_v2.zip
word_dict: dict[str, int] = collections.defaultdict(int)
for sentence in sentence_list:
    sentence2 = regex.sub("\\p{P}+", " ", sentence).strip()
    # word_list = jieba.cut(sentence2, cut_all=True, use_paddle=True)
    word_list = seg.cut(sentence2)
    for word in word_list:
        word2 = regex.sub("\\s+", " ", word)
        if len(word2) > 1 and word2 not in common_word_set and pattern.match(word2):
            word_dict[word2] += 1

# build wordcloud
build_wordcloud = False;

if build_wordcloud:
    colormap = matplotlib.colors.ListedColormap(["#5BCEFA", "#F5A9B8", "#2D2D2D", "#9B59D0", "#FFF433"])
    w = wordcloud.WordCloud(width=1920, height=1080, font_path="sarasa-ui-tc-regular.ttf", background_color="#7f7f7f", colormap=colormap)
    w.generate_from_frequencies(word_dict)
    w.to_file("result.png")

# build dict
word_list = sorted(word_dict.items(), key=lambda kv: kv[1], reverse=True)
open("result.json", "w", encoding="utf8").write(json.dumps(word_list, ensure_ascii=False))

#build rime dict
rime_dict_str = """---
name: project_trans
version: "0.1"
sort: by_weight
...

"""
rime_dict_pinyin_str = copy.deepcopy(rime_dict_str)

pinyin_pattern = regex.compile("(\\w|\\s)+")
for word in word_list:
    pinyin = " ".join(lazy_pinyin(word[0]))
    if pinyin_pattern.fullmatch(pinyin):
        word_str = word[0]
        word_str += "\t"
        word_str += pinyin
        word_str += "\t"
        word_str += str(word[1])
        word_str += "\n"
        rime_dict_str += word_str

        word_str_pinyin = word[0]
        word_str_pinyin += "\t\t"
        word_str_pinyin += str(word[1])
        word_str_pinyin += "\n"
        rime_dict_pinyin_str += word_str_pinyin

open("project_trans.dict.yaml", "w", encoding="utf8").write(rime_dict_str)
open("project_trans_pinyin.dict.yaml", "w", encoding="utf8").write(rime_dict_pinyin_str)
