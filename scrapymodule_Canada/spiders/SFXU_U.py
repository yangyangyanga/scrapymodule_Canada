# -*- coding: utf-8 -*-
import scrapy
import re
from scrapymodule_Canada.clearSpace import clear_space, clear_space_str
from scrapymodule_Canada.getItem import get_item
from scrapymodule_Canada.getTuition_fee import getTuition_fee
from scrapymodule_Canada.items import ScrapymoduleCanadaItem
import requests
from lxml import etree

class SFXUbenSchoolSpider(scrapy.Spider):
    name = "sfxuBen"
    start_urls = ["https://www.stfx.ca/academics"]
    # print(len(start_urls))
    # start_urls = list(set(start_urls))
    # print(len(start_urls))

    def parse(self, response):
        programmeKey = response.xpath("//span[@class='c-program__title']//text()").extract()
        clear_space(programmeKey)
        departmentValue = ["Faculty of Arts",
"Faculty of Arts, Faculty of Science",
"Faculty of Arts",
"Faculty of Education",
"Faculty of Science",
"Faculty of Business",
"Faculty of Arts",
"Faculty of Arts",
"Faculty of Science",
"Faculty of Arts",
"Faculty of Arts, Faculty of Science",
"Faculty of Arts, Faculty of Science",
"Faculty of Arts",
"Faculty of Education",
"Faculty of Science",
"Faculty of Arts",
"Faculty of Science",
"Faculty of Arts",
"Faculty of Science",
"Faculty of Arts, Faculty of Science",
"Faculty of Arts",
"Faculty of Arts, Faculty of Science",
"Faculty of Science",
"Faculty of Arts",
"Faculty of Education",
"Faculty of Education",
"Faculty of Science",
"Faculty of Arts",
"Faculty of Arts",
"Faculty of Science",
"Faculty of Education",
"Faculty of Arts",
"Faculty of Science",
"Faculty of Arts",
"Faculty of Arts, Faculty of Science",
"Faculty of Arts",
"Faculty of Arts",
"Faculty of Arts",
"Faculty of Arts",
"Faculty of Arts", ]
        resultDict = {}
        # print(len(programmeKey))
        # print(len(departmentValue))
        for i in range(len(programmeKey)):
            resultDict[programmeKey[i]] = departmentValue[i]
        # print(resultDict)

        links = response.xpath("//div[@class='o-container  c-program-search__slider  js-program-search-slider']//a/@href").extract()
        # print(len(links))
        links = list(set(links))
        # 40
        # print(len(links))
        for link in links:
            if "https:" not in link:
                url = "https://www.stfx.ca" + link
                yield scrapy.Request(url, callback=self.parse_data, meta=resultDict)

    def parse_data(self, response):
        item = get_item(ScrapymoduleCanadaItem)
        item['university'] = "St. Francis Xavier University"
        item['country'] = 'Canada'
        item['website'] = 'https://www.stfx.ca/'
        item['url'] = response.url
        item['degree_level'] = "0"
        item['TOEFL_code'] = item['SAT_code'] = ""
        print("===========================")
        print(response.url)
        try:
            # 专业
            programme = response.xpath(
                "//h1[@class='c-page-title c-page-title--hero']//text()").extract()
            programme = ''.join(programme)
            item['programme'] = programme
            print("item['programme']: ", item['programme'])

            degree_type = response.xpath(
                "//span[@class='c-hero__term-span']//text()").extract()
            clear_space(degree_type)
            dt = ""
            # if len(degree_type) != 0:
            if len(degree_type) == 1:
                dt = "Bachelor of " + degree_type[0].strip()
            elif len(degree_type) == 2:
                dt = "Bachelor of " + degree_type[0].strip() + ", Bachelor of " + degree_type[1].strip()
            item['degree_type'] = dt
            # print("item['degree_type']: ", item['degree_type'])

            item['department'] = response.meta[item['programme']]
            # print("item['department']: ", item['department'])

            # overview
            # //html//div[@class='region region-content']/div[1]/div[1]
            overview = response.xpath(
                "//html//div[@class='region region-content']/div[1]/div[1]//text()").extract()
            overview = ''.join(overview).strip()
            item['overview'] = overview
            # print("item['overview']: ", item['overview'])

            # career
            # //html/body/div[@class='o-container']//div[4]/div[1]
            career = response.xpath(
                "//div[@class='o-container']//div[@class='o-row']//text()").extract()
            clear_space(career)
            career = ' '.join(career).strip()
            # print("career", career)
            if "Rewarding careers in" in career:
                careerIndex = career.find("Rewarding careers in")
                if "Flexible degree" in career:
                    careerIndexEnd = career.find("Flexible degree")
                    ca = career[careerIndex:careerIndexEnd]
                    item['career'] = ''.join(ca).strip()
            # print("item['career']: ", item['career'])

            # modules
            modulesDict = {'Anthropology': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=ANTH&pterm=201810', 'APEX': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=APEX&pterm=201810', 'Aquatic Resources': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=AQUA&pterm=201810', 'Art': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=ART&pterm=201810', 'Biology': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=BIOL&pterm=201810', 'Business Administration': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=BSAD&pterm=201810', 'Catholic Studies': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=CATH&pterm=201810', 'Celtic Studies': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=CELT&pterm=201810', 'Chemistry': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=CHEM&pterm=201810', 'Classics': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=CLAS&pterm=201810', 'Computer Science': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=CSCI&pterm=201810', 'Co-operative Education': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=COOP&pterm=201810', 'Development Studies': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=DEVS&pterm=201810', 'Earth Sciences': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=ESCI&pterm=201810', 'Economics': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=ECON&pterm=201810', 'Engineering': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=ENGR&pterm=201810', 'English': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=ENGL&pterm=201810', 'Environmental Sciences': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=ENSC&pterm=201810', 'French': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=FREN&pterm=201810', 'German': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=GERM&pterm=201810', 'Health': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=HLTH&pterm=201810', 'History': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=HIST&pterm=201810', 'Human Kinetics': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=HKIN&pterm=201810', 'Human Nutrition': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=HNU&pterm=201810', 'Interdisciplinary Studies': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=IDS&pterm=201810', 'Mathematics': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=MATH&pterm=201810', "Mi'kmaq": 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=MIKM&pterm=201810', 'Music': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=MUSI&pterm=201810', 'Nursing': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=NURS&pterm=201810', 'Philosophy': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=PHIL&pterm=201810', 'Physics': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=PHYS&pterm=201810', 'Political Science': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=PSCI&pterm=201810', 'Psychology': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=PSYC&pterm=201810', 'Public Policy and Governance': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=PGOV&pterm=201810', 'Religious Studies': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=RELS&pterm=201810', 'Sociology': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=SOCI&pterm=201810', 'Spanish': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=SPAN&pterm=201810', 'Statistics': 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=STAT&pterm=201810', "Women's & Gender Studies": 'https://mesamis.stfx.ca/reports/Timetable_List.asp?pdept=WMGS&pterm=201810'}
            modulesUrl = modulesDict.get(item['programme'])
            print(modulesUrl)
            item['modules'] = modulesUrl
            # if modulesUrl != None:
            #     modules = self.parse_modules(modulesUrl)
            #     print("modules: ", modules)

            item['start_date'] = "September"
            item['deadline'] = "JUNE 30"
            item['tuition_fee'] = "$8,084"
            item['entry_requirements'] = """General Admission Requirements
For high school graduates, the minimum requirements include an average of 70% in Grade 12, with no marks below 65% in each of the required subjects.  
Admissions is competitive, so higher averages may be required in certain programs especially in Nursing, Human Kinetics and Engineering.
StFX has a new Admissions Requirement for the Four-Year Nursing and Two-Year Accelerated Nursing Programs for 2018. The CASPer test is mandatory for all applicants. Please visit here for more information. 
Note: Students who apply to the Four-Year Nursing Program after February 11 who have not completed the CASPer test will not be considered for Nursing. Students without CASPer scores will be deemed to have an incomplete application and will be processed for second choice ONLY.  
The last date to take the CASPer test and still be considered for the Four-Year Nursing program is February 11th.  
Transfer students who have applied to the Four-Year nursing program can expect to receive a decision on their application in May. No nursing offers will be made for transfer students until all transcripts for second semester have been received."""
            item['Application_link'] = "https://www.stfx.ca/admissions/apply"
            item['duration'] = "4"
            item['IELTS'] = "6.5"
            item['IELTS_L'] = "6"
            item['IELTS_S'] = "6"
            item['IELTS_R'] = "6"
            item['IELTS_W'] = "6"
            item['other'] = "Students with IELTS scores below 6.5 may be considered for admission conditional on the completion of a program designed to improve English language competency to an IELTS 6.5 equivalent."
            item['TOEFL'] = "92"
            item['SATI'] = "SAT and ACT scores are NOT required for admission into any of these academic programs. An overall B average is required in these courses for admission into each respective program."
            item['IB'] = """StFX welcomes and encourages applications from International Baccalaureate students. Please note the following:
Students will be considered for admission using the International Baccalaureate (IB) Diploma with a minimum score of 24. 
Students admitted to StFX with a score of 30 or higher on the IB Diploma, and who have received a score of at least 5 on all higher level and standard level courses, will be granted up to 30 credits. Students who have any one minimum score falling below 5 will have their courses individually assessed for possible transfer credits. 
Students who have completed IB courses but who do not possess the diploma, or who scored less than 30 on the IB Diploma, may receive individual university course credit if they have achieved grades of 5, 6, or 7 in higher level courses.
"""

            if item['programme'] == "Nursing":
                item['entry_requirements'] = """New Admissions Requirement for Nursing
Effective immediately all students interested in the Four-Year Traditional BSc Nursing program and Two-Year Accelerated program at StFX are required to complete a CASPer Assessment prior to the March 1st and June 1st application deadlines. This includes Current StFX Students wishing to apply to change programs.  Please click here for more information.
 
CASPer Admission Requirements (New)
    Effective immediately all students interested in the Four-Year Traditional BSc Nursing program and Two-Year Accelerated program at StFX are required to complete a CASPer Assessment prior to the March 1st and June 1st application deadlines.
This test is an online screening tool designed to evaluate the student’s personal and professional characteristics. The test is mandatory for all students who wish to be considered for Nursing. Knowing that academic knowledge is not always the best indicator of a superior applicant, CASPer allows our admissions team to gain a better understanding of each applicant, beyond cognitive measures. CASPer assesses non-cognitive skills and interpersonal characteristics.

Admissions Requirement:
Applicants are required to complete a 90-minute online assessment (CASPer).
Successful completion of CASPer is mandatory in order to maintain admission eligibility.
CASPer can be attempted once during a StFX admission cycle (October-February)
Multiple test attempts are not permitted in a recruitment cycle.
Applicants must submit an application to StFX prior to registering for the CASPer test.

Test Results:
CASPer scores will be submitted directly to the institutions identified when registering for the test at takeCASPer.com.
Approximately three weeks after the test is complete scores will be received by StFX, and will be used in combination with academic performance to determine admissibility to the program.
CASPer scores are not released to students in an effort to protect the integrity of the test.
CASPer test results are valid for one StFX admission cycle (October-February).
Test results from previous years will not be considered.
Questions: 
Please direct any inquiries on the test to support@takecasper.com.
Test Dates & Registration
CASPer test dates and times for September 2018 Nursing admission are now available at takeCASPer.com under the heading "Canadian Nursing School (2018 Admissions)". 
Limited testing dates are available and are set by CASPer. 
Students must register for the date they are available to take the assessment. 


Four-Year BScN Test Date Options
November 19, 2017 (Sunday) 4:00pm EDT
January 24, 2018 (Wednesday) 5:00pm EDT
February 11, 2018 (Sunday) 12:00pm, 3:00pm EDT
Two-Year Accelerated Test Date Options
November 19, 2017 (Sunday) 4:00pm EDT
January 24, 2018 (Wednesday) 5:00pm EDT
February 11, 2018 (Sunday) 12:00pm, 3:00pm EDT
February 22, 2018 (Thursday) 5:00pm EDT, 8:00pm EDT
Current StFX Student Test Date Options (For students requesting a change of program in mesAMIS)
November 19, 2017 (Sunday) 4:00pm EDT
January 24, 2018 (Wednesday) 5:00pm EDT
February 11, 2018 (Sunday) 12:00pm, 3:00pm EDT
February 22, 2018 (Thursday) 5:00pm EDT, 8:00pm EDT
Please Note: Students who apply to the Four-Year Nursing Program after February 11 who have not completed the CASPer test will not be considered for Nursing. Students without CASPer scores will be deemed to have an incomplete application and will be processed for second choice ONLY.  

Registration:
StFX applicants will need to create an account at takeCASPer.com. 
To register for the CASPer test students will use their StFX Student ID and a government-issued photo ID.
Students will receive their StFX ID# by email once a Nursing application has been submitted.
Test Fees
CASPer fees are paid online at takeCASPer.com at the time the test is booked.
The cost to take the CASPer assessment is $40 (CAD)
A fee to distribute your results to the institutions you select - $10 (CAD) per school. 
For more information on CASPer fees please visit takeCASPer.com.

Test Structure
The CASPer test comprises 12 sections of video and written scenarios. Following each scenario, you will be required to answer a set of probing questions under a strict time limit.
No studying is required for CASPer, although you may want to familiarize yourself with the test structure at takeCASPer.com. 
Technical Requirements
CASPer test takers are responsible for securing access to a computer on the selected test date with the following:
Audio capabilities
Webcam
Reliable internet connection
Please note that CASPer's policy states no exceptions will be provided for applicants unable to take CASPer online due to being located at sites where internet is not reliable due to technical or political factors. Tests cannot be rescheduled once the content has been viewed.
Accommodations
Applicants should be aware that requests can be made if an accommodation is required for the assessment. A formal request and supporting documentation must be provided at least three weeks in advance of the applicant taking the test, in order to allow sufficient time for document review and a decision on appropriate accommodation.
Please visit takeCASPer.com or email support@takecasper.com for more information."""
            yield item
        except Exception as e:
            with open("./error/" + item['university'] + item['degree_level'] + ".txt", 'a', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

    def parse_modules(self, modulesUrl):
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"Cookie": "_ga=GA1.2.200356326.1523266597; _gid=GA1.2.859987246.1523266597; ASPSESSIONIDQCDDCTTR=NDMFBBIBMGHIHMEPILJCDOGH",
"Host": "mesamis.stfx.ca",
"Referer": "http: //sites.stfx.ca/registrars_office/Course_Timetable.html",
"Upgrade-Insecure-Requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",}
        data = requests.get(modulesUrl, headers=headers)
        response = etree.HTML(data.text)
        # print(response)
        modules = response.xpath("//table[@cellpadding='3']//text()")
        # print("---", modules)
        modules = ''.join(modules).strip()
        # print("modules1: ", modules)
        return modules