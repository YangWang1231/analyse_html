#!/usr/bin/python
 #coding:utf-8

#“”“
#构建LDRA_rule table
#”“”

from openpyxl import load_workbook
from store_db_sqlit3 import process_bd

#表格LDRA973-support-Gjb8114.xlsx的GJB8114-rule-details保存了对应关系
rule_xlsx_file_name = 'LDRA973-support-Gjb8114.xlsx'
rule_sheet_name = u'GJB8114-rule-details'

def build_LDRA_rule_table():
    """from LDRA973-support-Gjb8114.xlsx import information, and stroe to db"""
    db_obj = process_bd()
    
    wb = load_workbook(rule_xlsx_file_name)
    ws = wb[rule_sheet_name]

    for row in ws.values:
        print(row)
        GJB8114Code, LDRACode, MandatoryStanard_en, MandatoryStandard_ch, Rule_classification = row
        if GJB8114Code == None:     #处理多个testbedrule共同支持一条gjb8114规则的情况
            GJB8114Code = last_GJB8114_code
            MandatoryStandard_ch = last_MandatoryStandard_ch
            Rule_classification = last_Rule_classification
            
        Rule_classification = Rule_classification.upper()
        db_obj.insert_LDRA_rule((GJB8114Code, LDRACode, MandatoryStanard_en, MandatoryStandard_ch, Rule_classification))
        #save last item
        last_GJB8114_code = GJB8114Code
        last_MandatoryStandard_ch = MandatoryStandard_ch
        last_Rule_classification = Rule_classification

    db_obj.commit()


if __name__ == '__main__':
    build_LDRA_rule_table()
