# import pymysql
# from main import createConfig
#
#
# con = pymysql.connect(host='localhost',
#                       user='admin',
#                       password='admin',
#                       db='result')
#
# with con:
#     cur = con.cursor()
#     cur.execute("SELECT VERSION()")
#
#     version = cur.fetchone()
#
#     print("Database version: {}".format(version[0]))