#!/usr/bin/python
 #coding:utf-8
import re
from    urllib import urlopen
from    bs4 import BeautifulSoup



#从html文件中得到一条规则的具体违背情况
#对应一个popup页面，也就是一条规则的详细违背情况，包括 {function name : [line number1, line number2,
#line number3....] }
class violations_info(object):
    def __init__(self, file_url):
        self.violations_num = 0
        self.ref_link = file_url
        self.violatons_detail = {}      #{function name : [line number1, line number2, line number3....] }
        
        #open ref_link file and get details
        html = urlopen(self.ref_link)
        self.bsObj = BeautifulSoup(html.read(), features="html.parser") 

    #每条规则的html模式如下：
    #<td bgcolor='#FF8181', align=center><font color='blue'> <center> <a
    #href='example_link_popup11S.htm' onClick='return popup(this, "knotes")'>
    #16</a> </center> </font></td>
    def get_violations_detail(self):
        if len(self.violatons_detail) == 0:
            a_list = self.bsObj.find_all('a')
            function_name = ''
            line_num = []

            state = 'init_state'
            for a_element in  a_list:
                element_string = a_element.get_text().strip()
                if element_string.isdigit(): #line number
                    if state == 'get_function_name':
                        state = 'get_number'
                    else:                        
                        pass    #should not happen
                    line_num.append(int(element_string))
                                        
                else: #function name
                    if state == 'init_state' : 
                        state = 'get_function_name'
                    elif state == 'get_number':
                        state = 'get_function_name'
                        if function_name in self.violatons_detail:
                            self.violatons_detail[function_name].extend(line_num)
                        else:
                            self.violatons_detail[function_name] = list(line_num)
                        line_num[:] = []
                    else:
                        pass #should not happen
                    function_name = element_string
            
            #处理剩余的行号，并加入到最后一个函数的字典
            if function_name in self.violatons_detail:
                self.violatons_detail[function_name].extend(line_num)
            else:
                self.violatons_detail[function_name] = list(line_num)
        return self.violatons_detail

#存储分析结果表格信息的类，包含以下四类信息
class rule_table_row(object):
    #violation_num = 0 Number of Violations
    #LDRA_code = '' #LDRA Code
    #mandatory_std = '' #Mandatory Standards
    #standard_code = '' #GJB_8114 Code
     #detail_list #rule obey details
    def __init__(self, v_num, l_code, man_std, std_code, detail_dict):
        self.violation_num = v_num
        self.LDRA_code = l_code
        self.mandatory_std = man_std
        self.standard_code = std_code
        self.detail_dict = detail_dict


