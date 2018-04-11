# -*- coding: utf-8 -*-
import scrapy
import re
from scrapymodule_Canada.clearSpace import clear_space, clear_space_str
from scrapymodule_Canada.getItem import get_item
from scrapymodule_Canada.getTuition_fee import getTuition_fee
from scrapymodule_Canada.items import ScrapymoduleCanadaItem


class CUBenSchoolSpider(scrapy.Spider):
    name = "cuBen"
    start_urls = ["http://www.concordia.ca/academics/undergraduate.html"]
    # print(len(start_urls))
    start_urls = list(set(start_urls))
    # print(len(start_urls))

    def parse(self, response):
        links = response.xpath("//table[@id='degree_program_table']/tbody/tr/td[1]/a/@href").extract()
        # print(len(links))
        links = list(set(links))
        # print(len(links))
        for link in links:
            url = "http://www.concordia.ca" + link
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        item = get_item(ScrapymoduleCanadaItem)
        item['university'] = "Concordia University"
        item['country'] = 'Canada'
        item['website'] = 'http://www.concordia.ca/'
        item['url'] = response.url
        item['degree_level'] = "0"
        item['TOEFL_code'] = item['SAT_code'] = "0956"
        print("===========================")
        print(response.url)
        try:
            # degree_type
            department = response.xpath(
                "//div[@class='span8 ordinal-group-1']//a[2]//text()").extract()
            # print(department)
            if len(department) > 0:
                item['department'] = department[0]
            # print("item['department']: ", item['department'])

            # 专业
            programme = response.xpath(
                "//div[@class='span8 ordinal-group-1']/h1//text()").extract()
            programme = ''.join(programme)
            degree_type = re.findall(r"\([\w\s,]+\)", programme)
            degree_type = ''.join(degree_type)
            # print("degree_type: ", degree_type)
            item['degree_type'] = degree_type.strip().strip("(").strip(")")
            # print("item['degree_type']: ", item['degree_type'])

            programme = programme.strip()
            if degree_type != "":
                programme = programme.split(degree_type)
            item['programme'] = ''.join(programme).strip()
            print("item['programme']: ", item['programme'])

            # AP
            apDict = {'Art History': 'ARTH 200 (6)* or GFAR (6)', 'Biology': 'BIOL 201 (3) and BIOL 1st year level (3)', 'Calculus AB\xa0': 'MATH 203 (3), with exemption from MATH 201, 206 and 209*', 'Calculus BC': 'MATH 203 (3) and MATH 205 (3), with exemption from MATH 201, 206 and 209*', 'Chemistry': 'CHEM 205 (3) and CHEM 206 (3)', 'Chinese': 'MCHI 1st year level (6)', 'Computer Science A': 'COMP 248 (3)', 'Economics: Macroeconomics': 'ECON 203 (3)', 'Economics: Microeconomics': 'ECON 201 (3)', 'English Language and Composition': 'ENGL 1st year level (6)\xa0', 'English Literature and Composition': 'ENGL 1st year level (6)\xa0', 'Environmental Science': 'GEOG 1st year level (3)', 'French Language': 'FRAN 211 (6)\xa0', 'French Literature': 'FRAN 1st year level (6)', 'German Language and Culture': 'GERM 200 (6) with exemptions for GERM 201 and GERM 202', 'Government and Politics: Comparative': 'POLI 203 (3)', 'Government and Politics: United States': 'POLI 1st year level (3), with an exemption for POLI\xa0310', 'History: European': 'HIST 1st year level (6)', 'History: United States': 'HIST 251 (3) and HIST 253 (3)', 'Human Geography': 'GEOG 1st year level (3)', 'Italian Language and Culture': 'ITAL 200 (6) with exemptions for ITAL 201 and ITAL 202', 'Japanese': 'MODL 1st year level (6)', 'Latin': 'CLAS 1st year level (6)', 'Music Theory': 'MUSI A (3)\xa0', 'Physics 1': 'No transfer credit awarded', 'Physics 2': 'No transfer credit awarded', 'Physics 1 and Physics 2': 'No transfer credit awarded', 'Physics C (Mechanics)': 'PHYS 204 (3)', 'Physics C\xa0(Electricity and Magnetics)': 'PHYS 205 (3)', 'Psychology': 'PSYC 200 (6)', 'Spanish Language and Culture': 'SPAN 200 (6) with exemptions for SPAN 201 and SPAN 202', 'Spanish Literature and Culture': 'SPAN 200 (6) with exemptions for SPAN 201 and SPAN 202', 'Statistics': 'MATH 1st year level (6)', 'Studio Art: Drawing': 'SFAR A (6)', 'Studio Art :2-D Design:': 'SFAR A (6)', 'Studio Art: 3-D Design:': 'SFAR A (6)', 'World History': 'HIST 1st year level (6)'}
            item['ap'] = apDict.get(item['programme'])
            print("item['ap']: ", item['ap'])

            # overview
            overview = response.xpath(
                "//html//div[@class='parbase box section']/div[contains(@class,'c-sidebar-calltoaction bloc  link-color-dark')]/div[1]/div[position()<3]//text()").extract()
            overview = ''.join(overview).strip()
            item['overview'] = overview
            # print("item['overview']: ", item['overview'])

            # entry_requirements
            entry_requirements = response.xpath(
                "//a[@name='legend-expand'][contains(text(),'Admission requirements')]/../../following-sibling::div[1]//text()").extract()
            # clear_space(entry_requirements)
            entry_requirements = ''.join(entry_requirements).strip()
            item['entry_requirements'] = entry_requirements
            # print("item['entry_requirements']: ", item['entry_requirements'])

            IB = re.findall(r"International\sBacc.\s\(IB\):.{1,300}", entry_requirements)
            # print("IB: ", IB)
            item['IB'] = ''.join(IB).strip()
            # portfolio
            # //a[@name='legend-expand'][contains(text(),'Portfolio')]/../../following-sibling::div[1]
            portfolio = response.xpath(
                "//a[@name='legend-expand'][contains(text(),'Portfolio')]/../../following-sibling::div[1]//text()").extract()
            # clear_space(entry_requirements)
            portfolio = ''.join(portfolio).strip()
            item['portfolio'] = portfolio
            # print("item['portfolio']: ", item['portfolio'])

            # how_to_apply
            # //a[@name='legend-expand'][contains(text(),'Portfolio')]/../../following-sibling::div[1]
            how_to_apply = response.xpath(
                "//a[@name='legend-expand'][contains(text(),'Application procedures')]/../../following-sibling::div[1]//text()").extract()
            # clear_space(entry_requirements)
            how_to_apply = ''.join(how_to_apply).strip()
            item['how_to_apply'] = how_to_apply
            # print("item['how_to_apply']: ", item['how_to_apply'])

            # 开学日期
            # //a[@name='legend-expand'][contains(text(),'Application deadlines')]/../../following-sibling::div[1]//table//tr[1]/td[position()>1]
            start_date = response.xpath(
                "//a[@name='legend-expand'][contains(text(),'Application deadlines')]/../../following-sibling::div[1]//table//tr[1]/td[position()>1]//text()|//a[@name='legend-expand'][contains(text(),'Application deadlines')]/../../following-sibling::div[1]//table//th//text()|//a[@name='legend-expand'][contains(text(),'Applications deadlines')]/../../following-sibling::div[1]//table//tr[1]/td[position()>1]//text()").extract()
            start_date = ', '.join(start_date).strip()
            # print(start_date)
            sd = ""
            if len(start_date) != 0:
                if "Fall" in start_date:
                    sd += "January"
                if "Winter" in start_date:
                    sd += ", September "
            item['start_date'] = sd
            # print("item['start_date']: ", item['start_date'])

            # 截止日期
            # //a[@name='legend-expand'][contains(text(),'Application deadlines')]/../../following-sibling::div[1]//table//tr[3]/td[position()>1]
            deadline = response.xpath(
                "//a[@name='legend-expand'][contains(text(),'Application deadlines')]/../../following-sibling::div[1]//table//tr[3]/td[position()>1]//text()").extract()
            # clear_space(entry_requirements)
            deadline = ', '.join(deadline).strip()
            item['deadline'] = deadline
            # print("item['deadline']: ", item['deadline'])

            # 就业
            # //a[@name='legend-expand'][contains(text(),'Application deadlines')]/../../following-sibling::div[1]//table//tr[3]/td[position()>1]
            career = response.xpath(
                "//a[@name='legend-expand'][contains(text(),'Career opportunities')]/../../following-sibling::div[1]//text()|//a[@name='legend-expand'][contains(text(),'After your degree')]/../../following-sibling::div[1]//text()").extract()
            # clear_space(career)
            career = ' '.join(career).strip()
            item['career'] = career
            # print("item['career']: ", item['career'])

            item['application_fee'] = "100"
            item['tuition_fee'] = "16,373.40–22,112.10"
            item['chinese_requirements'] = "Senior Middle School Diploma plus Chinese National University Entrance Examinations (if available)"

            item['IELTS'] = "7"
            item['TOEFL'] = "90"
            item['other'] = """TOEFL iBT score between 75 and 89 with a minimum combined score of 34 for speaking and writing.\nIELTS score of 6.5 or 6 with no component score under 5.5"""

            #
            if item['how_to_apply'] == "":
                item['how_to_apply'] = """Undergraduate application instructions
This guide will lead you through the online application process.
Please note:
You may save your application at any point, allowing you to partially complete the process (if necessary) and return to it later. 
Be sure to have a valid credit card (Visa, MasterCard, American Express or Discover) or debit card (Scotiabank, Bank of Montreal, Royal Bank or TD Canada Trust) ready for the application fee ($100 CAD) and a valid email address for correspondence.
1. Start your application
Visit this page.
2. Level of study
Specify your level of study. Choose undergraduate.
3. Applicant category
We’d like to know a bit about your educational history. Choose one of the six categories that applies to you. If you are not currently enrolled in school, choose the option that best describes your most recent situation.
You are:
a Cegep student in Quebec with a DEC or who will obtain a DEC
a high school student (including these categories)
an Ontario student with an OUAC number
an Ontario student without an OUAC number
attending high school in a Canadian province or territory other than Quebec or Ontario
attending high school in the United States
attending high school outside of Canada and the US
a current or former student from another university or college
a current or former Concordia student
homeschooled
applying as a mature student
4. Term
Select the term you wish to apply to (Fall or Winter) and the year.
5. Biographical information
Provide your name, date of birth, first language, email address and other details. Please ensure that all information is accurate and matches all your official supporting documents. If you had to modify the spelling of your name when you created your Netname account, please correct your name here.
To answer the questions about languages if you are bilingual or multilingual, please choose the options that seem most appropriate to you. Your answers will not affect your application for admission in any way.
The email address you provide will be the one we use to communicate with you throughout the admissions process.
6. Contact information
You may specify a mailing address different from your home address.
You can change your contact information at a later date through MyConcordia.ca.
MyConcordia is the university’s main site for students to carry out key tasks related to their academic life, like checking course schedules and paying tuition. For future students, it’s also the place where you can check on the status of your application for admission. You’ll be able to log into MyConcordia once you’ve submitted your application.
7. Academic programs and academic plans
Select the academic program and the academic plan to which you’d like to apply. An Academic Program is the type of degree or certificate (Bachelor of Arts, Bachelor of Engineering, etc.) you plan to pursue. An Academic Plan is the specific subject you want to focus on (Major in Art History, Specialization in Biophysics, etc.)
If you are not sure exactly which plan you would like to apply to, browse our A-Z program guide to consider all your options. Remember, if you leave your application open with no activity for more than 20 minutes, you will be automatically signed out to protect your privacy. Click the Save and Exit button if you need to leave your application.
First choice
Click Search by subject. Choose a subject from the drop-down menu and then click search by subject again to display your options.
Using your three choices
You may indicate up to three academic program and academic plan choices on your application. We strongly recommend that you use all three choices. Your first choice should be your most preferred program and plan. If you are not admitted to your first choice, we automatically consider you for your next choice. Do not choose more than one plan in the same subject—if you apply to the Honours or Specialization plan and are not qualified, you will automatically be considered for the Major plan in the same subject.
Adding a second plan
“Add a second plan” allows you to add a minor or a second major (if you’re planning on doing a double major). Click Add a second plan and then click the magnifying glass to select the plan.
You are not required to choose a second plan.  
Some academic plans don’t permit you to take on a second academic plan, in which case you’ll see the note “no matching values are found.”
Co-operative Education (optional)
If you are interested in applying to the Institute for Co-operative Education, check off the Co-op box when choosing your program.
If you graduated from a high school outside of Quebec and plan to apply for Co-op, please contact the Institute directly as we normally only consider you for Co-op in your second year.
8. Academic history
Create a list of all the academic institutions you have attended, including high school, college, and/or university.
Click Select School to begin. If you cannot find your school using the School Name Search, click Return and check “I could not find my specific school.”
Please include the time period when you studied there (approximate dates are acceptable), and the degree or level that you have completed. Your acceptance, placement level or registration may be affected if you don’t disclose your entire secondary and post-secondary academic history.
9. Distinctions, honours and additional information
List your academic honours, distinctions and achievements, including International Baccalaureate or Advanced Placement courses.
If you have any gaps in your educational history timeline, tell us about your activities and work history since you last attended school. You may also wish to attach your curriculum vitae/resumé later in the application.
10. Courses
Indicate any courses that you have registered in for the current semester (meaning they won’t yet appear on your transcript).
Please also indicate any courses you plan to complete before starting at Concordia, like summer courses.
11. Attach documents
Please ensure that you have electronic copies of your documents ready to upload. You do not have to upload all the documents listed in the drop-down list, only the documents required to support your application.
File types that can be uploaded include:
Adobe Acrobat Document (*.pdf)
Image files (*.bmp, *.gif, *.jpg, *.jpeg, *.tif)
Microsoft Word Document (*.doc, *.docx)
Rich Text File (*.rtf)
Text File (*.txt)
File size can be no larger than 5 MB per document.
You may also add documents after the application has been submitted through the My Student Centre on MyConcordia.
Documents and “To Do List”
To see what documents we require for your application, go to MyConcordia.ca. Under My Student Centre, check the “To Do List" on the right hand side. Once you submit a required document, we will review your file again and remove that item from your “To Do List”. Please note that it may take up to 10 working days to update your file.
To see a list of what documents we’ve already received, under the To-Do list, click on the link “List of Documents Received.” The list of documents will be displayed as soon as they are uploaded. Fine Arts portfolios will not appear on the list.
12. Finalize your application
You’re almost finished!
Release of Information
Privacy rules prevent us from talking to anyone but you about your application, unless you authorize a specific person in this section. Once you are admitted, this person will no longer have access to your file.
Application Fee
To finalize your application, you need to agree to our terms and conditions, and pay a non-refundable application fee ($100 CAD) by credit card or debit card. Please note: we accept the following credit cards: Visa, MasterCard, American Express, Discover, and the following debit cards: Scotiabank, Bank of Montreal, Royal Bank or TD Canada Trust.
Once you click the “submit” button, you will receive a confirmation email with an attached PDF copy of your application within 24 hours. This email will include an eight-digit student ID number that you will use throughout your studies should you be accepted at Concordia.
If you didn’t get the confirmation email (and you can’t find it in your junk mail folder either), call us at 514-848-2424, extension 2668 or email study@concordia.ca. We will send you your student ID number."""
            item['Application_link'] = "http://www.concordia.ca/admissions/undergraduate/apply/instructions.html"
            item['application_documents'] = """Gather supporting documents
You can always upload documents after your application has been submitted.
All applicants must include the following documents:

Transcripts
Please upload unofficial copies of transcripts when you apply to Concordia because it speeds up the review of your application.
Uploaded transcripts, however, are not official transcripts. Official transcripts are documents sent directly from an institution to our Admissions Application Centre. Unless otherwise specified, we request official transcripts only once you are admitted.
Quebec Cegep applicants
If you include your permanent code on your application, you do not need to provide a copy of your Cegep transcript. Your permanent code allows us to obtain your official transcripts from the Conférence des recteurs et des principaux des universités du Québec (CREPUQ).
Ontario high school applicants
Ontario Universities’ Application Centre (OUAC): If you also applied to an Ontario university, you have an OUAC number and the OUAC will provide us with your high school transcripts.
Include a valid OUAC number for the current year in your web application
Winter term exception: OUAC does not send transcripts in the winter term. If you apply to Concordia for a winter term, please upload a copy of your transcript
If you didn’t apply through OUAC, please upload a copy of your transcript 
Other Canadian provinces/United States applicants
Upload copies of transcripts from all previous educational institutions.
If you are currently enrolled in school:
Submit the results of previous terms and a list of your current courses
Include mid-year grades if they’re available 
International applications
Upload a copy of your transcripts from all previous educational institutions
If you’re currently enrolled in school:
Submit the results of previous terms and a list of current courses you are currently registered in
Include mid-year grades if they’re available
All transcripts should be in the original language
Translation requirement: If your official transcript is in neither English nor French, submit a copy translated into English or French by a certified translator. Notarial certificates are not accepted.
Transfer applicants from colleges/universities
Upload a copy of your transcripts from any post-secondary institutions, indicating any courses in progress.
If you have not completed a full year of university or college studies at the time of application, you should also upload transcripts from previous educational institutions.
Where to mail official transcripts (if we request them)
Send all official transcripts to one of the following locations:
By mail:
Concordia University
Undergraduate Admissions
Application Centre
P.O. Box 2900
Montreal, Quebec, Canada
H3G 2S2    
By courier:
Birks Student Service Centre
Room LB-185, J.W. McConnell Building
1400 De Maisonneuve Blvd. W.
Montreal, Quebec  H3G 2V8
Contact phone number for courier:
514-848-2424
Hours of operation
Monday to Wednesday: 9 a.m. – 5 p.m.
Thursday: 9 a.m. – 6 p.m.
Friday: 10 a.m. – 5 p.m.
The University reserves the right to request official documents at any time during the admissions process, and rescind any Offer of Admission made if discrepancies between unofficial and official documents are found.
Sealed Envelope Method
If the institution you attended is located in North America, you may use the sealed envelope method to submit an official transcript. Request that the institution place an official transcript in a sealed envelope.
The envelope must bear:
the name and address of the school
the institutional logo
a stamp or other notice indicating that it contains official transcripts
If you submit the envelope unopened, the transcript will be considered as official.

Proof of status in Canada
Every Canadian citizen or a permanent resident of Canada applying to Concordia — except for Cegep applicants — must provide their proof of status in Canada. If you do not provide this proof of status, you will be charged international tuition fees.
To prove Canadian citizenship or permanent resident status, submit a clear photocopy of one of the following documents:
Quebec birth certificate issued by the Quebec Directeur de l'état civil
(see Concordia’s description for Quebec Residency Guidelines) 
Canadian birth certificate (if born outside Quebec)
Canadian citizenship card (both sides)
Permanent resident card (both sides) or IMM 5292
We do not accept the following documents as proof of status in Canada:
Driver’s licence 
Medicare card 
Quebec baptismal certificate
Social Insurance Number card

For mature students only:
A curriculum vitae
A birth certificate or other acceptable proof of age
School records and any documents which may indicate your ability to pursue university studies
Transcripts"""
            yield item
        except Exception as e:
            with open("./error/" + item['university'] + item['degree_level'] + ".txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

