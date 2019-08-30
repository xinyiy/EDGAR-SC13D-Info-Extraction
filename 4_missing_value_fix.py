#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 13:34:35 2019

@author: yxy
"""

import pandas as pd
from collections import Counter
import urllib.request
import re
from urllib.error import HTTPError
import os

Folder_Path = r'/Users/yxy/Downloads/secfilings_all_corrected'          
SaveFile_Path =  r'/Users/yxy/Downloads/secfilings_all_corrected_fixed'
os.chdir(Folder_Path)
file_list = os.listdir()
file_list.sort(key= lambda x:str(x[:4]))
print(file_list)

def filter_tags(htmlstr):

    re_cdata = re.compile('//<!\
    CDATA\[[ >]∗ //\
    CDATA\[[ >]∗ //\
    \] > ',re.I) 
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
 
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)

    re_br = re.compile('<br\s*?/?>')

    re_h = re.compile('</?\w+[^>]*>')

    re_comment = re.compile('<!--[^>]*-->')

    s = re_cdata.sub('', htmlstr)

    s = re_script.sub('', s)  
    s = re_style.sub('', s)

    s = re_br.sub('\n', s)

    s = re_h.sub('', s)  
    s = re_comment.sub('', s)


    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s) 
    return s

def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group() 
        key = sz.group('name')  
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
  
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string,s)

def Cleaning_data(x):
    m2=str(x).replace('<p>&nbsp; &nbsp; &nbsp; &nbsp;','').replace('</p><p><br></p>','').replace('<br>','').replace('</p>','').replace('<p>','').replace('       ','').replace('[图片]','').strip()
    m3=filter_tags(m2)
    m4=replaceCharEntity(m3)
    return m4

def clean(x):
    reg = re.compile('<[^>]*>')
    content = reg.sub('',x).replace('\n','').replace('    ','').replace('  ','').replace('\\n','').replace('\\t','').replace('  ','')
    return content

def addspace(s):
    s = s.replace('of',' of ').replace('of  ','of ').replace('  of',' of')
    s = s.replace('OF',' OF ').replace('OF  ','OF ').replace('  OF',' OF')
    s = s.replace('VOTING',' VOTING ').replace('VOTING  ','VOTING ').replace('  VOTING',' VOTING')
    s = s.replace('voting',' voting ').replace('voting  ','voting ').replace('  voting',' voting')
    s = s.replace('Amountin','Amount in') #22
    s = s.replace('AMOUNTIN','AMOUNT IN') #49
    s = s.replace('amountin','amount in') #23
    s = s.replace('aggregateamount', 'aggregate amount')
    s = s.replace('amountbeneficially', 'amount beneficially')
    s = s.replace('', '')
    s = s.replace('SeeInstructions','See Instructions') #49
    s = s.replace('seeInstructions','see Instructions') #18
    s = s.replace('Aggregateamount','Aggregate amount') #18
    s = s.replace('AGGREGATEAMOUNT','AGGREGATE AMOUNT') #45
    s = s.replace('AggregateAmount','Aggregate Amount')
    s = s.replace('Ownedby', 'Owned by')
    s = s.replace('reportingperson', 'reporting person')
    s = s.replace('AMOUT', 'AMOUNT')
    s = s.replace('AmountBeneficially', 'Amount Beneficially')
    s = s.replace('AGGREGATEDAMOUNT', 'AGGREGATED AMOUNT')
    s = s.replace('BENEFICIALLY OWNER', 'BENEFICIALLY OWNED')
    s = s.replace('Beneficially Owner', 'Beneficially Owned')
    s = s.replace('Aggregate Amount of Beneficially', 'Aggregate Amount Beneficially')
    s = s.replace('BENEFICALLY', 'BENEFICIALLY')
    s = s.replace('BENEFICIALLYOWNED', 'BENEFICIALLY OWNED')
    s = s.replace('SOLEDISPOSITIVE','SOLE DISPOSITIVE') #45
    s = s.replace('Shareddispositive','Shared dispositive') #18
    s = s.replace('SHAREDDISPOSITIVE','SHARED DISPOSITIVE') #45
    s = s.replace('SoleVoting','Sole Voting') #1
    s = s.replace('SharedVoting','Shared Voting') #1
    s = s.replace('SoleDispositive','Sole Dispositive') #1
    s = s.replace('SharedDispositive','Shared Dispositive') #1
    s = s.replace('9Sole Voting Power','9Sole Dispositive Power') #9
    s = s.replace('10Shared Voting Power','10Shared Dispositive Power') #9
    s = s.replace(':::','') #58
    s = s.replace(' Sole','Sole') #60
    s = s.replace(' Shared','Shared') #60
    s = s.replace('REPORTINGPERSON', 'REPORTING PERSON')
    s = s.replace('PERCENT OF CLASS REPRESENTED BY THE AMOUNT IN ROW', 'PERCENT OF CLASS REPRESENTED BY AMOUNT IN ROW')
    s = s.replace("Soledispositive", "Sole dispositive")
    s = s.replace("Shared Voting ", "Shared Voting Power")
    s = s.replace("Shared Voting PowerPower", "Shared Voting Power")
    s = s.replace("21.2(4)", "21.2%(4)") #46
    s = s.replace("BYEACH", "BY EACH")
    s = s.replace("9SOLE", "9. SOLE")
    s = s.replace("10SHARED", "10. SHARED")
    s = s.replace("11AGGREGATE", "11. AGGREGATE")
    s = s.replace("NAME OR REPORTING PERSONS", "NAME OF REPORTING PERSONS")
    s = s.replace("Percent of Class Represented byAmount in Row", "Percent of Class Represented by Amount in Row")
    s = s.replace("PERCENT OF CLASS REPRESENTED BYAMOUNT IN ROW", "PERCENT OF CLASS REPRESENTED BY AMOUNT IN ROW")
    s = s.replace("(Name of Company)", "(Name of Issuer)")
    s = s.replace("Communication)", "Communications)")
    s = s.replace("8SHARED VOTING POWER", "8. SHARED VOTING POWER")
    s = s.replace("SHARED OR NO VOTING POWER", "8. SHARED VOTING POWER")
    s = s.replace("8 SHARED VOTING POWER","8. SHARED VOTING POWER")
    s = s.replace("OWNEDBY", "OWNED BY")
    s = s.replace("byEach", "by Each")
    s = s.replace("EachReporting", "Each Reporting")
    s = s.replace("CHECKBOX", "CHECK BOX")
    s = s.replace("BeneficiallyOwned", "Beneficially Owned")
    s = s.replace("INROW", "IN ROW")
    s = s.replace("EACHREPORTING", "EACH REPORTING")
    s = s.replace("ReportingPerson", "Reporting Person")
    s = s.replace("Nubmer", "Number")
    s = s.replace("CUSIP Numbers", "CUSIP Number")
    s = s.replace("Name of Issuer:", "(Name of Issuer)")
    s = s.replace("Title of Class of Securities:", "(Title of Class of Securities)")
    s = s.replace("CUSIP Number:", "(CUSIP Number)")
    s = s.replace("SHARES DISPOSITIVE POWER", "SHARED DISPOSITIVE POWER")
    s = s.replace("EACHPERSON", "EACH PERSON")
    s = s.replace("DISPOSITIVEPOWER", "DISPOSITIVE POWER")
    s = s.replace("NAME OF REPORTING PERSON", "NAME OF REPORTING PERSONS")
    s = s.replace("Title and Class of Securities", "(Title of Class of Securities)")
    s = s.replace("AMOUNTBENEFICIALLY", "AMOUNT BENEFICIALLY")
    s = s.replace("CLASSREPRESENTED", "CLASS REPRESENTED")
    s = s.replace("REPRESENTEDBY", "REPRESENTED BY")
    s = s.replace("Name of Reporting Person", "Name of Reporting Person ")
    s = s.replace("Sh1red Voting Power", "Shared Voting Power")
    s = s.replace("DispositivePower", "Dispositive Power")
    s = s.replace("Titles of Class of Securities", "Title of Class of Securities")
    s = s.replace("7 SOLE VOTING POWER", "7SOLE VOTING POWER")
    s = s.replace("AGGREGATE AMOUNT OWNED BY EACH REPORTING PERSON", "AGGREGATE AMOUNT BENEFICIALLY OWNED BY EACH REPORTING PERSON")
    s = s.replace("PERCENT OF CLASS REPRESENTED BY ROW 11", "PERCENT OF CLASS REPRESENTED BY AMOUNT IN ROW (11)")
    s = s.replace("ClassRepresented", "Class Represented")
    s = s.replace("NAMES OF REPORTING PERSONSEOUL", "NAMES OF REPORTING PERSON SEOUL")
    s = s.replace("Name of Reporting Person s", "Name of Reporting Persons")
    s = s.replace("1NAME OF REPORTING PERSONS Cannell", "1NAMES OF REPORTING PERSONS Cannell")
    s = s.replace("percent of class represented by amount in row 11", "percent of class represented by amount in row (11)")
    s = s.replace("shareddispositive", "shared dispositive")
    s = s.replace("soledispositive", "sole dispositive")
    s = s.replace("Sole Dispositive7,500,000", "Sole Dispositive Power 7,500,000")
    s = s.replace("Sole dispositive voting power", "Sole dispositive power")
    s = s.replace("(2) CHECK THE", "(2)CHECK THE")
    s = s.replace("(2) Check the", "(2)Check the")
    s = s.replace("SHARE DISPOSITIVE POWER", "SHARED DISPOSITIVE POWER")
    s = s.replace("AbovePerson", "Above Person")
    s = s.replace("Percent of Class Representing by Amount in Row", "Percent of Class Represented by Amount in Row ")
    s = s.replace("Sole Voting Beneficially Owned Power", "Sole Voting Power")
    s = s.replace("PERCENT OF CLASS REPRESENTED BY AMOUNT IN ROW 11", "PERCENT OF CLASS REPRESENTED BY AMOUNT IN ROW (11)")
    s = s.replace("2) CHECK THE", "(2)CHECK THE")
    s = s.replace("(2) Check the", "(2)Check the")
    s = s.replace("SS. OR I.R.S. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("NAME OF PERSONNESTLE", "Names of Reporting Persons")
    s = s.replace("Name and I.R.S. Identification Number", "Names of Reporting Persons")
    s = s.replace("Title of Class and Securities", "Title of Class of Securities")
    s = s.replace("NAME OF REPORT PERSON", "NAME OF REPORTING PERSON")
    s = s.replace("NAME OF PERSON", "NAME OF REPORTING PERSON")
    s = s.replace("; S.S. or I.R.S. IdentificationNos. of Above Persons", "")
    s = s.replace("(no S.S. or I.R.S. Identification No.)", "")
    s = s.replace("*", "")
    s = s.replace("NAME OF REPORTING PERSONS", "NAMES OF REPORTING PERSONS")
    s = s.replace('classrepresented', 'class represented')
    s = s.replace('', '')
    s = s.replace('14.TYPER', '14.TYPE')
    s = s.replace('BYAMOUNT', 'BY AMOUNT')
    s = s.replace('PERCENT OF SERIES REPRESENTED', 'PERCENT OF CLASS REPRESENTED')
    s = s.replace('Title of Series of Securities', 'Title of Class of Securities')
    s = s.replace('Titleand', 'Title and')
    s = s.replace('TitleClass', 'Title Class')
    s = s.replace('Title and Class of Securities', 'Title of Class of Securities')
    s = s.replace('Title of Class Securities', 'Title of Class of Securities')
    s = s.replace('Title Class of Securities', 'Title of Class of Securities')
    s = s.replace('Title of Class and Securities', 'Title of Class of Securities')
    s = s.replace('Title of Securities', 'Title of Class of Securities')
    s = s.replace('CUSIPNumber', 'CUSIP Number')
    s = s.replace('12.Checkif', '12. Check if')
    s = s.replace('12.Check if', '12. Check if')
    s = s.replace('12 CHECK BOX', '12. CHECK BOX')
    s = s.replace('AGGREGATE AMOUNT OF BENEFICIALLY', 'AGGREGATE AMOUNT BENEFICIALLY')
    s = s.replace('Benefically', 'Beneficially')
    s = s.replace('PERCENT OF CLASS REPRESENTED BY AMOUNT ON ROW', 'PERCENT OF CLASS REPRESENTED BY AMOUNT IN ROW')
    s = s.replace('Beneficial Owned', 'Beneficially Owned')
    s = s.replace('12)CHECK', '12.CHECK')
    s = s.replace('(Title of Classes of Securities)', '(Title of Class of Securities)')
    s = s.replace('CUSIP NO.', 'CUSIP Number')
    s = s.replace('RepresentedbyAmount', 'Represented by Amount')
    s = s.replace('PERCENTAGE OF CLASS', 'PERCENT OF CLASS')
    s = s.replace('Percentage of Class', 'Percent of Class')
    s = s.replace('REPRESENTED TO AMOUNT IN ROW', 'REPRESENTED BY AMOUNT IN ROW')
    s = s.replace('VotingPower', 'Voting Power')
    return s

#cnt_file = open("/Users/yxy/Downloads/counter_file.txt", "w")
#cnt_file.close()

for p in range(18, len(file_list)):
#for p in range(13, 16):
#for p in range(,4):
    q = file_list[p]
    print(q)
    SaveFile_Name = r'fixed_' + q
    print(SaveFile_Name)
    
    df = pd.read_csv(Folder_Path +'/'+ q)
    
    l_col = list(df.columns) 
    l_svp_row = []
    l_sdp_row = []
    l_shvp_row = []
    l_shdp_row = []
    l_aa_row = [] # Rows with missing aggregate amount
    l_percent_row = [] # Rows with missing percentage
    l_cusip_row = [] # Rows with missing percentage CUSIP
    l_missing = []
    l_date = []
    
    for i in range(df.shape[0]):
        #print(i)
        l_temp = df.iloc[i].values.tolist()
        l_temp = map(str, l_temp)
        indices = [i for i, s in enumerate(l_temp) if 'Please' in s]
        if indices != []:
            for m in indices:
                l_missing.append(l_col[m])
            if l_col.index("Sole Voting Power") in indices:
                l_svp_row.append(i)
            if l_col.index("Sole Dispositive Power") in indices:
                l_sdp_row.append(i)
            if l_col.index("Shared Voting Power") in indices:
                l_shvp_row.append(i)
            if l_col.index("Shared Dispositive Power") in indices:
                l_shdp_row.append(i)
            if l_col.index("Aggregate Amount") in indices:
                l_aa_row.append(i)
            if l_col.index("Percent") in indices:
                l_percent_row.append(i)
            if l_col.index("CUSIP Number") in indices:
                l_cusip_row.append(i)
            if l_col.index("Date of Event") in indices:
                l_date.append(i)
                
    
    Counter(l_missing)
    cnt_file = open("/Users/yxy/Downloads/counter_file_dates.txt", "a+")
    cnt_file.write("\n")
    cnt_file.write(str(1994+p))
    cnt_file.write("\n")
    cnt_file.write(str(Counter(l_missing)))
    cnt_file.write("\n")
    cnt_file.close()




#%%
# CUSIP        
    for i in l_cusip_row:
        if i == 0 or df['File'][i] != df['File'][i-1]:
            #print(df['File'][i])
            with urllib.request.urlopen(df['File'][i]) as url:
                s = str(url.read())
                s = Cleaning_data(s)
                s = clean(s)
                s = addspace(s)
                
                try:
                    cusip_pattern = re.compile(r"(?<=Title of Class of Securities).*?(?=\(CUSIP Number\)|\(CUSIPNumber\)|\(CUSIP Number of Class of Securities\)|CUSIP Number|\(CUSIP No\.\))", re.IGNORECASE)
                    cusip = cusip_pattern.search(s).group().replace(" ","").replace("-","").replace("_","").replace("*", "").replace("(", "").replace(")", "").replace("=", "")
                    df['CUSIP Number'][i] = '"' + str(cusip) + '"'
                    print("CUSIP Row", i, df['CUSIP Number'][i])
                except AttributeError:
                    try:
                        cusip_pattern = re.compile(r"(?<=CUSIP NUMBER:).*?(?= NAME)", re.IGNORECASE)
                        cusip = cusip_pattern.search(s).group().replace(" ","").replace("-","").replace("_","").replace("*", "").replace("(", "").replace(")", "").replace("=", "")
                        df['CUSIP Number'][i] = '"' + str(cusip) + '"'
                        print("CUSIP Row", i, df['CUSIP Number'][i])
                    except AttributeError:
                        df['CUSIP Number'][i] = 'N/A' 
                        print("CUSIP Row", i, df['CUSIP Number'][i])
                        name = "/Users/yxy/Downloads/Missing/CUSIP_Missing_" + str(1994+p) + "_" + str(i) + ".txt"
                        file = open(name,"w") 
                        file.write(s) 
                        file.close()
                
        elif df['File'][i] == df['File'][i-1]:
            #print(df['File'][i])
            df['CUSIP Number'][i] = df['CUSIP Number'][i-1]
            print("CUSIP Row", i, df['CUSIP Number'][i])
            
# Sole Voting Power
    
# Sole Dispositive Power
    
# Shared Voting Power
    
# Shared Dispositive Power
 
# Aggregate Amount
    for i in l_aa_row:
        if i == 0 or df['File'][i] != df['File'][i-1]:
            with urllib.request.urlopen(df['File'][i]) as url:
                s = str(url.read())
                s = Cleaning_data(s)
                s = clean(s)
                s = addspace(s)
                
                aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially Owned by Each Reporting Person).*?(?=Units|12. CHECK BOX|shares|12CHECK|12.CHECK|. CHECK BOX|12. Check if|[(]|Units)", re.IGNORECASE)
                aa = aa_pattern.findall(s)
                if aa == []:
                    aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially Owned by the Reporting Person).*?(?=Units|12. CHECK BOX|shares|12CHECK|12.CHECK|. CHECK BOX|12. Check if|[(]|Units)", re.IGNORECASE)
                    aa = aa_pattern.findall(s)
                    if aa == []:
                        aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially Owned by each Person).*?(?=Units|12. CHECK BOX|shares|12CHECK|12.CHECK|. CHECK BOX|12. Check if|[(]|Units)", re.IGNORECASE)
                        aa = aa_pattern.findall(s)
                        if aa == []:
                            aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially Owned by reporting Person).*?(?=Units|12. CHECK BOX|shares|12CHECK|12.CHECK|. CHECK BOX|12. Check if|[(]|Units)", re.IGNORECASE)
                            aa = aa_pattern.findall(s)
                            if aa == []:
                                aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially).*?(?=Owned)", re.IGNORECASE)
                                aa = aa_pattern.findall(s)
                                if aa == []:
                                    aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially Owned by).*?(?=Each)", re.IGNORECASE)
                                    aa = aa_pattern.findall(s)
                print(aa)
                if aa == []:
                    df['Aggregate Amount'][i] = 'N/A'
                    name = "/Users/yxy/Downloads/Missing/AA_Missing_" + str(1994+p) + "_" + str(i) + ".txt"
                    file = open(name,"w") 
                    file.write(s) 
                    file.close()
                else:
                    for n in range(len(aa)):
                        print(df['Aggregate Amount'][i+n])
                        aa[n] = aa[n].lstrip("")
                        aa[n] = aa[n].replace("Common", "").replace("Stock", "").replace("of", "")
                        aa[n] = aa[n].replace("shares", "").replace("(1)", "").replace("(2)", "").replace("Redeemable", "")
                        aa[n] = aa[n].replace(" ", "").replace(":", "").replace("-", "").replace("/", "").replace("_", "").replace("(", "").replace(")", "")
                        aa[n] = aa[n].replace(".", "").replace("=", "").replace("#", "").replace('common', '')
                        if aa[n] == '':
                            aa[n] = 'N/A'
                        if df['File'][i+n] == df['File'][i]:
                            df['Aggregate Amount'][i+n] = aa[n]
                        else:
                            df['Aggregate Amount'][i+n] = "check"
                        print("AA Row", i+n, df['Aggregate Amount'][i+n])
# Percentage    
    for i in l_percent_row:
        if i == 0 or df['File'][i] != df['File'][i-1]:
            with urllib.request.urlopen(df['File'][i]) as url:
                s = str(url.read())
                s = Cleaning_data(s)
                s = clean(s)
                s = addspace(s)
                
                pcr_pattern = re.compile(r"(?<=PERCENT OF CLASS REPRESENTED BY AMOUNT IN ROW).*?(?=14. Type of|14.Type of|14Type of|Type of|14 TYPE|CUSIP)", re.IGNORECASE)
                pcr = pcr_pattern.findall(s)
                if pcr == []:
                    pcr_pattern = re.compile(r"(?<=Percent of Class Represented).*?(?=by Amount in Row)", re.IGNORECASE)
                    pcr = pcr_pattern.findall(s)
                #print(pcr)
                if pcr == []:
                    df['Percent'][i] = 'N/A'
                    name = "/Users/yxy/Downloads/Missing/PCR_Missing_" + str(1994+p) + "_" + str(i) + ".txt"
                    file = open(name,"w") 
                    file.write(s) 
                    file.close()
                else:
                    for n in range(len(pcr)):
                        pcr[n] = pcr[n].replace(" ", "").replace(":", "").replace("-", "").replace("(11)", "").replace("(", "").replace("_", "")
                        if pcr[n] == '':
                            pcr[n] = 'N/A'
                        if df['File'][i+n] == df['File'][i]:
                            df['Percent'][i+n] = pcr[n]
                        else:
                            df['Percent'][i+n] = "check"
                        print("PCR Row", i+n, df['Percent'][i+n])
    
    df.to_csv(SaveFile_Path+'/'+ SaveFile_Name, encoding="utf_8_sig",index=False)       
        
    l_col_2 = list(df.columns) 
    l_aa_row_2 = [] # Rows with missing aggregate amount
    l_percent_row_2 = [] # Rows with missing percentage
    l_cusip_row_2 = [] # Rows with missing percentage CUSIP
    l_missing_2 = []
    
    for i in range(df.shape[0]):
        l_temp_2 = df.iloc[i].values.tolist()
        l_temp_2 = map(str, l_temp_2)
        indices_2 = [i for i, s in enumerate(l_temp_2) if 'N/A' in s]
        if indices_2 != []:
            for m in indices_2:
                l_missing_2.append(l_col_2[m])
            if l_col_2.index("Aggregate Amount") in indices_2:
                l_aa_row_2.append(i)
            if l_col_2.index("Percent") in indices_2:
                l_percent_row_2.append(i)
            if l_col_2.index("CUSIP Number") in indices_2:
                l_cusip_row_2.append(i)
    
    #Counter(l_missing_2)
    cnt_file = open("/Users/yxy/Downloads/counter_file.txt", "a+")
    cnt_file.write("\n")
    cnt_file.write(str(1994+p))
    cnt_file.write("\n")
    cnt_file.write(str(Counter(l_missing_2)))
    cnt_file.write("\n")
    cnt_file.close()
    