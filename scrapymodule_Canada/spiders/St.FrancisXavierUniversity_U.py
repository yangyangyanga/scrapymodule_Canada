# -*- coding: utf-8 -*-
import scrapy
import re
from scrapymodule_Canada.clearSpace import clear_space, clear_space_str
from scrapymodule_Canada.getItem import get_item
from scrapymodule_Canada.getTuition_fee import getTuition_fee
from scrapymodule_Canada.items import ScrapymoduleCanadaItem


class SFXUbenSchoolSpider(scrapy.Spider):
    # name = "sfxuBen"
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
        print(len(programmeKey))
        print(len(departmentValue))
        for i in range(len(programmeKey)):
            resultDict[programmeKey[i]] = departmentValue[i]
        print(resultDict)

        links = response.xpath("//div[@class='slick-list draggable']/div[@class='slick-track']/a/@href").extract()
        print(len(links))
        links = list(set(links))
        print(len(links))
        for link in links:
            url = "https://www.stfx.ca" + link
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        item = get_item(ScrapymoduleCanadaItem)
        item['university'] = "St. Francis Xavier University "
        item['country'] = 'Canada'
        item['website'] = 'https://www.stfx.ca/'
        item['url'] = response.url
        item['degree_level'] = "0"
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

            item['IELTS'] = "6.5"
            item['TOEFL'] = "88"
            yield item
        except Exception as e:
            with open("./error/" + item['university'] + item['degree_level'] + ".txt", 'w', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

