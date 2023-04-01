'''
2023.3.22
宝可梦wiki爬虫,保存朱紫图鉴400只宝可梦序号+名称+属性到本地json文件
'''

import requests
from bs4 import BeautifulSoup
import json
import os

# 区分形态的几个例外宝可梦,这几个在网页里读第0,3,6个table,跳过其他地区形态,其他默认读第0,1,2个table
ex_pokemon = ["喵喵","肯泰罗"]

def table2json(table_soup, type) -> list:
    '''将爬取到的table转为list'''
    skill_list = []
    # 遍历行
    trs = table_soup.find_all("tr")
    # 遍历行中单元格
    for tr in trs:
        # 尾行不看
        if not tr.get("class") is None:
            if "sortbottom" in tr.get("class"):
                continue
        tds = tr.find_all("td")
        # 跳过表头
        if tds == []:
            continue
        # 通过升级
        if type == "lv":
            skill_list.append({
                # 第一格:等级/技能机编号/亲代
                "id": tds[0].text,
                # 第二格:技能名
                "name": tds[2].text,
                # 第三格:属性
                "type": tds[3].text,
                # 第四格:分类
                "cat": tds[4].text,
                # 第五格:威力
                "pwr": tds[5].text,
                # 第六格:命中率
                "acc": tds[6].text,
                # 第七格:PP
                "pp": tds[7].text
            })
        # 通过技能机
        elif type == "tm":
            skill_list.append({
                # 第一格:等级/技能机编号/亲代
                "id": tds[1].text,
                # 第二格:技能名
                "name": tds[2].text,
                # 第三格:属性
                "type": tds[3].text,
                # 第四格:分类
                "cat": tds[4].text,
                # 第五格:威力
                "pwr": tds[5].text,
                # 第六格:命中率
                "acc": tds[6].text,
                # 第七格:PP
                "pp": tds[7].text
            })
        # 通过野餐
        elif type == "bd":
            # print(table_soup.text)
            # with open("../test/tp.html", "w", encoding="utf-8") as f:
            #     f.write(table_soup.text)
            id = tds[0].find("span").get("data-msp") if tds[0].find("span") else tds[0].find("a").text
            skill_list.append({
                # 第一格:等级/技能机编号/亲代
                "id": id,
                # 第二格:技能名
                "name": tds[1].text,
                # 第三格:属性
                "type": tds[2].text,
                # 第四格:分类
                "cat": tds[3].text,
                # 第五格:威力
                "pwr": tds[4].text,
                # 第六格:命中率
                "acc": tds[5].text,
                # 第七格:PP
                "pp": tds[6].text
            })
    return skill_list


# 加载list.json中的宝可梦名
pokemon_list = []
with open("./list.json", "r", encoding="utf-8")as list_file:
    pokemon_list = json.load(list_file)

# 爬取到三个技能table
for pokemon in pokemon_list:
    name = pokemon["name"]
    id = pokemon["pd_id"]
    if os.path.isfile("./skill/%s.json" % name):
        print("pass : %s - %s" % (id, name))
        continue
    print("process : %s - %s ..." % (id, name))

    url = r'https://wiki.52poke.com/wiki/' + name
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all(name="table", attrs={"class": "roundy", "class": "textblack", "class": "a-c", "class": "at-c", "class": "sortable"})
    if name in ex_pokemon:
        skill_data = {
            # 通过升级
            "lv": table2json(tables[0], type="lv"),
            # 通过技能机
            "tm": table2json(tables[3], type="tm") if len(tables) > 1 else [],
            # 通过野餐
            "bd": table2json(tables[6], type="bd") if len(tables) > 2 else []
        }
    else:
        skill_data = {
            # 通过升级
            "lv": table2json(tables[0], type="lv"),
            # 通过技能机
            "tm": table2json(tables[1], type="tm") if len(tables) > 1 else [],
            # 通过野餐
            "bd": table2json(tables[2], type="bd") if len(tables) > 2 else []
        }
    with open("./skill/%s.json" % name, "w", encoding="utf-8") as f:
        f.write(json.dumps(skill_data, ensure_ascii=False) + "\n")
