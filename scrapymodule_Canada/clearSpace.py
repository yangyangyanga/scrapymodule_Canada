
def clear_space(templist):
    for i in range(len(templist)):
        templist[i] = templist[i].replace('\n', " ")
        templist[i] = templist[i].strip(" ")
        templist[i] = templist[i].replace('\r', " ")
        templist[i] = templist[i].replace('\t', " ")

def clear_space_str(str):
    str = str.replace("\n", " ").replace("\r", " ").strip()
    return str

def clear_space_list(templist):
    for i in range(len(templist)):
        templist[i] = templist[i].replace('\n', " ")
        templist[i] = templist[i].strip(" ")
        templist[i] = templist[i].replace('\r', " ")
        templist[i] = templist[i].replace('\t', " ")
    return templist