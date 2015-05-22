#EntMaker [Version: 1.0]
#Made by hTml in 2015
#https://github.com/hTmlDP/
#---

#CONFIG
mapnames=["propaint", "beta/wobluda_fix"] #TODO: Add an option to load from a directory, too lazy to do it now. You can post it at the github repo though.
"""
#EXAMPLE, COMMENTED CONFIG FOR OLD-SCHOOL MAPS
custom_vars={"info_player_deathmatch": {"giveammo": "200",
                                        "givegun": "carbine",
                                        "givehopper": "200",
                                        "loadedco2": "20oz",
                                        "givebarrel": "steel"},
             "item_pballhopper": None, #Skip
             "item_pballbarrel": None, #Skip
             "item_pballco2": None, #Skip
             }
"""
#EXAMPLE CONFIG FOR A PGP SERVER
custom_vars={"info_player_deathmatch": {
                                        "givegun": None
                                        },
             "weapon_pballgun": None, #Skip
             }

#END OF THE CONFIG




#Code, edit for your own risk ;)
import re
from os.path import join, exists
from os import mkdir

if not exists("entmaker_output"):
    mkdir("entmaker_output")

def txtFromDict(ent):
    if not ent:
        return ""
    ret="{\n"
    for var in ent:
        ret+='"%s" "%s"\n'%(var, ent[var])
    ret+="}\n"
    return ret

def editClass(ent):
    _custom_vars={}
    if ("classname" in ent) and (ent["classname"] in custom_vars):
        _custom_vars=custom_vars[ent["classname"]]
    else:
        return ent
    if _custom_vars:
        for var in _custom_vars:
            if _custom_vars[var]:
                ent[var]=_custom_vars[var]
            else:
                ent.pop(var, None)
    else:
        return None
    return ent

for mapname in mapnames:
    with open("pball/maps/%s.bsp" % mapname, "rb") as fo:
        text=fo.readlines()
    txt=""
    text.reverse();
    i=1
    char=125
    line=""
    while char in (125, 123, 34):
        txt=line+txt
        line=text[i].decode('utf-8', 'ignore')
        char=ord(line[0]);
        i+=1
    txt="{\n"+txt
    txt = re.findall("\\{(.*?)\\}", txt, re.DOTALL)
    ent_list=[]
    for ent in txt:
        temp_dict = {}
        for var in re.findall('\\"(.*?)\\"\\ \\"(.*?)"\\\n', ent):
            temp_dict[var[0]]=var[1]
        ent_list.append(editClass(temp_dict))
    ent_text=""
    for ent in ent_list:
        ent_text+=txtFromDict(ent)
    with open("entmaker_output/{mapname}.ent".format(mapname=mapname.split('/')[-1]), "w+") as fo:
        fo.write(ent_text)
