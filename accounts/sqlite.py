import sqlite3 as db
import json

conn = db.connect("data.db")
c = conn.cursor()
universite_list = []
rows = c.execute("select * from datas where year = '2021' group by universite order by universite").fetchall()
for r in rows:
    print(r)
    universite_list.append(r)
with open('data_2021.json', 'w', encoding='utf-8') as f:
    json.dump(universite_list, f, ensure_ascii=False, indent=4)

# c.execute('''CREATE TABLE datas (bolum text, fakulte text, universite text, burs text, sehir text, dil text, score_last text, range_last text,
#             score_first text, range_first text, faculty_member_count text, year text, enrollment text, capacity text, demand text, ratio_same_city text,
#             number_same_city text, average_range text, min_range text, average_score text, min_score text, range_average_demand text, range_first_demand text,
#             number_first_preference_enrollment text, number_three_preference_enrollment text, number_ten_preference_enrollment text,
#             enroll_average_range text, number_preference_same_city text, number_preference_same_department text, total_preference text)''')


# file = open('data0-480.csv', encoding="utf-8-sig")
# contents = csv.reader(file)
# print(next(contents))

# insert_records = "INSERT INTO datas (bolum, fakulte, universite, burs, sehir, dil, score_last, range_last, score_first, range_first, faculty_member_count, year, enrollment, capacity, demand, ratio_same_city, number_same_city, average_range, min_range, average_score, min_score, range_average_demand, range_first_demand, number_first_preference_enrollment, number_three_preference_enrollment, number_ten_preference_enrollment, enroll_average_range, number_preference_same_city, number_preference_same_department, total_preference) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
# c.executemany(insert_records, contents)







# ################################# Create Columm ####################################
# c.execute("alter table datas add column faculty_student_ratio_in_university 'text'")
# rows = c.execute("select * from datas LIMIT 10")
# for r in rows:
#     print(r)
#     print(r[38])
#     print(len(r))


# 30
# #################################################  average_enrollment_rate_same_faculty_university  ###################
# select_all = "SELECT universite, fakulte, count(bolum), sum(enrollment), sum(capacity), sum(enrollment)/sum(capacity), year FROM datas GROUP BY universite, fakulte, year"
# # select_all = "SELECT universite, fakulte, count(bolum), sum(enrollment), sum(capacity), sum(enrollment)/sum(capacity), year FROM datas WHERE universite = 'ABDULLAH GÜL ÜNİVERSİTESİ' AND fakulte='Mühendislik Fakültesi' GROUP BY universite, fakulte, year"
# # select_all = "SELECT universite, fakulte, bolum, enrollment, capacity, average_enrollment_rate_same_faculty_university, year FROM datas WHERE universite = 'ABDULLAH GÜL ÜNİVERSİTESİ' AND fakulte='Mühendislik Fakültesi'"
# # select_all = "SELECT count(*) FROM datas GROUP BY universite, fakulte LIMIT 10 OFFSET 600"
# rows = c.execute(select_all).fetchall()
# # print(len(rows)) #2533/6522
# i = 0
# for r in rows:
#     # print(r)
#     print(i)
#     i += 1
#     # print("rate = {}".format(str(round(r[5], 2))))
#     # print("rate = {}".format(round(r[5],2)))
#     rate = r[3]/r[4]
#     rate = round(rate,2)
#     print("rate=",rate)
#     # select_average_enrollment_rate_of_the_other_departments_in_the_same_faculty_of_this_university = "SELECT bolum, fakulte, universite, year, average_enrollment_rate_same_faculty_university FROM datas WHERE universite =? AND fakulte =? year =? "
#     results = c.execute("SELECT bolum, fakulte, universite, year, average_enrollment_rate_same_faculty_university FROM datas WHERE universite =? AND fakulte =? AND year =?",(r[0], r[1],r[6])).fetchall()
#     # results = c.execute(select_average_enrollment_rate_of_the_other_departments_in_the_same_faculty_of_this_university,(r[0], r[1], r[6])).fetchall()
#     for result in results:
#         # update = "UPDATE datas SET average_enrollment_rate_same_faculty_university = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? "
#         c.execute("UPDATE datas SET average_enrollment_rate_same_faculty_university = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? ",(rate,result[0],result[2], result[1], result[3]))
#         conn.commit()
#     results_updated = c.execute("SELECT bolum, fakulte, universite, year, average_enrollment_rate_same_faculty_university FROM datas WHERE universite =? AND fakulte =? AND year =?",(r[0], r[1], r[6])).fetchall()
#     for result in results_updated:
#         print("result: " + str(result))


