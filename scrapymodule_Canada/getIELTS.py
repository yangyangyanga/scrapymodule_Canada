import re
def get_ielts(ieltsStr):
    ieltDict = {}
    ieltlsrw = re.findall(r"\d\.\d", ieltsStr)
    if len(ieltlsrw) >= 2:
        ieltDict['IELTS'] = ieltlsrw[0]
        ieltDict['IELTS_L'] = ieltlsrw[1]
        ieltDict['IELTS_S'] = ieltlsrw[1]
        ieltDict['IELTS_R'] = ieltlsrw[1]
        ieltDict['IELTS_W'] = ieltlsrw[1]
    elif len(ieltlsrw) == 1:
        ieltDict['IELTS'] = ieltlsrw[0]
        ieltDict['IELTS_L'] = ieltlsrw[0]
        ieltDict['IELTS_S'] = ieltlsrw[0]
        ieltDict['IELTS_R'] = ieltlsrw[0]
        ieltDict['IELTS_W'] = ieltlsrw[0]
    return ieltDict

def get_toefl(toeflStr):
    toeflDict = {}
    toefllsrw = re.findall(r"\d+", toeflStr)
    # print(toefllsrw)
    if len(toefllsrw) >= 2:
        toeflDict['TOEFL'] = toefllsrw[0]
        toeflDict['TOEFL_L'] = toefllsrw[1]
        toeflDict['TOEFL_S'] = toefllsrw[1]
        toeflDict['TOEFL_R'] = toefllsrw[1]
        toeflDict['TOEFL_W'] = toefllsrw[1]
    elif len(toefllsrw) == 1:
        toeflDict['TOEFL'] = toefllsrw[0]
        toeflDict['TOEFL_L'] = toefllsrw[0]
        toeflDict['TOEFL_S'] = toefllsrw[0]
        toeflDict['TOEFL_R'] = toefllsrw[0]
        toeflDict['TOEFL_W'] = toefllsrw[0]
    return toeflDict