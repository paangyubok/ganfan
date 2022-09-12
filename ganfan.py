#!/usr/bin/python3

from curses.ascii import isdigit
import json
import re
import os
import sys
import random

choice_filepath = "./choice.json"
tagset_filepath = "./tagset.json"
typeset_filepath = "./typeset.json"

def parse_question(quest: str) -> dict:
    ret = {"price": {"max": 9999, "min": 0}, "tag": [], "type": []};
    quest = quest.rstrip()
    if quest == "随便":
        return ret

    idx = quest.find("大概"); 
    if idx != -1:
        idx_end = idx + 2
        while idx_end < len(quest) and (quest[idx_end] == "到" or isdigit(quest[idx_end])):
            idx_end += 1
        price_range = re.findall(r"\d+", quest[idx:idx_end])
        if len(price_range) >= 2:
            ret["price"]["min"] = int(price_range[0])
            ret["price"]["max"] = int(price_range[1])

        quest = quest.replace(quest[idx:idx_end], "")
    
    tagset = parse_set(tagset_filepath)
    typeset = parse_set(typeset_filepath)

    idx = quest.rfind("的")
    if idx == -1:
        type_tmp = quest
    else:
        type_tmp = quest[idx+1:]
        tag_tmp = quest[:idx]

    tag_tmp = [t for t in re.split("的|或者|或", tag_tmp) if t]
    tag = []
    for t in tag_tmp:
        if t in tagset:
            tag += tagset[t]
        else:
            tag.append(t)
    ret["tag"] = tag
    
    type_ = []
    type_tmp = [t for t in re.split("或者|或", type_tmp) if t]
    for t in type_tmp:
        if t in typeset:
            type_ += typeset[t]
        else:
            type_.append(t)
    ret["type"] = type_
    return ret

def parse_choice(filepath: str) -> list:
    fp = open(filepath, "r")
    ret = json.load(fp)
    fp.close()
    return ret

def parse_set(filepath: str) -> dict:
    fp = open(filepath, "r")
    ret = json.load(fp)
    fp.close()
    return ret
    
def search_restaurant(quest: str, r: int = 0) -> str:
    all_rest = parse_choice(choice_filepath)
    q_range = parse_question(quest)
    choices = []
    q_tag = set(q_range["tag"])
    q_type = set(q_range["type"])
    for rest in all_rest:
        price = rest["price"]
        if q_range["price"]["min"] <= price and q_range["price"]["max"] >= price \
           and (not q_tag or len(set(rest["tag"]) & q_tag) > 0) \
           and (not q_type or len(set(rest["type"]) & q_type) > 0):
            choices.append(rest["name"])
    if len(choices) < 1:
        return "出门右转第二间." 
    random.shuffle(choices)
    return choices[r % len(choices)]

def test():
    print(parse_set(tagset_filepath))
    print(parse_question("大概30到50的烤鱼"))
    print(parse_question("南门的面"))
    print(parse_question("龙湖的面或者快餐"))
    print(parse_question("大概50到80西门的适合聚餐的"))
    print(parse_question("饭堂或者商业街的\n\r"))
    print(parse_choice(choice_filepath))
    print(search_restaurant("西门的火锅"))

def main():
    argc = len(sys.argv)
    argv = sys.argv

    quest = ""
    if (argc >= 2):
        quest = argv[1]
    else:
        quest = input()
    r = int.from_bytes(os.urandom(4), "little")
    print(search_restaurant(quest, r))


# test()
main()