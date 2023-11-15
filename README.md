# 跨儿计划 RIME 词典

## 语料

来源：

- [MtF.wiki](https://github.com/project-trans/MtF-wiki)
- [FtM.wiki](https://github.com/project-trans/FtM-wiki)
- [RLE.wiki](https://github.com/project-trans/RLE-wiki)
- [女性倾向跨性别者科学](https://github.com/project-trans/transfeminine-science)
- [中华人民共和国跨性别相关法律法规变迁](https://github.com/project-trans/legal-spec)

使用[pkuseg](https://github.com/lancopku/pkuseg-python)分词，[python-pinyin](https://github.com/mozillazg/python-pinyin)注音。

停用词：

- [现代汉语常用词表](https://gist.github.com/indiejoseph/eae09c673460aa0b56db)

## 仓库内容

去除停用词后包含一万余条记录。

1. 词频统计：`result.json`，JSON 格式，降序排列。
1. RIME 词典：包含除常用词表外的汉语词汇及词频，无编码，预构建文件位于仓库根目录下`project_trans.dict.yaml`，亦可在 Release 中获取。
1. RIME 词典：全拼编码，位于仓库根目录下`project_trans_pinyin.dict.yaml`。

软件源：

- [NUR](https://github.com/Cryolitia/nur-packages/blob/master/pkgs/rimePackages/rime-project-trans.nix)
- [AUR](https://aur.archlinux.org/packages/rime-project-trans-bin)

### 词云

#### 无停用词

![result_full](./result_full.png)

#### 停用常用词

![result](./result.png)
