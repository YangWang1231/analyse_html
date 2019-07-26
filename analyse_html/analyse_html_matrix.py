#!/usr/bin/python
 #coding:utf-8
"""
 analyse_html_matrix.py主要作用是获取testbed分析出的质量度量结果，作为生成word报告的数据素材

 输出：
 模块总数： function total number
 最大模块行数：max module execute line number ,    filename
 最小模块行数：min module execute line number ,    filename
 最大圈复杂度数： max matrix complex number,    filename\function name 

 模块信息表：
 文件名            模块数      
 .....                     .......

 模块圈复杂度、扇出数统计表：
 模块名称                                   圈复杂度（超过10）              扇出数（大于7）
 filename/function name             12                                                  9
                ......                                 ......                                              ......


输入： xxx.mts.htm文件
每个testbed生成的最终结果，包含一个xxx.mts.htm文件，存放了软件的质量度量信息
所有的度量信息都是以.c文件为单位，用JSON描述这些信息.
以code.c为例：
{
    file name : string ,
    1.  reformatted code information for file : (<a id="reformatted code information for file">Reformatted Code Information for File (TM.C)</a>)
    {
        total lines : int
        totalcomments : int
        executeable ref lines : int 
        Non executeable lines: int
        number of procedures : int (模块信息表项)
     },

    2. complexity metrics :  (<a id="complexity metrics">Complexity Metrics (UTIL.C)</a>)
    [
        { function name : string ,   Cyclomatic information :  int },
        { function name : string ,   Cyclomatic information :  int },
        { function name : string ,   Cyclomatic information :  int }
    ],

    3. dataflow information:   (<a id="dataflow information">Dataflow Information (UTIL.C)</a> )
    [
        {       function name : string,      fan out number : int    },
        {       function name : string,      fan out number : int    },
        {       function name : string,      fan out number : int    },
    ]
}

方法：
从每个文件中依次查找
<a id="reformatted code information for file">Reformatted Code Information for File (TM.C)</a>
<a id="complexity metrics">Complexity Metrics (UTIL.C)</a>
<a id="dataflow information">Dataflow Information (UTIL.C)</a>


TODO:
考虑用jison来存储这些信息，并发送给C#生成端程序，这样保证数据库格式与C#分离，在数据库格式修改的情况下，不需要修改C#软件
同理，规则分析的结果也通过jison发给C#生成端
 """


import re
from    urllib import urlopen
from    bs4 import BeautifulSoup

class reformated_code_information(object):
    def __init__(self, totaline=0, totalcomment=0, executeablelines=0, nonexecuteablelines=0, numberOfprocedure=0):
        self.total_line_number = totaline 
        self.total_comments_number = totalcomment
        self.executeable_ref_lines = executeablelines
        self.Non_executeable_lines = nonexecuteablelines 
        self.number_of_procedure = numberOfprocedure
    
    def __str__(self):
        str_output = "{}  {}  {} {} {}".format(self.total_line_number, self.total_comments_number, self.executeable_ref_lines, self.Non_executeable_lines, self.number_of_procedure)
        return str_output



class function_complexity_fanout(object):
    def __init__(self):
        self.function_name = ''
        self.Cyclomatic_information = 0
        self.fanout = 0


class metrix_report(object):
    """
    处理一个软件的metrix report
    """
    def __init__(self):
        slef.filename = ''
        self.reformated_code_information = reformated_code_information()
        self.complexity_metrics = [] #list of function_complexity_fanout
        return 

    def fun(self, name):
        pass
    

