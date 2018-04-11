# -*- coding: utf-8 -*-
import scrapy
import re
from scrapymodule_Canada.clearSpace import clear_space, clear_space_str
from scrapymodule_Canada.getItem import get_item
from scrapymodule_Canada.getTuition_fee import getTuition_fee
from scrapymodule_Canada.items import ScrapymoduleCanadaItem


class MyspiderSchoolSpider(scrapy.Spider):
    name = "myspiderBen"
    start_urls = []
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
        item['TOEFL_code'] = item['SAT_code'] = item['ap'] = ""
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
            item['IELTS_L'] = "6"
            item['IELTS_S'] = "6"
            item['IELTS_R'] = "6"
            item['IELTS_W'] = "6"
            item['TOEFL'] = "88"
            item['TOEFL_L'] = "20"
            item['TOEFL_S'] = "21"
            item['TOEFL_R'] = "20"
            item['TOEFL_W'] = "21"
            yield item
        except Exception as e:
            with open("./error/" + item['university'] + item['degree_level'] + ".txt", 'a', encoding="utf-8") as f:
                f.write(str(e) + "\n" + response.url + "\n========================")
            print("异常：", str(e))
            print("报错url：", response.url)

