# -*- coding: utf-8 -*-
import scrapy
import re
from scrapymodule_Canada.clearSpace import clear_space, clear_space_str
from scrapymodule_Canada.getItem import get_item
from scrapymodule_Canada.getTuition_fee import getTuition_fee
from scrapymodule_Canada.items import ScrapymoduleCanadaItem


class UMBenSchoolSpider(scrapy.Spider):
    name = "umBen"
    start_urls = ["http://umanitoba.ca/student/admissions/programs/index.html"]
    allow_domains = ['umanitoba.ca']
    # print(len(start_urls))
    start_urls = list(set(start_urls))
    # print(len(start_urls))

    def parse(self, response):
        links = response.xpath("//div[@id='centerInfo']/dl/blockquote/p/a/@href").extract()
        # print(len(links))
        links = list(set(links))
        # 113
        # print(len(links))
        for link in links:
            if "/student/admissions/programs/" in link:
                url = "http://umanitoba.ca" + link
                yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        item = get_item(ScrapymoduleCanadaItem)
        item['university'] = "University of Manitoba"
        item['country'] = 'Canada'
        item['website'] = 'http://umanitoba.ca/'
        item['url'] = response.url
        item['degree_level'] = "0"
        print("===========================")
        print(response.url)
        try:
            # 地点
            location = response.xpath(
                "//text()").extract()
            location = ''.join(location)
            # item['location'] = location
            # print("item['location']: ", item['location'])

            programmeDepartment = response.xpath(
                "//div[@id='centerHeader']//text()").extract()
            # print("programmeDepartment: ", programmeDepartment)

            item['programme'] = ''.join(programmeDepartment)
            if "-" in ''.join(programmeDepartment):
                programmeDepartment = ''.join(programmeDepartment).split("-")
                # 专业
                item['programme'] = programmeDepartment[-1]
                # 学院
                item['department'] = programmeDepartment[0]
            elif ":" in ''.join(programmeDepartment):
                programmeDepartment = ''.join(programmeDepartment).split(":")
                # 专业
                item['programme'] = programmeDepartment[-1]
                # 学院
                item['department'] = programmeDepartment[0]
            elif "&" in ''.join(programmeDepartment):
                programmeDepartment = ''.join(programmeDepartment).split("&")
                # 专业
                item['programme'] = programmeDepartment[-1]
                # 学院
                item['department'] = programmeDepartment[0]
            # print("item['programme']: ", item['programme'])
            # print("item['department']: ", item['department'])

            # overview
            overview = response.xpath(
                "//*[contains(text(),'Program description')]/../../following-sibling::p[1]//text()").extract()
            overview = ''.join(overview)
            item['overview'] = overview
            # print("item['overview']: ", item['overview'])

            # allcontent    //div[@id='centerInfo']
            allcontent = response.xpath(
                "//div[@id='centerInfo']//text()").extract()
            clear_space(allcontent)
            # print("allcontent: ", allcontent)

            # degree_type
            if "Degree options" in allcontent:
                degree_typeIndex = allcontent.index("Degree options")
                if "Program\xa0options" in allcontent[degree_typeIndex:]:
                    degree_typeIndexEnd = allcontent.index("Program\xa0options")
                    degree_type = allcontent[degree_typeIndex+2:degree_typeIndexEnd]
                    # print("degree_type1: ", degree_type)
                    degree_typeStr = ""
                    if len(degree_type) > 2:
                        degree_typeStr = degree_type[0] + "," + degree_type[1] + "\n" + ','.join(degree_type[2:])
                    else:
                        degree_typeStr = ','.join(degree_typeStr)
                    item['degree_type'] = degree_typeStr
                elif "Interesting courses and unique opportunities" in allcontent:
                    degree_typeIndexEnd = allcontent.index("Interesting courses and unique opportunities")
                    degree_type = allcontent[degree_typeIndex+2:degree_typeIndexEnd]
                    # print("degree_type2: ", degree_type)
                    degree_typeStr = ""
                    if len(degree_type) > 2:
                        degree_typeStr = degree_type[0] + "," + degree_type[1] + "\n" + ''.join(degree_type[2:])
                    else:
                        degree_typeStr = ''.join(degree_typeStr)
                    item['degree_type'] = degree_typeStr
            # print("item['degree_type']: ", item['degree_type'])
            durationContent = item['degree_type']
            if len(item['degree_type']) != 0:
                detype = re.findall(r"([A-Z]\.\w+\.\s\(\w+\.\))|([A-Z]\.\w+\.)|([A-Z]\.\s\w+\.)", item['degree_type'])
                # print("detype: ", detype)
                if len(detype) != 0:
                    for i in range(len(detype)):
                        detype[i] = ''.join(list(detype[i]))
                    item['degree_type'] = ', '.join(detype)
            # print("item['degree_type']: ", item['degree_type'])

            duration = re.findall(r"(\d\.\d+\syears)|(\d\syears)", durationContent)
            print("duration: ", duration)
            if len(duration) != 0:
                for i in range(len(duration)):
                    duration[i] = ''.join(list(duration[i]))
                item['duration'] = ', '.join(duration)
            print("item['duration']: ", item['duration'])
            # modules
            if "Interesting courses and unique opportunities" in allcontent:
                degree_typeIndex = allcontent.index("Interesting courses and unique opportunities")
                if "Professional opportunities" in allcontent[degree_typeIndex:]:
                    degree_typeIndexEnd = allcontent.index("Professional opportunities")
                    degree_type = allcontent[degree_typeIndex:degree_typeIndexEnd]
                    item['modules'] = '\t'.join(degree_type)
            # print("item['modules']: ", item['modules'])

            # career
            if "Professional opportunities" in allcontent:
                degree_typeIndex = allcontent.index("Professional opportunities")
                if "Admission Requirements" in allcontent[degree_typeIndex:]:
                    degree_typeIndexEnd = allcontent.index("Admission Requirements")
                    degree_type = allcontent[degree_typeIndex:degree_typeIndexEnd]
                    item['career'] = '\t'.join(degree_type)
                elif "Admission requirements" in allcontent[degree_typeIndex:]:
                    degree_typeIndexEnd = allcontent.index("Admission requirements")
                    degree_type = allcontent[degree_typeIndex:degree_typeIndexEnd]
                    item['career'] = '\t'.join(degree_type)
            # print("item['career']: ", item['career'])

            # http://umanitoba.ca/student/admissions/media/General_requirement_sheet_china.pdf
            item['IELTS'] = "6.5"
            item['TOEFL'] = "86"
            item['TOEFL_L'] = "20"
            item['TOEFL_S'] = "20"
            item['TOEFL_R'] = "20"
            item['TOEFL_W'] = "20"

            item['ACT'] = """NO ACT/SAT REQUIRED
Students applying from the United States are not required to
present ACT/SAT results as part of their application. All admission
decisions are made on the basis of final high school grades."""
            #
            item['how_to_apply'] = """Application Process
Preparing to apply 
Choose an undergraduate program 
Explore the many programs available to you. Review the complete list of programs we offer and consider your long-term career and degree goals before making your choice. For information on career choices, visit our Career Services area. Students applying for admission from high school will often begin their university studies in University 1 as a first step to their desired program. 
Review the entrance requirements
The requirements for all of our programs are found in our admissions requirements section. If you are not sure if you meet these requirements, contact our office for advice. 
Check available terms and application deadlines
The terms and deadlines for all of our programs are listed in our apply for admission section. Your application and fee must be submitted online or postmarked by the deadline to be considered. Note that some programs will continue to accept in-person paper applications after the online application process is closed. If you miss the deadline for your preferred program, check with our office for alternate suggestions. 
Apply

Applying online is easy. The online application guide is designed to assist you in applying to the undergraduate programs offered at the University of Manitoba. 
Make sure you have the following information available before you begin the online application: 

Basic biographical information such as address, date of birth, immigration details if not born in Canada, etc. You will require an email address; if you do not already have one, you can obtain a free address at any of a number of sites including hotmail.com, yahoo.com or gmail.com. 
Details of your current and prior education including starting and end dates. 
A valid VISA or MasterCard if you wish to pay the required application fee by credit card. You will also have the option to complete the application form online and submit the application fee by mail (cheque or international money order in Canadian funds made payable to the University of Manitoba) or in person at our office (cheque, money order, cash, or debit card). Both the application form and the application fee must be received in our office by the admission deadline. 

APPLY NOW
Offer & Acceptance
Acknowledgement 
Applicants will receive an acknowledgement email detailing required documentation within a few weeks of the receipt of their application by the Admissions Office. Make note of your Admission Officer's name and contact information, and your U of M ID and Applicant Numbers for any future questions about your application.
Admission Offer
You will receive a notice of decision once all required documentation has been received and your admission has been assessed completely.
Acceptance
All students who are offered admission will be required to confirm their acceptance to finalize the admission process. In some cases, students will be required to submit a non-refundable deposit on their tuition fees or to submit other documentation to hold their position. You will receive details regarding deposits, documentation due dates, and details on how to confirm the acceptance of your offer with your formal offer of admission.
Additional Information
Required Documentation
Applicants must send in any documents or information requested in the acknowledgement notification as quickly as possible. Generally, applications must be complete by July 7 to be considered for September admission. (Some faculties will have different deadlines as detailed in their Applicant Bulletins or the acknowledgement letters). Photocopies are not accepted. It is recommended that original documents be sent by registered mail or courier to prevent loss. Original documents, such as marriage or birth certificates, will be returned to applicants. Other original documents may be returned if the request is made by October 1 (for Fall applications). Transcripts and other academic documents become University property and will not be returned. 
Alternate choice of program
Any student who applies for admissions to a Direct Entry Program other than University 1, will be automatically be considered for admission to University 1 as their alternate program. Students must complete a second application form (online or paper) and pay a second application fee, to be considered for admission to any other alternate program. The second application must be submitted by the appropriate application deadline. You do not need to wait for the admission decision on your first choice to apply for an alternate program.
Next Steps
To learn more about applying for residence, course selection and registration, and Student Services visit our Next Steps page. """
            item['Application_link'] = "http://umanitoba.ca/student/admissions/application/deadlines/application-process.html"

            item['deadline'] = "http://umanitoba.ca/student/admissions/application/index.html"
            item['tuition_fee'] = "http://umanitoba.ca/student/admissions/finances/tuition-fees.html"
            item['chinese_requirements'] = "http://umanitoba.ca/student/admissions/media/General_requirement_sheet_china.pdf"
            item['application_fee'] = "120"
            yield item
        except Exception as e:
            with open("./error/" + item['university'] + item['degree_level'] + ".txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