class process_metrix_repot(object):
    def __init__(self):
        self.fileurl = ''
        self.html = None
        self.bsObj = None



    def get_reformated_info(self, content_table):
        #<table bgcolor="#ECE2E2" width="100%">
        #<tbody>
        #<tr align="LEFT"><th> File </th><th> Total Ref.  </th><th> Total
        #</th><th> Executable </th><th> Non-Executable </th><th> Number of
        #</th><th> Total </th><th> Expansion </th></tr>
        #<tr align="LEFT"><th> &nbsp; </th><th> <u> Lines </u> </th><th> <u>
        #Comments </u> </th><th> <u> Ref.  Lines </u> </th><th> <u> Ref.  Lines
        #</u> </th><th> <u> Procedures </u> </th><th> <u> Src.  Lines </u>
        #</th><th> <u> Factor </u> </th></tr>
        #<tr align="LEFT"><th colspan="8"> &nbsp; </th></tr>
        #<tr align="LEFT"><td> Total for UTIL.C </td><td><font color="#008000">
        #538 (P) </font></td><td><font color="#008000"> 92 (P) (17%)
        #</font></td><td><font color="#008000"> 245 (P) (46%)
        #</font></td><td><font color="#008000"> 201 (P) (37%)
        #</font></td><td><font color="#008000"> 6 (P) </font></td><td><font
        #color="#008000"> 315 (P) </font></td><td><font color="#008000"> 1.71
        #(P) </font></td></tr>
        #</tbody></table>
            tr_list = content_table.find_all('tr')
            tr_list = tr_list[3:] #前面三行是固定的无用内容
            for tr in tr_list:
                td_list = tr.find_all('td')
                numberlist = [ td.string.strip() for td in td_list[1 : 6]  ]
                #使用正则表达式把真实数字从numberlist中提取出来
                real_number = [int(self.script_regex.findall(numberstring)[0]) for numberstring in numberlist]
                #一个很方便的列表初始化函数参数列表的方法 function(*list_name)
                reformat_code_info = reformated_code_information(*real_number)
                pass
            return reformat_code_info

    def get_metrix_complextity_info(self,  content_table):
        tr_list = content_table.find_all('tr')
        if len(tr_list) > 4:
            tr_list = tr_list[3:-2] #前面3行是固定的无用内容，后面2行是无用的内容
        else:
            tr_list = tr_list[3:]

        comlextity_list= []
        for tr in tr_list:
            td_list = tr.find_all('td')
            function_name , complextity_num = td_list[0].string.strip(), td_list[2].string.strip()
            number_mattched = self.script_regex.findall(complextity_num)
            if len(number_mattched) != 0: #testbed 报告每10个函数有一个空行
                complextity_num = int(number_mattched[0])
                comlextity_list.append((function_name , complextity_num ))
        return comlextity_list

    def analyse_html(self,file_url):
            """
            脚本文件主函数
            处理一个htlm文件
            将文件中规则违背情况抽取出来，放入列表，并返回
    
            Args:
                file_url: html文件路径
       
            Returns:
                如果这个文件包含规则违背情况，则返回详细情况的list
                如果这个文件包含规则违背情况，则返回空表
            方法：
                从每个文件中依次查找
                <a id="reformatted code information for file">Reformatted Code Information for File (TM.C)</a>
                <a id="complexity metrics">Complexity Metrics (UTIL.C)</a>
                <a id="dataflow information">Dataflow Information (UTIL.C)</a>
            """
            self.fileurl = file_url
            self.html = urlopen(file_url)
            self.bsObj = BeautifulSoup(self.html.read(), features="html.parser") 
            self.match_digital_string = '\d+\.?\d*' #匹配数字
            self.script_regex = re.compile(self.match_digital_string)
            

            #process all reformatted code information
            #list of reformated_code_information class instance
            reformat_codelist = []
            reformat_title_list = self.bsObj.find_all(u'a', id = u'reformatted code information for file')
            with open("temp_reformatted_code_info.dat",'w') as write_file:
                for reformat_tag in reformat_title_list:
                    write_file.write("%s\n" % reformat_tag)
                    for e in reformat_tag.parent.next_siblings:
                        if e.name == 'center':
                            content_table = e.find_all('table')[1] #获取第二个table
                            #获取第二个table中的tr
                            reformat_code_info = self.get_reformated_info(content_table)
                            reformat_codelist.append(reformat_code_info)
                            write_file.write("%s\n" % reformat_code_info)
                            #write_file.write('%s\n' % content_table)
                            write_file.flush()
                            break

            #process complexity metrics                    
            complexity_metrics_list = []
            complextity_title_list = self.bsObj.find_all(u'a', id = u'complexity metrics')
            with open("complexity_metrics_info.dat",'w') as write_file:
               for complextity_tag in complextity_title_list:
                    write_file.write("%s\n" % complextity_tag)
                    for e in complextity_tag.parent.next_siblings:
                        if e.name == 'center':
                            content_table = e.find_all('table')[1] #获取第二个table
                            metrix_info = self.get_metrix_complextity_info(content_table)
                            complexity_metrics_list.append(metrix_info)
                            write_file.write("%s\n" % '  '.join(str(e) for e in metrix_info))
                            write_file.flush()
                            break
                            
            pass
                    




if __name__ == '__main__':
    html = u"file:///C:/LDRA_Workarea/example_tbwrkfls/example.mts.htm"
    report = process_metrix_repot()
    report.analyse_html(html)