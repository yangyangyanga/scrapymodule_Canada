# -*- coding: utf-8 -*-
import scrapy
import re
from scrapymodule_Canada.clearSpace import clear_space, clear_space_str
from scrapymodule_Canada.getItem import get_item
from scrapymodule_Canada.getTuition_fee import getTuition_fee
from scrapymodule_Canada.items import ScrapymoduleCanadaItem
import requests
from lxml import etree

# 布鲁克大学
class BUBenSchoolSpider(scrapy.Spider):
    name = "buBen"
    start_urls = ["https://brocku.ca/programs/"]
    # print(len(start_urls))
    start_urls = list(set(start_urls))
    # print(len(start_urls))

    def parse(self, response):
        links = response.xpath("//div[@id='content']/div[@id='grid']/div/div[@class='content']/a/@href").extract()
        # print(len(links))
        links = list(set(links))
        # 76
        # print(len(links))
        for url in links:
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        item = get_item(ScrapymoduleCanadaItem)
        item['university'] = "Brock University"
        item['country'] = 'Canada'
        item['website'] = 'https://brocku.ca/'
        item['url'] = response.url
        item['degree_level'] = "0"
        # https://brocku.ca/admissions/english-proficiency/
        item['TOEFL_code'] = item['SAT_code'] = item['ap'] = "0895"
        print("===========================")
        print(response.url)
        try:
            # 学院
            department = response.xpath(
                "//div[@class='specs']//p/a[1]//text()").extract()
            department = ''.join(department)
            item['department'] = department
            # print("item['department']: ", item['department'])

            # 专业
            programme = response.xpath(
                "//h1[@class='entry-title']/text()").extract()
            programme = ''.join(programme)
            item['programme'] = programme
            # print("item['programme']: ", item['programme'])

            # degree_type
            degree_type = response.xpath(
                "//div[@class='specs']//p/a[2]//text()").extract()
            degree_type = ''.join(degree_type)
            item['degree_type'] = degree_type
            # print("item['degree_type']: ", item['degree_type'])

            # overview
            overview = response.xpath(
                "//div[@class='entry-content']//text()").extract()
            overview = ''.join(overview).strip()
            item['overview'] = overview
            # print("item['overview']: ", item['overview'])

            career = response.xpath(
                "//h2[contains(text(),'Career outcomes')]/..//text()").extract()
            career = ''.join(career).strip()
            item['career'] = career
            # print("item['career']: ", item['career'])

            # //html//div[@class='col2']//p[2]/a[1]/@href
            # 学位描述
            degree_descriptionUrl = response.xpath("//a[contains(text(),'Program website')]/@href").extract()
            if len(degree_descriptionUrl) != 0:
                degree_description = self.parse_degreeDescription(''.join(degree_descriptionUrl))
                item['degree_description'] = degree_description
            print("item['degree_description']: ", item['degree_description'])

            item['IELTS'] = "6.5"
            item['IELTS_L'] = "6"
            item['IELTS_S'] = "6"
            item['IELTS_R'] = "6"
            item['IELTS_W'] = "6"
            item['TOEFL'] = "88"
            # item['TOEFL_L'] = "20"
            item['TOEFL_S'] = "21"
            # item['TOEFL_R'] = "20"
            item['TOEFL_W'] = "21"

            # 学历认证链接
            # https://brocku.ca/admissions/international/requirements-by-country/
            item['diploma_certification'] = "(Grade 12) Senior High School Graduation Certificate (3 Years) plus final transcript showing Grade 12 first and second term grades"

            item['IB'] = "https://brocku.ca/admissions/international/international-secondary-school-student/"

            item['chinese_requirements'] = """General admission requirements:
Senior Secondary school credential appropriate for entry to university in your home country;
Academically rigorous grade 12 year
Minimum B- average (higher for some programs);
English Language proficiency requirements must be satisfied"""
            item['how_to_apply'] = """How and when to apply
Ready to apply for admission to Brock? Use the four steps below to apply for the program that’s right for you. Click here to go directly to the application.

Step 1
Determine the type of applicant you are, as well as your admission requirements.
UndergraduatesTeacher EducationGraduate studiesInternational undergraduatesUndergraduates
Ontario secondary school
Out-of-province secondary school
University graduate or transfer
College graduate or transfer
All other students (including returning Brock Students and Nursing ‘Change of Majors’)
Teacher Education
Initial Consecutive Teacher Education
Concurrent Teacher Education
Technological Teacher Education
Continuing Teacher Education (Additional Qualifications)
Adult Education
Aboriginal Education
Masters Preparation Certificate in Education (MPCE)
Undergraduate Education
Graduate Education
Graduate studies
Go to the Graduate Studies page
International undergraduates
Ontario secondary school curriculum
Out-of-province curriculum
International secondary school
University graduate or transfer
College graduate or transfer
Intensive English Language Program (IELP)/Undergraduate Conditional Program (ESL bridging)
Academic Transitions (ACT)

Step 2
If applying using a Brock internal application, be sure to carefully read the following information beforehand. Similar information can be found on the OUAC application.
Technical details
An incomplete application will expire two weeks after first activated. If you cannot complete the application immediately, an email will be sent with a link allowing you future access to the application.
Make Brock a safe sender
Email is the primary communication tool for Admissions at Brock University. If you have not received an acknowledgement email thanking you for applying within four business days of submitting your application, there may be a problem with your email address. Here are some common problems:
You have an email address that ends in qq.com. The qq.com server is rejecting Brock emails. We advise that you contact central@brocku.ca with a different email address. If you have applied through OUAC, add a different address using your OUAC account.
Your mailbox could be full.
You have a new email address and haven’t told us. Contact central@brocku.ca with your new email address. If you have applied through OUAC, add a new address using your OUAC account.
Add Brock to your friends/safe list (see below).
In order to avoid problems after submitting your application, please add the brocku.ca domain to your safe senders email list and check your junk email regularly. Ensure your junk folder is not set to automatically delete messages.
Hotmail/Outlook users:
Please add us to your safe senders list using these directions:
Log into Hotmail.
In the top right of your inbox, click on the settings icon wheel.
Under Junk Email, click Safe and Blocked Senders or Safe Senders.
Type in central@brocku.ca, in the Sender or domain to mark as safe entry field.  
Gmail users:
Gmail accounts have been redesigned to automatically filter communications from large institutions like Brock University and categorize them as Promotions. By creating a filter for emails from brocku.ca, you will ensure that all correspondence with our office is delivered to your primary inbox. Please add brocku.ca to your safe sender list in Gmail by following these instructions:
Log into Gmail.
Click on the settings icon (top right of screen – it looks like a gear).
Choose Settings from the list.
Click Filters at the top of the page.
Click Create a new filter.
Type brocku.ca in the From box in the next window.
Click Create filter with this search at the bottom of the page.
Click Never send it to Spam and Always mark it as important.
Click Create filter button.
Application fees
You must have a valid credit card to apply.
Once your application is submitted and paid, you cannot make changes.
Please do not submit a new application if you wish to make a change. Email central@brocku.ca
Application fee is non-refundable.
If in doubt whether you are using the correct application, contact central@brocku.ca
  Application fees:
OUAC 101, 105, TEAS: see OUAC website.
Auditor, LOP, part-time, mature, upgrading, adult education: $55
Continuing (AQ) Teacher Education (in-service): no fee
IELP Conditional/undergraduate application: $400 ($100 assessment fee, $50 service fee, $250 IELP application fee)
Programs with supplementary document requirements
Dramatic Arts: Mandatory DART Invitational (audition)
Game Design: Statement of interest
Game Programming: Statement of interest
Mathematics and Statistics: Accelerated mathematics study stream
Music: Audition
Visual Arts (Studio Art): Portfolio
Submission of documents
Unofficial documents may be used for admissions assessment. Official documents must be submitted in order to begin studies.
Unofficial documents are copies of documents that have been in your possession and were issued by the awarding institution or body. These can be uploaded using your applicant portal. For help uploading documents please see: How to Upload Documents
Official documents are issued by the awarding institution or body and are sent from the awarding institution or body directly to the Office of the Registrar. These may never be in your possession, and cannot be uploaded using your applicant portal.
How to submit documents for assessment
Once you apply, you will be notified of the steps required to log into your applicant portal, and the documents required for assessment. Upload unofficial documents using the applicant portal. Hard copies can be submitted by mail but uploading is preferable.
If you have already completed your schooling, you may choose to submit final official documents for assessment.
Ontario universities may require international undergraduate applicants to have official academic transcripts submitted directly to World Education Services (WES) Canada for verification as part of the admission process. Universities will notify applicants about specific submission requirements through WES Canada. While Brock University does not require applicants to submit documents through WES Canada, we will accept and consider official any authenticated and verified documents received directly from them.
Learn more about WES.
How to submit final official documents
If you received an offer of admission based on unofficial documents, you will be asked to have official final academic documents/transcripts sent directly from each secondary school, college, university or proper issuing authority to:
Brock University, Office of the Registrar,
1812 Sir Isaac Brock Way
St. Catharines, ON
L2S 3A1
Brock University reserves the right to withdraw the final offer of admission or revoke registration if there is a discrepancy between documents originally submitted and the official, final documents/transcripts submitted to Brock either directly or via WES Canada.
Document requirements
Applicants applying from institutions outside of Canada must provide appropriate academic information to ensure an accurate assessment of your qualifications including:
Academic transcript(s) bearing the original institutional seal and/or signature in the original language confirming all study.
A transcript should include:
official confirmation regarding the years of study;
official confirmation of the credential awarded, and the date the credential was awarded;
official confirmation of the credit system or course weight;
official confirmation of completed courses/subjects and grades.
If you have completed a post-secondary credential, please submit notarized copies of any diplomas.
If the above information is not printed on your academic transcript(s) and is not part of the transcript legend accompanying your transcript, please include the missing information in an original letter from your academic institution. Also include a certified translation if the letter is in a language other than English. This will help us assess your studies accurately.
WES Canada is an excellent resource for internationally educated applicants to find out which documents are necessary for each country.
Important: When uploading academic transcripts, be sure to include the front and back of the document where applicable.
Course descriptions/syllabus for transfer credit assessment
If you have attended college or university and wish to have your previous study considered for recognition (transfer credit), you may be required to submit course descriptions or a complete syllabus (detailed outline of a course). Goodman School of Business applicants will be asked for detailed courses descriptions for any previous study. All other applicants will be asked as necessary.
Translations
Translations of academic documents will be accepted from one of the following:
the issuing institution or school;
the consulate, high commission or embassy to Canada of the country where the documents were issued;
a Canadian embassy, consulate, high commission in the country from which you emigrated;
a translator accredited by a professional association of translators in Canada. To obtain the name of an accredited translator contact the Association of Translators and Interpreters of Ontario (ATIO) at 1-800-234-5030 OR 613-241-2846, email: infor@atio.on.ca or visit ATIO;
a translator who has received accreditation through a federal, provincial or municipal government in Canada.
If the ATIO is unable to provide a translator for the language you require, you may contact COSTI-IIAS Immigrant Services at 416-651-1496 or email languages@costi.org. The translator must include a photocopy of the original document(s) from which the translation was prepared, as well as an original statement indicating:
that the translation is accurate and authentic;
that the translator belongs to one of the categories listed above (identification number and/or seal, name, address, and telephone number required);
and including printed name and signature of the translator.
Deferral requests
Brock University will grant a deferral where extenuating circumstances warrant one but the decision is at the discretion of the University and is not automatic. Deferrals will be considered only after a Brock University offer has been accepted and the University receives final grades. Contact central@brocku.ca for further information and the appropriate deferral request form.

Step 3
Applications are completed via Ontario Universities Application Centre (OUAC) or an internal Brock application, unless you have been registered at Brock University in the past.
Applicants who were previously registered at Brock University must contact the Admissions Office for the appropriate application information. Have you ever:
1) Studied at Brock University on a Letter of Permission, or
2) Registered in courses previously but dropped them (even if you had never attended classes), or
3) Registered as a part-time or Audit student?
4) Please note that if you apply with the Brock University Online Application, the application fee is non refundable.
If any of the 4 apply to you, please email central@brocku.ca or call 905 688 5550 x 3052
ApplicationsUndergraduatesTeacher EducationGraduateInternational undergraduatesUndergraduates
Applicant
Current Ontario secondary school
Application
OUAC 101 application
Application deadline
January 17, 2018 (Fall term) (applications continue to be accepted where space available)
Ontario secondary school graduates; out-of-province secondary school; university graduate or transfer; college graduate or transfer; homeschooled
OUAC 105D application
June 1 (Fall term) (applications continue to be accepted where space available)
BScN Nursing
OUAC 105D application
Application Deadline: February 1
Document Deadline: February 8
Auditor
Internal Brock application
Two weeks before start of term (Fall, Winter, Spring terms)
Letter of permission (incoming)
Internal Brock application
Two weeks before start of term (Fall, Winter, Spring terms)
Part-time/mature
Internal Brock application
Two weeks before start of term (Fall, Winter, Spring terms)
Upgrading
Internal Brock application
Two weeks before start of term (Fall, Winter, Spring terms)
Teacher Education
Applicant
Aboriginal Education
Application
Learn more about Aboriginal Education
Application deadline
Adult Education
Internal Brock application
July 15 (Fall term)
Nov. 15 (Winter term)
Continuing (AQ) Teacher Education (in-service)
Internal Brock application
You must apply and be admitted before registering in a course
Initial Consecutive Teacher Education
OUAC TEAS application
Dec. 1 (Fall term)
Professional Master’s Preparation Certificate in Education (MPCE)
Learn more about MPCE
Technological Education Teacher Education
Learn more about Technological Education and Teacher Education
May 15, 2018 (Winter 2019 term)
Graduate
Applicant
Graduate studies
Application
Learn more about Graduate Studies
Application deadline
International undergraduates
Applicant
Ontario secondary school curriculum
Application
OUAC 101
Application deadline
January 17, 2018 (Fall term) (applications continue to be accepted where space available)
International:
Secondary school (out of province or international);
college graduate or transfer;
university graduate or transfer
Applying to more than one Ontario university:
OUAC 105F application
Deadline: April 1 for all programs with the exception of Game Design, Game Programming, Nursing and Sport Management.
After April 1, applications may be accepted under special circumstances and continue to be assessed where space is available and there is the likelihood of receiving a Study Permit in time for a September start. After April 1st contact: international@brocku.ca
Applying to Brock University only:
Internal Brock application
May 1: Fall term
Oct. 1: Winter term
Feb. 1: Spring term
BScN Nursing
Applying to more than one Ontario university:
OUAC 105F application
Application Deadline: February 1
Document Deadline: February 8
Applying to Brock University only:
Internal Brock application
Application Deadline: February 1
Document Deadline: February 8
Intensive English Language Program (IELP)/Undergraduate – Conditional Program (ESL bridging)
Internal Conditional application
No fixed deadline. (Admission for Fall, Winter, Spring terms) You will be admitted to the next available term.

Step 4
Connect with Admissions if you have questions or concerns about your application."""
            item['Application_link'] = "https://brocku.ca/admissions/apply/"
            item['deadline'] = "https://brocku.ca/important-dates/other-important-dates/"
            item['tuition_fee'] = "https://brocku.ca/safa/undergraduate-tuition-and-fees-2018-academic-year/#2017-ug-international7420-ef5cf380-e567"

            yield item
        except Exception as e:
            with open("./error/" + item['university'] + item['degree_level'] + ".txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

    def parse_degreeDescription(self, degree_descriptionUrl):
        # degree_description = ""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
        data  = requests.get(degree_descriptionUrl, headers=headers)
        response = etree.HTML(data.text)
        print("====", degree_descriptionUrl)
        degree_description = response.xpath("//html//div[@class='entry-content']/div[3]//text()")
        degree_description = ''.join(degree_description).strip()
        return degree_description
