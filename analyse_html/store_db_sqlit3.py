#!/usr/bin/python
 #coding:utf-8

from    analyse_html import violations_info,  rule_reports, violations_info
import sqlite3
from    sqlite3 import Error

class process_bd(object):
    def __init__(self, db_path=r'C:\Users\Administrator\source\repos\FlaskWebProject3\FlaskWebProject3\instance\flaskr.sqlite'):
        self.db_url = db_path
        self.db_conn = self.create_connection(db_path)
        self.db_conn.row_factory = sqlite3.Row              #enable row object, r['qty'] not a tuple, but a Row Object
        if self.db_conn == None:
            pass    #error process

    
    def commit(self)  :
        self.db_conn.commit()

##存储分析结果表格信息的类，包含以下四类信息
#class rule_table_row(object):
#    #violation_num = 0 Number of Violations
#    #LDRA_code = '' #LDRA Code
#    #mandatory_std = '' #Mandatory Standards
#    #standard_code = '' #GJB_8114 Code
#     #detail_list #rule obey details
#    def __init__(self, v_num, l_code, man_std, std_code, detail_dict):
#        self.violation_num = v_num
#        self.LDRA_code = l_code
#        self.mandatory_std = man_std
#        self.standard_code = std_code
#        self.detail_dict = detail_dict
    def store_to_db(self, rule_report):
        """将一个软件的testbed规则分析结果存入DB
        :param rule_report: a object of class rule_reports
        """
        userid , proid = self.get_userid_projectid()
        for row in rule_report.rule_results():
            pass                                                    
            
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
 
        return None

    def insert_LDRA_rule(self, ldra_rule)  :
        cur = self.db_conn.cursor()
        sql = '''insert into LDRA_rule(GJB8114Code, LDRACode,  MandatoryStanard_en,  MandatoryStandard_ch,  Rule_classification)
                values (?,?,?,?,?) '''
        cur.execute(sql, ldra_rule)
        
    def insert_rule_obey_info(self, rule_obey_info):
        cur = self.db_conn.cursor()
        sql = '''inset into rule_obey_info(projectid, ldracode,location_function, line_numbers) 
        values(?,?,?,?)'''

    def insert_project(self, project):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO projects(name,begin_date,end_date)
                  VALUES(?,?,?) '''
        cur = self.db_conn.cursor()
        cur.execute(sql, project)
        return cur.lastrowid

    def insert_user(self, user):
        """
        Create a new user into the projects table
        :param conn:
        :param user:
        :return: user id
        """
        sql = ''' INSERT INTO user(name)
                  VALUES(?) '''
        cur = self.db_conn.cursor()
        cur.execute(sql, user)
        return cur.lastrowid


    def get_userid_projectid(self):
        '''
        仅调试用
        从数据库中获取userid和projectid，用来作为具体信息的外键，
        在实际使用时，会根据用户在网站的登陆信息来获取
        '''
        cur = self.db_conn.cursor()

        sql = r'''select * from user where name = 'wangyang' ''' 
        cur.execute(sql)
        userid = cur.fetchone()['id']
        
        sql = r'''select id from projects where projectname = 'testproject' ''' 
        cur.execute(sql)
        projectid = cur.fetchone()['id']

        return (userid, projectid)



    def init_db_for_debug(self):
        """
        仅调试用
        在没有建立用户和工程的情况下，先调试分析结果入库的功能
        在数据库中插入一个用户和一个工程，每次使用前先调用这个函数
        """
        cur = self.db_conn.cursor()
        sql = '''select * from user'''
        cur.execute(sql)
        rows = cur.fetchall()
        
        if len(rows) == 0:
            sql = '''INSERT INTO user(name)
                      VALUES(?) ''' 
            cur.execute(sql, ('wangyang',))
            userid = cur.lastrowid

            sql = '''INSERT INTO projects(projectname, userid)
                      VALUES(?,?) ''' 
            cur.execute(sql,("testproject",userid))            
            self.db_conn.commit()               
        return


if __name__ == '__main__':
    #analyse html
    html = u"file:///C:/LDRA_Workarea/example_tbwrkfls/example.rps.htm"
    report = rule_reports()
    report.analyse_html(html)

    #store to DB
    db_obj = process_bd()
    db_obj.init_db_for_debug()
    #userid , proid = db_obj.get_userid_projectid()
    db_obj.store_to_db(report)


