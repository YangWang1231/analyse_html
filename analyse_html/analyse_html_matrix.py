#!/usr/bin/python
 #coding:utf-8
"""
 analyse_html_matrix.py主要作用是获取testben分析的质量度量结果
 包括：
 
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

TODO:
考虑用jison来存储这些信息，并发送给C#生成端程序，这样保证数据库格式与C#分离，在数据库格式修改的情况下，不需要修改C#软件
同理，规则分析的结果也通过jison发给C#生成端
 """






 
 