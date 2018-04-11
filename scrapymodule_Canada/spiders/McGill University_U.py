# -*- coding: utf-8 -*-
import scrapy
import re
from scrapymodule_Canada.clearSpace import clear_space, clear_space_str
from scrapymodule_Canada.getItem import get_item
from scrapymodule_Canada.getTuition_fee import getTuition_fee
from scrapymodule_Canada.items import ScrapymoduleCanadaItem


class MUBenSchoolSpider(scrapy.Spider):
    name = "muBen"
    start_urls = ["http://www.mcgill.ca/undergraduate-admissions/programs"]
    # print(len(start_urls))
    start_urls = list(set(start_urls))
    # print(len(start_urls))

    def parse(self, response):
        # //div[@id='tabs-2']/div[@class='paging-group']/div[@class='alphabetic-group']/ul[@class='programs-group']/li/a/@href
        links = response.xpath(
            " //div[@id='tabs-2']/div[@class='paging-group']/div[@class='alphabetic-group']/ul[@class='programs-group']/li/a/@href").extract()
        # print(len(links))
        links = list(set(links))
        # 265
        # print(len(links))
        for link in links:
            url = "http://www.mcgill.ca" + link
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        item = get_item(ScrapymoduleCanadaItem)
        item['university'] = "McGill University"
        item['country'] = 'Canada'
        item['website'] = 'http://www.mcgill.ca/'
        item['url'] = response.url
        item['degree_level'] = "0"
        item['TOEFL_code'] = item['SAT_code'] = item['ap'] = "0935-00"
        print("===========================")
        print(response.url)
        try:
            # 地点
            item['location'] = "Montreal, Quebec, Canada"
            # print("item['location']: ", item['location'])

            # 专业
            programme = response.xpath(
                "//div[@class='details']/h1//text()").extract()
            programme = ''.join(programme)
            item['programme'] = programme
            print("item['programme']: ", item['programme'])

            # 学院 department
            department = response.xpath(
                "//span[@class='value faculty']//text()").extract()
            department = ', '.join(department)
            item['department'] = department
            # print("item['department']: ", item['department'])

            # 学位类型 //span[@class='value degree']
            degree_type = response.xpath(
                "//span[@class='value degree']//text()").extract()
            degree_type = ', '.join(degree_type)
            item['degree_type'] = degree_type
            # print("item['degree_type']: ", item['degree_type'])

            # //div[@class='description']/p[position()<last()-2]
            overview = response.xpath(
                "//div[@class='description']/p[position()<last()-1]//text()").extract()
            overview = ''.join(overview).strip()
            item['overview'] = overview
            # print("item['overview']: ", item['overview'])

            # modules
            modules = response.xpath(
                "//div[@class='description']/div//text()").extract()
            clear_space(modules)
            modules = '\n'.join(modules).strip().replace("\n\n", "\n").strip()
            item['modules'] = modules
            # print("item['modules']: ", item['modules'])

            if item['programme'] == "Architecture":
                # Architecture portfolio    March 7
                item['deadline'] = "March 7"
            else:
                item['deadline'] = "January 15"

            if item['department'] == "Faculty of Medicine":
                item['application_fee'] = "150.5"
            elif item['department'] == "Schulich School of Music":
                item['application_fee'] = str(107.5+66.17)
            elif item['degree_type'] == "Bachelor of Education":
                item['application_fee'] = str(107.5+33.09)
            else:
                item['application_fee'] = "107.5"

            item['tuition_fee'] = "16373 - 42027"
            item['chinese_requirements'] = """(PRC) Senior High School Graduation Diploma
Applicants will be considered for admission on their high school transcript (Grades 1, 2 and midyear grade 3) and all available results of the Huikao exams. Note that SAT cannot be used as a substitute for the Huikao/Academic Proficiency Test (APT).
The minimum requirements normally are averages of 85% or higher in each year and in all prerequisite courses. Many programs are more competitive and will require higher grades; applicants who present the minimum requirements are not guaranteed admission.
View prerequisites by program.
Applicants from Chinese provinces where the Huikao is not offered must present additional external information of their academic credentials, such as SATI and SATII scores. If admitted to McGill, you must arrange for your school to send to McGill University an official final transcript of your complete high school record, the graduation certificate, and all final HUIKAO results.
If you write the GAOKAO, you must make arrangements to forward to us the final official results.
If admitted, you are expected to maintain your level of academic performance through to the completion of your pre-McGill studies."""
            item['average_score'] = "85"
            item['IELTS'] = "6.5"
            item['IELTS_L'] = "6"
            item['IELTS_S'] = "6"
            item['IELTS_R'] = "6"
            item['IELTS_W'] = "6"

            if item['degree_type'] == "Bachelor of Education" or item['department'] == "Desautels Faculty of Management":
                item['TOEFL'] = "100"
            elif item['degree_type'] == "Bachelor of Music":
                item['TOEFL'] = "79-80"
            else:
                item['TOEFL'] = "90"
                item['TOEFL_L'] = "21"
                item['TOEFL_S'] = "21"
                item['TOEFL_R'] = "21"
                item['TOEFL_W'] = "21"

            item['ACT_code'] = "5231"
            item['IB'] = """Applicants will be considered for admission on their high school transcript and predicted IB results or, if already completed, on the final IB Diploma results. The Diploma with grades of 5 or better on each Higher and Standard Level subject is the minimum expected for most programs. Many programs are more competitive and will require higher grades.
Note: The Math Studies course is not acceptable for programs where math is a required prerequisite.
View prerequisites by program and minimum grades required for admission in 2017.
If admitted, you are expected to maintain your level of academic performance through to the completion of your pre-McGill studies.
A maximum of 30 credits of advanced standing may be granted for the International Baccalaureate Diploma"""
            item['application_documents'] = """Copy of Senior high school transcript, including final 1st semester results for Senior 3, or completed transcript if already graduated
All completed Huikao/ Academic Proficiency Test (APT) results.  Note that SAT cannot be used as a substitute for the Huikao/Academic Proficiency Test (APT).
If you are from a province where the Huikao is not offered (Hubei) then additional external examination information, such as SATI and SATII scores, must be presented.
Gaokao, if written"""
            item['how_to_apply'] = """Tips for completing your application:
1) Be prepared
Make sure you have read through the admissions requirements and deadlines to determine whether you meet the entrance requirements. Be aware of application and document submission deadlines – priority will be given to students who apply on time!

2) Keep track of your Login ID and PIN
At the beginning of the application, you will be asked to select a Login ID and PIN.  By keeping a record of your ID and PIN as you can log in and out of your application as many times as you need to before you submit it.  However, to make a change after you have submitted your application, you must submit a modification request.

3) Provide a valid and reliable email address
After you submit your application, you will receive a confirmation email with important information on your Minerva account and how to complete your file.  As such, it is very important that you provide a reliable email address.

4) Use both your program choices
It does not matter what order you use. Both choices will be evaluated and you will receive a separate decision for each program choice (though you may not receive these decisions at the same time). If you want to apply to more than two programs, you will need to submit – and pay for – another application. 

5) Tell us who can obtain application information on your behalf
If you would like a parent, guardian, family member or friend to be able to contact McGill on your behalf and obtain information about your application, you must include their name in the “Disclosure information” section of the application.  Otherwise, privacy laws prevent us from sharing your information with anyone other than you and staff from your school.

6) Have on hand the following information as it may be helpful in filling out the application:
- Test scores (if you are required to submit tests, such as TOEFL, IELTS, SAT, etc…)
- Quebec Permanent Code (if you have studied at any level in Quebec)
- Ontario Universities Application Centre number (if available)

7) Have a credit card to pay the application fee
At the undergraduate level, a non-refundable application fee of $107.50 ($150.50 for the Faculty of Medicine) is required for up to two program choices. You will be able to preview your application and print a copy before you pay the application fee. You may also print a confirmation of your credit card payment for your records.
Note: Applicants to the B.Ed. TESL program must pay an additional testing fee of $33.09. Applicants to the Schulich School of Music must pay an additional audition fee of $66.17.

8) Review your Minerva confirmation
You will receive an email acknowledgment within 48 hours after submitting your application for admission.  The login information provided in the email will allow you to access your Minerva account to view your application status and upload supporting documents.  It is your responsibility to verify your status and ensure the completion of your application."""
            item['Application_link'] = "https://horizon.mcgill.ca/pban1/hzskalog.P_DispAppLogin?p_langue=01"
            yield item
        except Exception as e:
            with open("./error/" + item['university'] + item['degree_level'] + ".txt", 'a', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