#存储了一个被测软件的规则分析结果
class rule_reports(object):
    script_pattern_string = u'\'.*?\''
    script_regex = re.compile(script_pattern_string)
    
    def __init__(self):
        self.fileurl = ''
        self.baseurl = ''
        self.result_list = []        #list of rule_table_row.  Overall Code Review Summary
        self.bsObj = None
        self.html = None

    def rule_results(self):
        """
        生成器算法，将rule_reports对象变成一个可以迭代的对象
        """
        for row in self.result_list:
            yield row

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
    def store_rule_repot_to_db(self, db_obj):
        """将一个软件的testbed规则分析结果存入DB
        :param rule_report: a object of class rule_reports
        """
        userid , proid = db_obj.get_userid_projectid()
        for row in self.rule_results():
            LDRA_code = row.LDRA_code
            for functionname, err_list in row.detail_dict.iteritems():
                line_str = ','.join(str(e) for e in err_list)
                rule_obey_item = (proid, LDRA_code, functionname, line_str)
                db_obj.insert_rule_obey_info(rule_obey_item)

        db_obj.commit()
        return         
        
    #脚本文件主函数
    #处理一个htlm文件
    #    将文件中规则违背情况抽取出来，放入列表，并返回
    
    #    Args:
    #        file_url: html文件路径
       
    #    Returns:
    #        如果这个文件包含规则违背情况，则返回详细情况的list
    #        如果这个文件包含规则违背情况，则返回空表
    def analyse_html(self,file_url):
            self.fileurl = file_url
            self.html = urlopen(file_url)
            self.bsObj = BeautifulSoup(self.html.read(), features="html.parser") 
            index = file_url.rfind('/')
            self.base_url = file_url[:index + 1] #init base url

            tablelist = self.bsObj.find_all("table")
            #存放多个表的分析结果，因此使用list
            for table_tag in tablelist:
                print table_tag
                if self.is_rule_table(table_tag):
                        self.result_list.extend(self.get_rule_table_contents(table_tag))
            return self.result_list

        #judege if table is 8114 analyse result
    #取出表头判断是否为rule table，表头格式如下：
    #<TR><th > Number of Violations </th><th > LDRA Code </th><th > Mandatory
    #Standards </th><th > GJB_8114 Code
    #</th></TR>
    def is_rule_table(self, table_tag):
            #不存在tbody的tag一定不是需要处理的table类型
            if table_tag.tr == None:
                    return
            #获得trlistth_list[0].string == 'Number of Violations'
            tr_list = table_tag.find('tr')
            #从trlist中获得tdlist，并且tdlist的长度 == 4才可能是需要的信息
            if tr_list != None:
                    th_list = tr_list.find_all('th')
            if len(th_list) != 4:
                    return False
            elif th_list[0].string.strip() == u'Number of Violations' and \
                    th_list[1].string.strip() == u'LDRA Code' and \
                    th_list[2].string.strip() == u'Mandatory Standards' and \
                    th_list[3].string.strip() == u"GJB_8114 Code": 
                            return True
    
    #获取一个rule table的所有错误信息行，并保存在一个list中返回
    #调用该函数的前提是 table_tag一定是我们需要的table信息，也就是8114规则表格
    def get_rule_table_contents(self, table_tag):
            if table_tag.tr == None:
                    return
            #获取所有的table rows
            tr_list = table_tag.find_all('tr')
            row_list = []
            first_tr = tr_list[0]
            for e in tr_list[1:] : #遍历所有<tr> e -> tr tag
                    v = self.process_one_row(e)
                    if v:
                            row_list.append(v)
            return row_list

    #处理一个table_row
    #    从table row中获取每一条规则的违背情况。如果这个规则的违背情况为0，返回None
    #    如果违背情况大于0，那么返回一个rule_table_row对象
    
    #    Args:
    #        table_row: 包含一条规则违背情况的tag，应该是以<tr/>包含.
       
    #    Returns:
    #        如果这个规则的违背情况为0，返回None
    #        如果违背情况大于0，那么返回一个rule_table_row对象
    def process_one_row(self, table_row):
            td_list = table_row.find_all('td')
            v_num_str = td_list[0].get_text().strip()
            #存在一种可能，v_num == '-'可能代表该规则没有被分析
            if v_num_str.isdigit():
                    v_num = int(v_num_str)
            else:
                    return None
        
            if v_num != 0:
                    a_tag = td_list[0].find('a')       
                    file_name = a_tag['href']
                    ref_link = self.base_url + file_name
                    
                    v_info = violations_info(ref_link)
                    v_detail_dict = v_info.get_violations_detail()
                    l_code = td_list[1].string
                    m_string = self.strip_mandatory_standard(td_list[2].script.string)
                    r_string = self.strip_standard_rule_number(td_list[3].script.string)
                    v = rule_table_row(v_num,l_code,m_string,r_string,v_detail_dict)
                    return v
            else:
                    return None

          
    #从java script源代码中抽取出mandator standard string的内容
    def strip_mandatory_standard(self, script_string):
            match_list = self.script_regex.findall(script_string)
            mandatory_standard_string = match_list[1]
            return mandatory_standard_string 

    #从java script源代码中抽取出特定标准的序号
    def strip_standard_rule_number(self, script_string):
            match_list = self.script_regex.findall(script_string)
            standard_rule_number_string = match_list[1]
            return standard_rule_number_string 


from store_db_sqlit3 import process_db

if __name__ == "__main__":
    html = u"file:///C:/LDRA_Workarea/example_tbwrkfls/example.rps.htm"
    report = rule_reports()
    report.analyse_html(html)

    db_obj = process_db()
    report.store_rule_repot_to_db(db_obj)