# #31
# #################################################  average_enrollment_rate_same_university  ###################
# # select_all = "SELECT universite, fakulte, count(bolum), sum(enrollment), sum(capacity), sum(enrollment)/sum(capacity), year FROM datas GROUP BY universite, fakulte, year"
# select_all = "SELECT universite, count(bolum), sum(enrollment), sum(capacity), sum(enrollment)/sum(capacity), year FROM datas GROUP BY universite, year"

# rows = c.execute(select_all).fetchall()
# i = 0
# for r in rows:
#     # print(r)
#     print(i)
#     i += 1
#     # print("rate = {}".format(str(round(r[5], 2))))
#     # print("rate = {}".format(round(r[5],2)))
#     rate = r[2]/r[3]
#     rate = round(rate,2)
#     print("rate=",rate)
#     # select_average_enrollment_rate_of_the_other_departments_in_the_same_faculty_of_this_university = "SELECT bolum, fakulte, universite, year, average_enrollment_rate_same_faculty_university FROM datas WHERE universite =? AND fakulte =? year =? "
#     results = c.execute("SELECT bolum, fakulte, universite, year, average_enrollment_rate_same_university FROM datas WHERE universite =? AND year =?",(r[0],r[5])).fetchall()
#     # results = c.execute(select_average_enrollment_rate_of_the_other_departments_in_the_same_faculty_of_this_university,(r[0], r[1], r[6])).fetchall()
#     for result in results:
#         # update = "UPDATE datas SET average_enrollment_rate_same_faculty_university = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? "
#         c.execute("UPDATE datas SET average_enrollment_rate_same_university = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? ",(rate,result[0],result[2], result[1], result[3]))
#         conn.commit()
#     results_updated = c.execute("SELECT bolum, fakulte, universite, year, average_enrollment_rate_same_university FROM datas WHERE universite =? AND year =?",(r[0], r[5])).fetchall()
#     for result in results_updated:
#         print("result: " + str(result))


# #32
# #################################################  average_enrollment_rate_same_department_private_universities  ###################
# # select_all = "SELECT universite, fakulte, count(bolum), sum(enrollment), sum(capacity), sum(enrollment)/sum(capacity), year FROM datas GROUP BY universite, fakulte, year"
# select_all = "SELECT bolum, sum(enrollment), sum(capacity), year FROM datas WHERE burs != 'Ücretsiz' GROUP BY bolum, year"

# rows = c.execute(select_all).fetchall()
# i = 0
# for r in rows:
#     # print(r)
#     print(i)
#     i += 1
#     # print("rate = {}".format(str(round(r[5], 2))))
#     # print("rate = {}".format(round(r[5],2)))
#     rate = r[1]/r[2]
#     rate = round(rate,2)
#     print("rate=",rate)
#     # select_average_enrollment_rate_of_the_other_departments_in_the_same_faculty_of_this_university = "SELECT bolum, fakulte, universite, year, average_enrollment_rate_same_faculty_university FROM datas WHERE universite =? AND fakulte =? year =? "
#     results = c.execute("SELECT bolum, fakulte, universite, year FROM datas WHERE burs != 'Ücretsiz' AND bolum=? AND year =?",(r[0],r[3])).fetchall()
#     # results = c.execute(select_average_enrollment_rate_of_the_other_departments_in_the_same_faculty_of_this_university,(r[0], r[1], r[6])).fetchall()
#     for result in results:
#         # update = "UPDATE datas SET average_enrollment_rate_same_faculty_university = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? "
#         c.execute("UPDATE datas SET average_enrollment_rate_same_department_private_universities = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? ",(rate,result[0],result[2], result[1], result[3]))
#         conn.commit()
#     results_updated = c.execute("SELECT bolum, burs, fakulte, universite,average_enrollment_rate_same_department_private_universities, year FROM datas WHERE burs != 'Ücretsiz' AND bolum=? AND year =?",(r[0],r[3])).fetchall()
#     for result in results_updated:
#         print("result: " + str(result))




# #33
# #################################################  average_enrollment_rate_same_department_state_universities  ###################
# # select_all = "SELECT universite, fakulte, count(bolum), sum(enrollment), sum(capacity), sum(enrollment)/sum(capacity), year FROM datas GROUP BY universite, fakulte, year"
# select_all = "SELECT bolum, sum(enrollment), sum(capacity), year FROM datas WHERE burs = 'Ücretsiz' GROUP BY bolum, year"

