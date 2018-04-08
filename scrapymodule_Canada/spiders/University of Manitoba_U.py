# -*- coding: utf-8 -*-
import scrapy
import re
from scrapymodule.clearSpace import clear_space, clear_space_str
from scrapymodule.getItem import get_item1
from scrapymodule.getTuition_fee import getTuition_fee
from scrapymodule.items import SchoolItem1

class NewcastleSchoolSpider(scrapy.Spider):
    name = "newcastleBen"
    # start_urls = ["http://www.ncl.ac.uk/undergraduate/degrees/#a-z"]
    start_urls = ["http://www.ncl.ac.uk/undergraduate/degrees/n400/",
"http://www.ncl.ac.uk/undergraduate/degrees/n402/",
"http://www.ncl.ac.uk/undergraduate/degrees/n406/",
"http://www.ncl.ac.uk/undergraduate/degrees/n280/",
"http://www.ncl.ac.uk/undergraduate/degrees/d400/",
"http://www.ncl.ac.uk/undergraduate/degrees/d444/",
"http://www.ncl.ac.uk/undergraduate/degrees/d422/",
"http://www.ncl.ac.uk/undergraduate/degrees/d402/",
"http://www.ncl.ac.uk/undergraduate/degrees/v110/",
"http://www.ncl.ac.uk/undergraduate/degrees/vv14/",
"http://www.ncl.ac.uk/undergraduate/degrees/c305/",
"http://www.ncl.ac.uk/undergraduate/degrees/c211/",
"http://www.ncl.ac.uk/undergraduate/degrees/v400/",
"http://www.ncl.ac.uk/undergraduate/degrees/k100/",
"http://www.ncl.ac.uk/undergraduate/degrees/k190/",
"http://www.ncl.ac.uk/undergraduate/degrees/arch-int-found-ipc/",
"http://www.ncl.ac.uk/undergraduate/degrees/arch-year-one-ipc/",
"http://www.ncl.ac.uk/undergraduate/degrees/h660/",
"http://www.ncl.ac.uk/undergraduate/degrees/h661/",
"http://www.ncl.ac.uk/undergraduate/degrees/c700/",
"http://www.ncl.ac.uk/undergraduate/degrees/c701/",
"http://www.ncl.ac.uk/undergraduate/degrees/biol-and-biomed-int-found-ipc/",
"http://www.ncl.ac.uk/undergraduate/degrees/c100/",
"http://www.ncl.ac.uk/undergraduate/degrees/c103/",
"http://www.ncl.ac.uk/undergraduate/degrees/c1c7/",
"http://www.ncl.ac.uk/undergraduate/degrees/c7c1/",
"http://www.ncl.ac.uk/undergraduate/degrees/c182/",
"http://www.ncl.ac.uk/undergraduate/degrees/c183/",
"http://www.ncl.ac.uk/undergraduate/degrees/b901/",
"http://www.ncl.ac.uk/undergraduate/degrees/b903/",
"http://www.ncl.ac.uk/undergraduate/degrees/b940/",
"http://www.ncl.ac.uk/undergraduate/degrees/b900/",
"http://www.ncl.ac.uk/undergraduate/degrees/nn14/",
"http://www.ncl.ac.uk/undergraduate/degrees/bus-and-man-int-found-ipc/",
"http://www.ncl.ac.uk/undergraduate/degrees/bus-year-one-ipc/",
"http://www.ncl.ac.uk/undergraduate/degrees/n200/",
"http://www.ncl.ac.uk/undergraduate/degrees/h810/",
"http://www.ncl.ac.uk/undergraduate/degrees/h813/",
"http://www.ncl.ac.uk/undergraduate/degrees/h831/",
"http://www.ncl.ac.uk/undergraduate/degrees/h814/",
"http://www.ncl.ac.uk/undergraduate/degrees/h816/",
"http://www.ncl.ac.uk/undergraduate/degrees/h815/",
"http://www.ncl.ac.uk/undergraduate/degrees/h830/",
"http://www.ncl.ac.uk/undergraduate/degrees/hh82/",
"http://www.ncl.ac.uk/undergraduate/degrees/f100/",
"http://www.ncl.ac.uk/undergraduate/degrees/f103/",
"http://www.ncl.ac.uk/undergraduate/degrees/f102/",
"http://www.ncl.ac.uk/undergraduate/degrees/f106/",
"http://www.ncl.ac.uk/undergraduate/degrees/f107/",
"http://www.ncl.ac.uk/undergraduate/degrees/f123/",
"http://www.ncl.ac.uk/undergraduate/degrees/f151/",
"http://www.ncl.ac.uk/undergraduate/degrees/f122/",
"http://www.ncl.ac.uk/undergraduate/degrees/f124/",
"http://www.ncl.ac.uk/undergraduate/degrees/f156/",
"http://www.ncl.ac.uk/undergraduate/degrees/tt12/",
"http://www.ncl.ac.uk/undergraduate/degrees/h210/",
"http://www.ncl.ac.uk/undergraduate/degrees/h242/",
"http://www.ncl.ac.uk/undergraduate/degrees/h206/",
"http://www.ncl.ac.uk/undergraduate/degrees/h296/",
"http://www.ncl.ac.uk/undergraduate/degrees/h202/",
"http://www.ncl.ac.uk/undergraduate/degrees/h292/",
"http://www.ncl.ac.uk/undergraduate/degrees/h208/",
"http://www.ncl.ac.uk/undergraduate/degrees/h298/",
"http://www.ncl.ac.uk/undergraduate/degrees/h200/",
"http://www.ncl.ac.uk/undergraduate/degrees/h290/",
"http://www.ncl.ac.uk/undergraduate/degrees/h201/",
"http://www.ncl.ac.uk/undergraduate/degrees/h205/",
"http://www.ncl.ac.uk/undergraduate/degrees/h295/",
"http://www.ncl.ac.uk/undergraduate/degrees/q810/",
"http://www.ncl.ac.uk/undergraduate/degrees/qq83/",
"http://www.ncl.ac.uk/undergraduate/degrees/q800/",
"http://www.ncl.ac.uk/undergraduate/degrees/y001/",
"http://www.ncl.ac.uk/undergraduate/degrees/g400/",
"http://www.ncl.ac.uk/undergraduate/degrees/g405/",
"http://www.ncl.ac.uk/undergraduate/degrees/g406/",
"http://www.ncl.ac.uk/undergraduate/degrees/g401/",
"http://www.ncl.ac.uk/undergraduate/degrees/i100/",
"http://www.ncl.ac.uk/undergraduate/degrees/i520/",
"http://www.ncl.ac.uk/undergraduate/degrees/i522/",
"http://www.ncl.ac.uk/undergraduate/degrees/i521/",
"http://www.ncl.ac.uk/undergraduate/degrees/i524/",
"http://www.ncl.ac.uk/undergraduate/degrees/g450/",
"http://www.ncl.ac.uk/undergraduate/degrees/i610/",
"http://www.ncl.ac.uk/undergraduate/degrees/g451/",
"http://www.ncl.ac.uk/undergraduate/degrees/i612/",
"http://www.ncl.ac.uk/undergraduate/degrees/i140/",
"http://www.ncl.ac.uk/undergraduate/degrees/i141/",
"http://www.ncl.ac.uk/undergraduate/degrees/g420/",
"http://www.ncl.ac.uk/undergraduate/degrees/i120/",
"http://www.ncl.ac.uk/undergraduate/degrees/g421/",
"http://www.ncl.ac.uk/undergraduate/degrees/i122/",
"http://www.ncl.ac.uk/undergraduate/degrees/i190/",
"http://www.ncl.ac.uk/undergraduate/degrees/i192/",
"http://www.ncl.ac.uk/undergraduate/degrees/i191/",
"http://www.ncl.ac.uk/undergraduate/degrees/i194/",
"http://www.ncl.ac.uk/undergraduate/degrees/g600/",
"http://www.ncl.ac.uk/undergraduate/degrees/g603/",
"http://www.ncl.ac.uk/undergraduate/degrees/w301/",
"http://www.ncl.ac.uk/undergraduate/degrees/d455/",
"http://www.ncl.ac.uk/undergraduate/degrees/a206/",
"http://www.ncl.ac.uk/undergraduate/degrees/h990/",
"http://www.ncl.ac.uk/undergraduate/degrees/h991/",
"http://www.ncl.ac.uk/undergraduate/degrees/f641/",
"http://www.ncl.ac.uk/undergraduate/degrees/f640/",
"http://www.ncl.ac.uk/undergraduate/degrees/f646/",
"http://www.ncl.ac.uk/undergraduate/degrees/f645/",
"http://www.ncl.ac.uk/undergraduate/degrees/l100/",
"http://www.ncl.ac.uk/undergraduate/degrees/ln12/",
"http://www.ncl.ac.uk/undergraduate/degrees/l161/",
"http://www.ncl.ac.uk/undergraduate/degrees/x390/",
"http://www.ncl.ac.uk/undergraduate/degrees/h607/",
"http://www.ncl.ac.uk/undergraduate/degrees/h604/",
"http://www.ncl.ac.uk/undergraduate/degrees/h606/",
"http://www.ncl.ac.uk/undergraduate/degrees/h605/",
"http://www.ncl.ac.uk/undergraduate/degrees/h623/",
"http://www.ncl.ac.uk/undergraduate/degrees/h622/",
"http://www.ncl.ac.uk/undergraduate/degrees/h640/",
"http://www.ncl.ac.uk/undergraduate/degrees/h621/",
"http://www.ncl.ac.uk/undergraduate/degrees/h652/",
"http://www.ncl.ac.uk/undergraduate/degrees/h654/",
"http://www.ncl.ac.uk/undergraduate/degrees/h101/",
"http://www.ncl.ac.uk/undergraduate/degrees/h103/",
"http://www.ncl.ac.uk/undergraduate/degrees/q302/",
"http://www.ncl.ac.uk/undergraduate/degrees/q300/",
"http://www.ncl.ac.uk/undergraduate/degrees/qv31/",
"http://www.ncl.ac.uk/undergraduate/degrees/q306/",
"http://www.ncl.ac.uk/undergraduate/degrees/qw38/",
"http://www.ncl.ac.uk/undergraduate/degrees/f850/",
"http://www.ncl.ac.uk/undergraduate/degrees/f851/",
"http://www.ncl.ac.uk/undergraduate/degrees/f8d4/",
"http://www.ncl.ac.uk/undergraduate/degrees/fd84/",
"http://www.ncl.ac.uk/undergraduate/degrees/f8h8/",
"http://www.ncl.ac.uk/undergraduate/degrees/fh88/",
"http://www.ncl.ac.uk/undergraduate/degrees/f8c1/",
"http://www.ncl.ac.uk/undergraduate/degrees/fc81/",
"http://www.ncl.ac.uk/undergraduate/degrees/f8f6/",
"http://www.ncl.ac.uk/undergraduate/degrees/ff86/",
"http://www.ncl.ac.uk/undergraduate/degrees/p303/",
"http://www.ncl.ac.uk/undergraduate/degrees/p313/",
"http://www.ncl.ac.uk/undergraduate/degrees/w150/",
"http://www.ncl.ac.uk/undergraduate/degrees/w344/",
"http://www.ncl.ac.uk/undergraduate/degrees/nd61/",
"http://www.ncl.ac.uk/undergraduate/degrees/b46d/",
"http://www.ncl.ac.uk/undergraduate/degrees/b4d6/",
"http://www.ncl.ac.uk/undergraduate/degrees/t901/",
"http://www.ncl.ac.uk/undergraduate/degrees/b901/",
"http://www.ncl.ac.uk/undergraduate/degrees/f862/",
"http://www.ncl.ac.uk/undergraduate/degrees/f867/",
"http://www.ncl.ac.uk/undergraduate/degrees/f800/",
"http://www.ncl.ac.uk/undergraduate/degrees/l701/",
"http://www.ncl.ac.uk/undergraduate/degrees/lk74/",
"http://www.ncl.ac.uk/undergraduate/degrees/t901/",
"http://www.ncl.ac.uk/undergraduate/degrees/l241/",
"http://www.ncl.ac.uk/undergraduate/degrees/v100/",
"http://www.ncl.ac.uk/undergraduate/degrees/vv41/",
"http://www.ncl.ac.uk/undergraduate/degrees/human-and-soc-sci-int-found-ipc/",
"http://www.ncl.ac.uk/undergraduate/degrees/n120/",
"http://www.ncl.ac.uk/undergraduate/degrees/n122/",
"http://www.ncl.ac.uk/undergraduate/degrees/n124/",
"http://www.ncl.ac.uk/undergraduate/degrees/n5n2/",
"http://www.ncl.ac.uk/undergraduate/degrees/n5n5/",
"http://www.ncl.ac.uk/undergraduate/degrees/tt12/",
"http://www.ncl.ac.uk/undergraduate/degrees/p500/",
"http://www.ncl.ac.uk/undergraduate/degrees/m101/",
"http://www.ncl.ac.uk/undergraduate/degrees/q100/",
"http://www.ncl.ac.uk/undergraduate/degrees/q1t4/",
"http://www.ncl.ac.uk/undergraduate/degrees/q1r1/",
"http://www.ncl.ac.uk/undergraduate/degrees/q1r2/",
"http://www.ncl.ac.uk/undergraduate/degrees/q1r4/",
"http://www.ncl.ac.uk/undergraduate/degrees/h270/",
"http://www.ncl.ac.uk/undergraduate/degrees/h271/",
"http://www.ncl.ac.uk/undergraduate/degrees/c161/",
"http://www.ncl.ac.uk/undergraduate/degrees/cf17/",
"http://www.ncl.ac.uk/undergraduate/degrees/j615/",
"http://www.ncl.ac.uk/undergraduate/degrees/j616/",
"http://www.ncl.ac.uk/undergraduate/degrees/h504/",
"http://www.ncl.ac.uk/undergraduate/degrees/h501/",
"http://www.ncl.ac.uk/undergraduate/degrees/h502/",
"http://www.ncl.ac.uk/undergraduate/degrees/h503/",
"http://www.ncl.ac.uk/undergraduate/degrees/h355/",
"http://www.ncl.ac.uk/undergraduate/degrees/h356/",
"http://www.ncl.ac.uk/undergraduate/degrees/h520/",
"http://www.ncl.ac.uk/undergraduate/degrees/h524/",
"http://www.ncl.ac.uk/undergraduate/degrees/c350/",
"http://www.ncl.ac.uk/undergraduate/degrees/n500/",
"http://www.ncl.ac.uk/undergraduate/degrees/nn52/",
"http://www.ncl.ac.uk/undergraduate/degrees/b62m/",
"http://www.ncl.ac.uk/undergraduate/degrees/g101/",
"http://www.ncl.ac.uk/undergraduate/degrees/g100/",
"http://www.ncl.ac.uk/undergraduate/degrees/g103/",
"http://www.ncl.ac.uk/undergraduate/degrees/ng41/",
"http://www.ncl.ac.uk/undergraduate/degrees/gl11/",
"http://www.ncl.ac.uk/undergraduate/degrees/gg13/",
"http://www.ncl.ac.uk/undergraduate/degrees/ggc3/",
"http://www.ncl.ac.uk/undergraduate/degrees/g1n3/",
"http://www.ncl.ac.uk/undergraduate/degrees/g1n2/",
"http://www.ncl.ac.uk/undergraduate/degrees/hh37/",
"http://www.ncl.ac.uk/undergraduate/degrees/h300/",
"http://www.ncl.ac.uk/undergraduate/degrees/h301/",
"http://www.ncl.ac.uk/undergraduate/degrees/h3h8/",
"http://www.ncl.ac.uk/undergraduate/degrees/h3h2/",
"http://www.ncl.ac.uk/undergraduate/degrees/h304/",
"http://www.ncl.ac.uk/undergraduate/degrees/h305/",
"http://www.ncl.ac.uk/undergraduate/degrees/h3h6/",
"http://www.ncl.ac.uk/undergraduate/degrees/pql0/",
"http://www.ncl.ac.uk/undergraduate/degrees/b902/",
"http://www.ncl.ac.uk/undergraduate/degrees/a100/",
"http://www.ncl.ac.uk/undergraduate/degrees/a101/",
"http://www.ncl.ac.uk/undergraduate/degrees/h611/",
"http://www.ncl.ac.uk/undergraduate/degrees/h612/",
"http://www.ncl.ac.uk/undergraduate/degrees/t901/",
"http://www.ncl.ac.uk/undergraduate/degrees/tn92/",
"http://www.ncl.ac.uk/undergraduate/degrees/qt19/",
"http://www.ncl.ac.uk/undergraduate/degrees/r9q9/",
"http://www.ncl.ac.uk/undergraduate/degrees/w300/",
"http://www.ncl.ac.uk/undergraduate/degrees/w304/",
"http://www.ncl.ac.uk/undergraduate/degrees/bd46/",
"http://www.ncl.ac.uk/undergraduate/degrees/bd64/",
"http://www.ncl.ac.uk/undergraduate/degrees/a207/",
"http://www.ncl.ac.uk/undergraduate/degrees/b210/",
"http://www.ncl.ac.uk/undergraduate/degrees/b230/",
"http://www.ncl.ac.uk/undergraduate/degrees/v500/",
"http://www.ncl.ac.uk/undergraduate/degrees/fh82/",
"http://www.ncl.ac.uk/undergraduate/degrees/phys-sci-and-engin-int-found-ipc/",
"http://www.ncl.ac.uk/undergraduate/degrees/f300/",
"http://www.ncl.ac.uk/undergraduate/degrees/f303/",
"http://www.ncl.ac.uk/undergraduate/degrees/f304/",
"http://www.ncl.ac.uk/undergraduate/degrees/f305/",
"http://www.ncl.ac.uk/undergraduate/degrees/b100/",
"http://www.ncl.ac.uk/undergraduate/degrees/k400/",
"http://www.ncl.ac.uk/undergraduate/degrees/l200/",
"http://www.ncl.ac.uk/undergraduate/degrees/ll21/",
"http://www.ncl.ac.uk/undergraduate/degrees/vl12/",
"http://www.ncl.ac.uk/undergraduate/degrees/ll32/",
"http://www.ncl.ac.uk/undergraduate/degrees/rt47/",
"http://www.ncl.ac.uk/undergraduate/degrees/c800/",
"http://www.ncl.ac.uk/undergraduate/degrees/c8c1/",
"http://www.ncl.ac.uk/undergraduate/degrees/c8g1/",
"http://www.ncl.ac.uk/undergraduate/degrees/c8b4/",
"http://www.ncl.ac.uk/undergraduate/degrees/c8c6/",
"http://www.ncl.ac.uk/undergraduate/degrees/d452/",
"http://www.ncl.ac.uk/undergraduate/degrees/l300/",
"http://www.ncl.ac.uk/undergraduate/degrees/rt47/",
"http://www.ncl.ac.uk/undergraduate/degrees/b621/",
"http://www.ncl.ac.uk/undergraduate/degrees/c600/",
"http://www.ncl.ac.uk/undergraduate/degrees/g300/",
"http://www.ncl.ac.uk/undergraduate/degrees/study-abroad-with-english-ipc/",
"http://www.ncl.ac.uk/undergraduate/degrees/h244/",
"http://www.ncl.ac.uk/undergraduate/degrees/h249/",
"http://www.ncl.ac.uk/undergraduate/degrees/h392/",
"http://www.ncl.ac.uk/undergraduate/degrees/f345/",
"http://www.ncl.ac.uk/undergraduate/degrees/f344/",
"http://www.ncl.ac.uk/undergraduate/degrees/k421/",
"http://www.ncl.ac.uk/undergraduate/degrees/c300/",
"http://www.ncl.ac.uk/undergraduate/degrees/c301/",]
    # print(len(start_urls))
    start_urls = list(set(start_urls))
    # print(len(start_urls))

    def parse(self, response):
        item = get_item1(SchoolItem1)
        item['university'] = "Newcastle University"
        item['country'] = 'England'
        item['website'] = 'http://www.ncl.ac.uk/'
        item['url'] = response.url
        print("===========================")
        print(response.url)
        try:
            # 专业
            programme = response.xpath(
                "//header[@class='pageTitle']/h1/text()").extract()
            programme = ''.join(programme)
            item['programme'] = programme
            # print("item['programme']: ", item['programme'])

            # ucas_code
            ucas_code = response.xpath(
                "//div[@class='tablet-mobile-hide']//p[@class='no-padding']/text()").extract()
            ucas_code = ''.join(ucas_code)
            item['ucas_code'] = ucas_code
            # print("item['ucas_code']: ", item['ucas_code'])

            # duration
            duration = response.xpath(
                "//div[@class='icon-durantion tablet-mobile-hide']//p/text()").extract()
            duration = ''.join(duration)
            item['duration'] = duration
            # print("item['duration']: ", item['duration'])

            # degree_type
            degree_type = response.xpath(
                "//div[@class='icon-degree tablet-mobile-hide']//p/text()").extract()
            degree_type = ''.join(degree_type)
            item['degree_type'] = degree_type
            # print("item['degree_type']: ", item['degree_type'])
            if item['degree_type'] in item['programme'] and item['degree_type'] != "":
                item['programme'] = ''.join(item['programme'].split(item['degree_type']))
            # print("item['programme']: ", item['programme'])

            # overview
            overview = response.xpath(
            "//div[@class='contentSeparator containAsides textEditorArea'][1]//text()").extract()
            overview = ''.join(overview)
            item['overview'] = overview.strip()
            # print("item['overview']: ", item['overview'])

            # print(response.text)
            # //h2[contains(text(),'Course Details')]/..
            # modulesTeaching = response.xpath(
            #     "//h2[contains(text(),'Course Details')]/following-sibling::div[position()<last()-1]//text()").extract()
            # //html//div[@class='tab-wrapper']/div[@class='contentSeparator tab containAsides tabtp'][2]
            allcontent = response.xpath(
                "//main[@id='content']//article//text()").extract()
            print("allcontent：", allcontent)

            # modules
            if "Course Details" in allcontent:
                modulesIndex = allcontent.index("Course Details")
                if "Teaching and assessment" in allcontent:
                    modulesIndexEnd = allcontent.index("Teaching and assessment")
                    modules = allcontent[modulesIndex+1:modulesIndexEnd]
                    clear_space(modules)
                    item['modules'] = '\n'.join(modules)
                elif "Next step: Entry Requirements" in allcontent:
                    modulesIndexEnd = allcontent.index("Next step: Entry Requirements")
                    modules = allcontent[modulesIndex+1:modulesIndexEnd]
                    clear_space(modules)
                    item['modules'] = '\n'.join(modules)
            # print("item['modules']: ", item['modules'])

            # 评估方式
            if "Teaching and assessment" in allcontent:
                teachingIndex = allcontent.index("Teaching and assessment")
                if "Next step: Entry Requirements" in allcontent:
                    teachingIndexEnd = allcontent.index("Next step: Entry Requirements")
                    teaching = allcontent[teachingIndex+1:teachingIndexEnd]
                    clear_space(teaching)
                    item['teaching'] = '\n'.join(teaching)
            # print("item['teaching']: ", item['teaching'])

            # 学术要求
            if "Entry Requirements" in allcontent:
                entry_requirementsIndex = allcontent.index("Entry Requirements")
                if "Next step: Careers" in allcontent:
                    entry_requirementsIndexEnd = allcontent.index("Next step: Careers")
                    entry_requirements = allcontent[entry_requirementsIndex+1:entry_requirementsIndexEnd]
                    clear_space(entry_requirements)
                    item['entry_requirements'] = '\n'.join(entry_requirements)
            # print("item['entry_requirements']: ", item['entry_requirements'])

            # 学术要求
            if "Entry Requirements" in allcontent:
                entry_requirementsIndex = allcontent.index("Entry Requirements")
                if "Next step: Careers" in allcontent:
                    entry_requirementsIndexEnd = allcontent.index("Next step: Careers")
                    entry_requirements = allcontent[entry_requirementsIndex+1:entry_requirementsIndexEnd]
                    clear_space(entry_requirements)
                    item['entry_requirements'] = '\n'.join(entry_requirements)
            # print("item['entry_requirements']: ", item['entry_requirements'])

            # Alevel
            if "A Levels" in allcontent:
                AlevelIndex = allcontent.index("A Levels")
                if "Scottish Qualifications" in allcontent:
                    AlevelIndexEnd = allcontent.index("Scottish Qualifications")
                    Alevel = allcontent[AlevelIndex+2:AlevelIndexEnd]
                    clear_space(Alevel)
                    item['Alevel'] = ''.join(Alevel).strip()
            # print("item['Alevel']: ", item['Alevel'])

            # IB
            if "International Baccalaureate" in allcontent:
                IBIndex = allcontent.index("International Baccalaureate")
                if "Irish Leaving Certificate" in allcontent:
                    IBIndexEnd = allcontent.index("Irish Leaving Certificate")
                    IB = allcontent[IBIndex + 2:IBIndexEnd]
                    clear_space(IB)
                    item['IB'] = ''.join(IB).strip()
            # print("item['IB']: ", item['IB'])

            # IELTS
            if "English language requirements" in allcontent:
                IELTSIndex = allcontent.index("English language requirements")
                if "International Programmes" in allcontent:
                    IELTSIndexEnd = allcontent.index("International Programmes")
                    IELTS = allcontent[IELTSIndex + 2:IELTSIndexEnd]
                    clear_space(IELTS)
                    item['IELTS'] = ''.join(IELTS).strip()
                elif "Other International Qualifications" in allcontent:
                    IELTSIndexEnd = allcontent.index("Other International Qualifications")
                    IELTS = allcontent[IELTSIndex + 2:IELTSIndexEnd]
                    clear_space(IELTS)
                    item['IELTS'] = ''.join(IELTS).strip()
            elif "English requirements" in allcontent:
                IELTSIndex = allcontent.index("English requirements")
                if "Next step: Progression" in allcontent:
                    IELTSIndexEnd = allcontent.index("Next step: Progression")
                    IELTS = allcontent[IELTSIndex + 2:IELTSIndexEnd]
                    clear_space(IELTS)
                    item['IELTS'] = ''.join(IELTS).strip()
            elif "English Language Requirements" in allcontent:
                IELTSIndex = allcontent.index("English Language Requirements")
                if "International Programmes" in allcontent:
                    IELTSIndexEnd = allcontent.index("International Programmes")
                    IELTS = allcontent[IELTSIndex + 2:IELTSIndexEnd]
                    clear_space(IELTS)
                    item['IELTS'] = ''.join(IELTS).strip()
                elif "Other International Qualifications" in allcontent:
                    IELTSIndexEnd = allcontent.index("Other International Qualifications")
                    IELTS = allcontent[IELTSIndex + 2:IELTSIndexEnd]
                    clear_space(IELTS)
                    item['IELTS'] = ''.join(IELTS).strip()
            # print("item['IELTS']: ", item['IELTS'])

            # career
            if "Careers" in allcontent:
                careerIndex = allcontent.index("Careers")
                if "Next step: Fees and Funding" in allcontent:
                    careerIndexEnd = allcontent.index("Next step: Fees and Funding")
                    career = allcontent[careerIndex + 2:careerIndexEnd]
                    clear_space(career)
                    item['career'] = '\n'.join(career).strip()
            # print("item['career']: ", item['career'])

            # tuition_fee
            if "Tuition Fees (International students)" in allcontent:
                tuition_feeIndex = allcontent.index("Tuition Fees (International students)")
                if " Scholarships and Financial Support (UK students)" in allcontent:
                    tuition_feeIndexEnd = allcontent.index(" Scholarships and Financial Support (UK students)")
                    tuition_fee = allcontent[tuition_feeIndex + 2:tuition_feeIndexEnd]
                    clear_space(tuition_fee)
                    allfee = re.findall(r"\d+,\d+", ''.join(tuition_fee))
                    # print("allfee: ", allfee)
                    item['tuition_fee'] = ''.join(allfee).replace(",", "")
            # print("item['tuition_fee']: ", item['tuition_fee'])

            item['how_to_apply'] = "http://www.ncl.ac.uk/undergraduate/apply/ucas/"

            yield item
        except Exception as e:
            with open("./error/"+item['university']+item['degree_level']+".txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

