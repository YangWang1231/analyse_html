#!/usr/bin/python
 #coding:utf-8
import re
from    urllib import urlopen
from    bs4 import BeautifulSoup

base_url = ''   #基础路径

#<td bgcolor='#FF8181', align=center><font color='blue'> <center> <a
#href='example_link_popup11S.htm' onClick='return popup(this, "knotes")'>
#16</a> </center> </font></td>
class violations_info(object):
    violations_num = 0  #Number of Violations
    ref_link = ''   #link string of href='example_link_popup11S.htm'
    violatons_detail = []   #list store violation info .etc [(traverse , 28), ( reservedLookup , 68)]
    bsObj = None

    def __init__(self, td_element):
        a_tag = td_element.find('a')       
        file_name = a_tag['href']
        ref_link = base_url + file_name
        #open ref_link file and get details
        html = urlopen(ref_link)
        bsObj = BeautifulSoup(html.read(), features="html.parser") 

    #从html文件中得到一条规则的具体违背情况
    def get_violations_detail():

        return violatons_detail

#存储分析结果表格信息的类，包含以下四类信息
class rule_table_row(object):
    violation_num = 0       #Number of Violations
    LDRA_code = ''          #LDRA Code
    mandatory_std = ''      #Mandatory Standards
    standard_code = ''      #GJB_8114 Code
                 
    def __init__(self, v_num, l_code, man_std, std_code):
        self.violation_num = v_num
        self.LDRA_code = l_code
        self.mandatory_std = man_std
        self.standard_code = std_code

script_pattern_string = u'\'.*?\''
script_regex = re.compile(script_pattern_string)


#存储了一个被测软件的规则分析结果
class rule_reports(object):
    review_summary = []        #list of rule_table_row.  Overall Code Review Summary

#从java script源代码中抽取出mandator standard string的内容
def strip_mandatory_standard(script_string):
        match_list = script_regex.findall(script_string)
        mandatory_standard_string = match_list[1]
        return mandatory_standard_string 

#从java script源代码中抽取出特定标准的序号
def strip_standard_rule_number(script_string):
        match_list = script_regex.findall(script_string)
        standard_rule_number_string = match_list[1]
        return standard_rule_number_string 

#处理一个table_row
#    从table row中获取每一条规则的违背情况。如果这个规则的违背情况为0，返回None
#    如果违背情况大于0，那么返回一个rule_table_row对象
    
#    Args:
#        table_row: 包含一条规则违背情况的tag，应该是以<tr/>包含.
       
#    Returns:
#        如果这个规则的违背情况为0，返回None
#        如果违背情况大于0，那么返回一个rule_table_row对象
def process_one_row(table_row):
        td_list = table_row.find_all('td')
        v_num_str = td_list[0].get_text().strip()
        #存在一种可能，v_num == '-'可能代表该规则没有被分析
        if v_num_str.isdigit():
                v_num = int(v_num_str)
        else:
                return None
        
        if v_num != 0:
                v_info = violations_info(td_list[0])
                v_detail_list = v_info.get_violations_detail()
                l_code = td_list[1].string
                m_string = strip_mandatory_standard(td_list[2].script.string)
                r_string = strip_standard_rule_number(td_list[3].script.string)
                v = rule_table_row(v_num,l_code,m_string,r_string)
                return v
        else:
                return None

#获取一个rule table的所有错误信息行，并保存在一个list中返回
#调用该函数的前提是 table_tag一定是我们需要的table信息，也就是8114规则表格
def get_rule_table_contents(table_tag):
        if table_tag.tr == None:
                return
        #获取所有的table rows
        tr_list = table_tag.find_all('tr')
        row_list = []
        first_tr = tr_list[0]
        for e in tr_list[1:] : #遍历所有<tr> e -> tr tag
                v = process_one_row(e)
                if v:
                        row_list.append(v)
        return row_list

#judege if table is 8114 analyse result
    #取出表头判断是否为rule table，表头格式如下：
    #<TR><th > Number of Violations </th><th > LDRA Code </th><th > Mandatory
    #Standards </th><th > GJB_8114 Code
    #</th></TR>
def is_rule_table(table_tag):
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
        
#脚本文件主函数
#处理一个htlm文件
#    将文件中规则违背情况抽取出来，放入列表，并返回
    
#    Args:
#        file_url: html文件路径
       
#    Returns:
#        如果这个文件包含规则违背情况，则返回详细情况的list
#        如果这个文件包含规则违背情况，则返回空表
def analyse_html(file_url):
        html = urlopen(file_url)
        bsObj = BeautifulSoup(html.read(), features="html.parser") 

        tablelist = bsObj.find_all("table")
        #存放多个表的分析结果，因此使用list
        result_list = []
        for table_tag in tablelist:
            print table_tag
            if is_rule_table(table_tag):
                    result_list.extend(get_rule_table_contents(table_tag))
        return result_list

if __name__ == "__main__":
    html = u"file:///C:/LDRA_Workarea/example_tbwrkfls/example.rps.htm"
    index = html.rfind('/')
    base_url = html[:index + 1] #init base url
    analyse_html(html)