# rows = c.execute(select_all).fetchall()
# i = 0
# for r in rows:
#     # print(r)
#     print(i)
#     i += 1
#     # print("rate = {}".format(str(round(r[5], 2))))
#     # print("rate = {}".format(round(r[5],2)))
#     rate = r[1]/r[2]
#     rate = round(rate,2)
#     print("rate=",rate)
#     # select_average_enrollment_rate_of_the_other_departments_in_the_same_faculty_of_this_university = "SELECT bolum, fakulte, universite, year, average_enrollment_rate_same_faculty_university FROM datas WHERE universite =? AND fakulte =? year =? "
#     results = c.execute("SELECT bolum, fakulte, universite, year FROM datas WHERE burs = 'Ücretsiz' AND bolum=? AND year =?",(r[0],r[3])).fetchall()
#     # results = c.execute(select_average_enrollment_rate_of_the_other_departments_in_the_same_faculty_of_this_university,(r[0], r[1], r[6])).fetchall()
#     for result in results:
#         # update = "UPDATE datas SET average_enrollment_rate_same_faculty_university = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? "
#         c.execute("UPDATE datas SET average_enrollment_rate_same_department_state_universities = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? ",(rate,result[0],result[2], result[1], result[3]))
#         conn.commit()
#     results_updated = c.execute("SELECT bolum, burs, fakulte, universite,average_enrollment_rate_same_department_state_universities, year FROM datas WHERE burs = 'Ücretsiz' AND bolum=? AND year =?",(r[0],r[3])).fetchall()
#     for result in results_updated:
#         print("result: " + str(result))




# #34
# #################################################  demand_capacity_same_department_private_universities  ###################
# select_all = "SELECT bolum, sum(demand), sum(capacity), year FROM datas WHERE burs != 'Ücretsiz' GROUP BY bolum, year"

# rows = c.execute(select_all).fetchall()
# i = 0
# for r in rows:
#     print(r)
#     print(i)
#     i += 1
#     rate = r[1]/r[2]
#     rate = round(rate,2)
#     print("rate=",rate)
#     results = c.execute("SELECT bolum, fakulte, universite, year FROM datas WHERE burs != 'Ücretsiz' AND bolum=? AND year =?",(r[0],r[3])).fetchall()
#     for result in results:
#         c.execute("UPDATE datas SET demand_capacity_same_department_private_universities = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? ",(rate,result[0],result[2], result[1], result[3]))
#         conn.commit()
#     results_updated = c.execute("SELECT bolum, burs, fakulte, universite,demand_capacity_same_department_private_universities, year FROM datas WHERE burs != 'Ücretsiz' AND bolum=? AND year =?",(r[0],r[3])).fetchall()
#     for result in results_updated:
#         print("result: " + str(result))




# #35
# #################################################  demand_capacity_same_department_state_universities  ###################
# select_all = "SELECT bolum, sum(demand), sum(capacity), year FROM datas WHERE burs = 'Ücretsiz' GROUP BY bolum, year"

# rows = c.execute(select_all).fetchall()
# i = 0
# for r in rows:
# #     print(r)
#     print(i)
#     i += 1
#     rate = r[1]/r[2]
#     rate = round(rate,2)
#     print("rate=",rate)
#     results = c.execute("SELECT bolum, fakulte, universite, year FROM datas WHERE burs = 'Ücretsiz' AND bolum=? AND year =?",(r[0],r[3])).fetchall()
#     for result in results:
#         c.execute("UPDATE datas SET demand_capacity_same_department_state_universities = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? ",(rate,result[0],result[2], result[1], result[3]))
#         conn.commit()
#     results_updated = c.execute("SELECT bolum, burs, fakulte, universite,demand_capacity_same_department_state_universities, year FROM datas WHERE burs = 'Ücretsiz' AND bolum=? AND year =?",(r[0],r[3])).fetchall()
#     for result in results_updated:
#         print("result: " + str(result))



# #36
# #################################################  demand_capacity_same_faculty_university  ###################
# select_all = "SELECT universite, fakulte, sum(demand), sum(capacity), year FROM datas GROUP BY universite, fakulte, year"

