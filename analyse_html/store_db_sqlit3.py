#!/usr/bin/python
 #coding:utf-8

from    analyse_html_rule import violations_info,  rule_reports, violations_info
import sqlite3
from    sqlite3 import Error




class process_db(object):
    def __init__(self, db_path=r'C:\Users\Administrator\source\repos\FlaskWebProject3\FlaskWebProject3\instance\flaskr.sqlite'):
        self.db_url = db_path
        self.db_conn = self.create_connection(db_path)
        self.db_conn.row_factory = sqlite3.Row              #enable row object, r['qty'] not a tuple, but a Row Object
        if self.db_conn == None:
            pass    #error process

    def init_db(self):
        with open('create_tables.sql',mode = 'r') as f:
            self.db_conn.cursor().executescript(f.read())
        self.db_conn.commit()
    
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
    def store_rule_repot_to_db(self, rule_report):
        """将一个软件的testbed规则分析结果存入DB
        :param rule_report: a object of class rule_reports
        """
        userid , proid = self.get_userid_projectid()
        for row in rule_report.rule_results():
            LDRA_code = row.LDRA_code
            for functionname, err_list in row.detail_dict.iteritems():
                line_str = ','.join(str(e) for e in err_list)
                rule_obey_item = (proid, LDRA_code, functionname, line_str)
                self.insert_rule_obey_info(rule_obey_item)

        self.commit()
        return 

    def store_metrix_report_to_db(self, metrix_repot):
        return

    def insert_rule_obey_info(self, obey_info):
        cur = self.db_conn.cursor()
        sql = '''insert into rule_obey_info(projectid,  LDRA_Code, location_function, line_numbers)
                values (?,?,?,?) '''
        cur.execute(sql, obey_info)
        return 
            
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

    def get_ldra_id(self,ldra_code):
        cur = self.db_conn.cursor()
        sql = '''select * from LDRA_rule where LDRACode = ? '''
        cur.execute(sql, (ldra_code,))
        row = cur.fetchone()
        if row != None:
            return row['id']
        else:
            return None



    def insert_LDRA_rule(self, ldra_rule)  :
        cur = self.db_conn.cursor()
        sql = '''insert into LDRA_rule(LDRACode,  MandatoryStanard_en)
                values (?,?) '''
        cur.execute(sql, ldra_rule)
        return cur.lastrowid

    def insert_GJB8114_rule(self, GJB8114_rule)  :
        cur = self.db_conn.cursor()
        sql = '''insert into GBJ8114_rule(GJB8114Code,  Rule_description, MandatoryStandard_ch, Rule_classification)
                values (?,?,?,?) '''
        cur.execute(sql, GJB8114_rule)
        return cur.lastrowid

    def insert_GJB_LDRA_relation_table(self, GJB8114_LDRA_relation)  :
        cur = self.db_conn.cursor()
        sql = '''insert into GJB_LDRA_relation_table(GJB8114_id,  LDRA_id)
                values (?,?) '''
        cur.execute(sql, GJB8114_LDRA_relation)
   
    def create_GJB_LDRA_realtion_table(self):
        pass
        


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


from analyse_html_matrix import dev_location

if __name__ == '__main__':
    #analyse html
    if dev_location == 'home':
        html = u"file:///C:/Users/Administrator/Documents/code/project_from_github/analyse_html/example_tbwrkfls/example.rps.htm"
    else:
        html = u"file:///C:/LDRA_Workarea/example_tbwrkfls/example.rps.htm"

    report = rule_reports()
    report.analyse_html(html)

    #store to DB
    db_obj = process_db()
    db_obj.init_db_for_debug()
    #userid , proid = db_obj.get_userid_projectid()
    db_obj.store_rule_repot_to_db(report)



