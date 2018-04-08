# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapymodule_Canada.insert_mysql import InsertMysql

# 2018/04/08
class ScrapymoduleCanadaPipeline(InsertMysql):
    def process_item(self, item, spider):
        sql = "insert into tmp_school_major_copy(university, country, city, website, department, programme, degree_level, " \
              "degree_type, ucas_code, mode, application_date, deadline, start_date, degree_description, " \
              "overview, duration, modules, application_fee, tuition_fee, create_person, teaching_assessment, career, location, " \
              "entry_requirements, chinese_requirements, ATAS, GPA, average_score, accredited_university, Alevel, " \
              "IB, IELTS, IELTS_L, IELTS_S, IELTS_R, IELTS_W, TOEFL, TOEFL_L, TOEFL_S, TOEFL_R, TOEFL_W, GRE, GMAT," \
              " LSAT, MCAT, working_experience, interview, portfolio, application_documents, how_to_apply, school_test, " \
              "SATI, SATII, SAT_code, ACT, ACT_code, other, url,ap, writer, sid, did, TOEFL_code, Application_link, campus) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            self.cursor.execute(sql, (item["university"], item["country"], item["city"], item["website"],
                                      item["department"], item["programme"], item["degree_level"], item["degree_type"],
                                      item["ucas_code"], item["mode"], item["application_date"], item["deadline"],
                                      item["start_date"], item["degree_description"], item["overview"], item["duration"],
                                      item["modules"], item["application_fee"], item["tuition_fee"], item["create_person"],
                                      item["teaching_assessment"], item["career"], item["location"], item["entry_requirements"],
                                      item["chinese_requirements"], item["ATAS"], item["GPA"], item["average_score"],
                                      item["accredited_university"], item["Alevel"], item["IB"], item["IELTS"],
                                      item["IELTS_L"], item["IELTS_S"], item["IELTS_R"], item["IELTS_W"], item["TOEFL"],
                                      item["TOEFL_L"], item["TOEFL_S"], item["TOEFL_R"], item["TOEFL_W"], item["GRE"],
                                      item["GMAT"], item["LSAT"], item["MCAT"], item["working_experience"],
                                      item["interview"], item["portfolio"], item["application_documents"],
                                      item["how_to_apply"], item["school_test"], item["SATI"], item["SATII"],
                                      item["SAT_code"], item["ACT"], item["ACT_code"], item["other"], item["url"],
                                      item["ap"], item["writer"], item["sid"], item["did"], item["TOEFL_code"],
                                      item["Application_link"], item["campus"]))
            self.db.commit()
            print("数据插入成功")
        except Exception as e:
            self.db.rollback()
            print("数据插入失败：%s" % (str(e)))
            with open("./mysqlerror/"+item['university']+item['degree_level']+".txt", 'a', encoding="utf-8") as f:
                f.write(str(e) + "\n========================\n")
        # self.close()
        return item