# rows = c.execute(select_all).fetchall()
# i = 0
# for r in rows:
#     # print(r)
#     print("index: ",i)
#     i += 1
#     rate = r[2]/r[3]
#     rate = round(rate,2)
#     print("rate=",rate)
#     results = c.execute("SELECT bolum, fakulte, universite, year FROM datas WHERE universite =? AND fakulte =? AND year =?",(r[0], r[1],r[4])).fetchall()
#     for result in results:
#         c.execute("UPDATE datas SET demand_capacity_same_faculty_university = ? WHERE bolum =? AND universite=? AND fakulte=? AND year=? ",(rate,result[0],result[2], result[1], result[3]))
#         conn.commit()
#     results_updated = c.execute("SELECT bolum, fakulte, universite, demand_capacity_same_faculty_university, year FROM datas WHERE universite =? AND fakulte =? AND year =?",(r[0], r[1],r[4])).fetchall()
#     for result in results_updated:
#         print("result: " + str(result))



#37
#################################################  average_demand_change_percentage_years_same_department  ###################
# 2021
# select_all = "SELECT bolum, sum(demand), year FROM datas WHERE year='2021' GROUP BY bolum"

# rows = c.execute(select_all).fetchall()
# i = 0

# for r in rows:
#     # print(r)
#     # print("index: ",i)
#     # i += 1
#     demand_2021 = r[1]
#     # print("rate=",demand_2021)
#     results = c.execute("SELECT bolum, sum(demand), year FROM datas WHERE year='2020' AND bolum=?",(r[0],)).fetchall()
#     # if results: print("gecen yil:")
#     for result in results:
#         # print(result[1])
#         demand_2020 = result[1]
#         # print("demand_2020: ",demand_2020)
#         if demand_2021 and demand_2020:
#             change = (demand_2021 - demand_2020)/100
#         else:
#             change = None
#         # print("change: ",change)
#         c.execute("UPDATE datas SET average_demand_change_percentage_years_same_department = ? WHERE bolum =? AND year='2021' ",(change,r[0]))
#         conn.commit()
#     results_updated = c.execute("SELECT bolum, sum(demand), average_demand_change_percentage_years_same_department, year FROM datas WHERE year='2021' AND bolum=?",(r[0],)).fetchall()
#     for result in results_updated:
#         print("result: " + str(result))
# 2020
# select_all = "SELECT bolum, sum(demand), year FROM datas WHERE year='2020' GROUP BY bolum"

# rows = c.execute(select_all).fetchall()
# i = 0

# for r in rows:
#     # print(r)
#     # print("index: ",i)
#     # i += 1
#     demand_2020 = r[1]
#     # print("rate=",demand_2020)
#     results = c.execute("SELECT bolum, sum(demand), year FROM datas WHERE year='2019' AND bolum=?",(r[0],)).fetchall()
#     # if results: print("gecen yil:")
#     for result in results:
#         # print(result[1])
#         demand_2019 = result[1]
#         # print("demand_2019: ",demand_2019)
#         if demand_2020 and demand_2019:
#             change = (demand_2020 - demand_2019)/100
#         else:
#             change = None
#         # print("change: ",change)
#         c.execute("UPDATE datas SET average_demand_change_percentage_years_same_department = ? WHERE bolum =? AND year='2020' ",(change,r[0]))
#         conn.commit()
    # results_updated = c.execute("SELECT bolum, sum(demand), average_demand_change_percentage_years_same_department, year FROM datas WHERE year='2020' AND bolum=?",(r[0],)).fetchall()
    # for result in results_updated:
    #     print("result: " + str(result))






# #38
# #################################################  faculty_student_ratio_in_university  ###################
# select_all = "SELECT universite, count(fakulte), sum(enrollment), year FROM datas GROUP BY universite, year"

# rows = c.execute(select_all).fetchall()
# i = 0
# for r in rows:
#     # print(r)
#     print("index: ",i)
#     i += 1
#     rate = r[2]/r[1]
#     rate = round(rate,2)
#     # print("rate=",rate)
#     results = c.execute("SELECT bolum, fakulte, universite, year FROM datas WHERE universite=? AND year=?",(r[0], r[3])).fetchall()
#     for result in results:
#         c.execute("UPDATE datas SET faculty_student_ratio_in_university = ? WHERE bolum=? AND fakulte=? AND universite=? AND year=? ",(rate,result[0],result[1], result[2], result[3]))
#         conn.commit()
#     results_updated = c.execute("SELECT bolum, fakulte, universite, faculty_student_ratio_in_university, year FROM datas WHERE universite =? AND year =?",(r[0], r[3])).fetchall()
#     for result in results_updated:
#         print("result: " + str(result))




conn.commit()
conn.close()
