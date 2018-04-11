# -*- coding: utf-8 -*-
import scrapy
import re
from scrapymodule_Canada.clearSpace import clear_space, clear_space_str
from scrapymodule_Canada.getItem import get_item
from scrapymodule_Canada.getTuition_fee import getTuition_fee
from scrapymodule_Canada.items import ScrapymoduleCanadaItem


class LUBenSchoolSpider(scrapy.Spider):
    name = "luBen"
    start_urls = [""]
    # print(len(start_urls))
    start_urls = list(set(start_urls))
    # print(len(start_urls))

    def parse(self, response):
        item = get_item(ScrapymoduleCanadaItem)
        item['university'] = ""
        item['country'] = 'Canada'
        item['website'] = ''
        item['url'] = response.url
        item['degree_level'] = ""
        item['TOEFL_code'] = item['SAT_code'] = ""
        print("===========================")
        print(response.url)
        try:
            # 地点
            location = response.xpath(
                "").extract()
            location = ''.join(location)
            item['location'] = location
            # print("item['location']: ", item['location'])

            # 专业
            programme = response.xpath(
                "//text()").extract()
            programme = ''.join(programme)
            item['programme'] = programme
            # print("item['programme']: ", item['programme'])

            # ucas_code
            ucas_code = response.xpath(
                "").extract()
            ucas_code = ''.join(ucas_code)
            item['ucas_code'] = ucas_code
            # print("item['ucas_code']: ", item['ucas_code'])

            # duration
            duration = response.xpath(
                "").extract()
            duration = ''.join(duration)
            item['duration'] = duration
            # print("item['duration']: ", item['duration'])

            allcontent = response.xpath(
                "").extract()
            # modules
            if "Interesting courses and unique opportunities" in allcontent:
                degree_typeIndex = allcontent.index("Interesting courses and unique opportunities")
                if "Professional opportunities" in allcontent[degree_typeIndex:]:
                    degree_typeIndexEnd = allcontent.index("Professional opportunities")
                    degree_type = allcontent[degree_typeIndex + 2:degree_typeIndexEnd]
                    item['modules'] = ''.join(degree_type)
            # print("item['modules']: ", item['modules'])


            # https://laurentian.ca/international
            item["start_date"] = "January, September"
            item["deadline"] = "10/1,  4/1"
            item["chinese_requirements"] = "Senior High School/ Middle School Graduation Certificate with final transcript showing grade 12 first and second term grades. GAOKAO not required."
            item['IELTS'] = "6.5"
            # item['TOEFL'] = ""
            item["SATI"] = "1650"
            item["ACT"] = "24"
            item["application_documents"] = """official high school transcripts with notarized English translation;
official high school diploma with notarized English translation;
proof of English language proficiency unless also applying to English for Academic Preparation (EAP);
resume or CV specifying current education, interests and work experience;
copy of valid passport (both sides)."""
            item["how_to_apply"] = """How to apply
To apply: 
	For international applicants to undergraduate bachelor's programs. apply here
	For international applicants to graduate (Master's, PhDs or Graduate Diploma programs). apply here
 
Provide the following documents to the university directly in order to process your application:
	official high school transcripts with notarized English translation
	official high school diploma with notarized English translation
	proof of English language proficiency unless also applying to English for Academic Preparation (EAP)
	resume or CV specifying current education, interests and work experience
	copy of valid passport (both sides)
 
Documents should be mailed to:
Admissions Office
Laurentian University
935 Ramsey Lake Road
Sudbury, Ontario
Canada P3E 2C6"""
            item["Application_link"] = "https://www3.laurentian.ca/international/"


            yield item
        except Exception as e:
            with open("./error/" + item['university'] + item['degree_level'] + ".txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

