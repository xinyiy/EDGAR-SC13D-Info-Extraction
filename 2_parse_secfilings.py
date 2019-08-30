#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:01:03 2019

@author: yxy
"""

# In[1]:
import csv
import pandas as pd

#%% Import the index files

#df = pd.read_csv('~/Downloads/1994_sc13d.csv', sep='|', header = None)
df = pd.read_csv('~/Downloads/2019_secfiling_index.csv')
df.head()

#%% Extract SC13D files only

df13d = df[df.iloc[:,2].str.contains("13D")]
df13d = df13d.reset_index(drop = True)
df13d.to_csv(r'2019_SC13D.csv')
df13d.head(10)

df13d.describe()

#%% Clean HTML

def filter_tags(htmlstr):
    re_cdata = re.compile('//<!    CDATA\[[ >]∗ //    CDATA\[[ >]∗ //    \] > ',re.I) 
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

def digitonly(s):
    temp = filter(str.isdigit, s)
    a = "".join(temp)
    return a

def alphaonly(s):
    temp = filter(str.isalpha, s)
    a = "".join(temp)
    return a


#%% Data cleaning
def addspace(s):
    s = s.replace('of',' of ').replace('of  ','of ').replace('  of',' of')
    s = s.replace('OF',' OF ').replace('OF  ','OF ').replace('  OF',' OF')
    s = s.replace('VOTING',' VOTING ').replace('VOTING  ','VOTING ').replace('  VOTING',' VOTING')
    s = s.replace('voting',' voting ').replace('voting  ','voting ').replace('  voting',' voting')
    s = s.replace('Amountin','Amount in') #22
    s = s.replace('AMOUNTIN','AMOUNT IN') #49
    s = s.replace('amountin','amount in') #23
    s = s.replace('SeeInstructions','See Instructions') #49
    s = s.replace('seeInstructions','see Instructions') #18
    s = s.replace('Aggregateamount','Aggregate amount') #18
    s = s.replace('AGGREGATEAMOUNT','AGGREGATE AMOUNT') #45
    s = s.replace('AggregateAmount','Aggregate Amount')
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
    #s = s.replace("53632A 10 2Cusip Number", "53632A 10 2(Cusip Number)")
    s = s.replace("AMOUNTBENEFICIALLY", "AMOUNT BENEFICIALLY")
    s = s.replace("CLASSREPRESENTED", "CLASS REPRESENTED")
    s = s.replace("REPRESENTEDBY", "REPRESENTED BY")
    #s = s.replace("8Shared Voting3,539,643", "8Shared Voting Power3,539,643")
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
    #s = s.replace("Shared Voting3,539,643", "Shared Voting Power3,539,643")
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
    return s

def nprclean(s):
    s = s.replace("I.R.S. Identification Nos. of above persons (entities only)", "")
    s = s.replace("S.S. OR I.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS", "")
    s = s.replace("S.S. OR I.R.S. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("S.S. OR I.R.S. IDENTIFICATION NO. OF ABOVEPERSON", "")
    s = s.replace("S.S. OR I.R.S. IDENTIFICATION NO. OF ABOVE", "")
    s = s.replace("S.S. or I.R.S. Identification No. of Above Person", "")
    s = s.replace("S. Or I.R.S. Identification No. Of Above Person", "")
    s = s.replace("L.P.S.S. OR I.R.S. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("S.S. OR I.R.S IDENTIFICATION NO. OF ABOVE PERSONS", "")
    s = s.replace("(S.S. or I.R.S. Identification Nos. of Above Persons)", "")
    s = s.replace(".S. or I.R.S. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace(".S. or I.R.S. Identification No. of Above Person", "")
    s = s.replace("(SS )", "").replace("()", "").replace("SS ", "")
    s = s.replace(".S. or I.R.S. Identification No. of above person", "")
    s = s.replace(".S. OR I.R.S. IDENTIFICATION NOS. OF ABOVE PERSON", "")
    s = s.replace("2)", "").replace("|", "").replace("=", "")
    s = s.replace("1S.S. OR IRS. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("S.S. No.", "")
    s = s.replace(".S. or I.R.S. Identification Nos. of Above Persons", "")
    s = s.replace(".S. orI.R.S. Identification No. of Above Person", "")
    s = s.replace("S.S.", "")
    s = s.replace(".S. OR IRS. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("OF I.R.S. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("OR IRS IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("( OR I.R.S. IDENTIFICATION NO. OF REPORTING PERSON)", "")
    s = s.replace("OR IRSIDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("OR I.R.S.IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("ORI.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS", "")
    s = s.replace(". of I.R.S. Identification No. of Above Person", "")
    s = s.replace("or I.R.S. IdentificationNo. of Above Person", "")
    s = s.replace("OR I.R.S. IDENTIFICATION NUMBER OF ABOVEPERSONS", "")
    s = s.replace("or I.R.S.Identification Nos. of Above Persons", "")
    s = s.replace("or I.R.S.IdentificationNos. of Above Persons", "")
    s = s.replace("OR I.R.S IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("SS or IRS Identification No. of Above Person", "")
    s = s.replace("S.S OR I.R.S. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("1 OF ABOVE PERSON", "")
    s = s.replace("S. OR I.R.S. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("or I.R.S. IdentificationNos. of Above Persons", "")
    s = s.replace("IRS IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("OR IRS IDENTIFICATION NO OF ABOVE PERSON", "")
    s = s.replace("I.R.S. IDENTIFICATION NO. OF ABOVE PERSON (ENTITIES ONLY)", "")
    s = s.replace("I.R.S. IDENTIFICATION NO. OF ABOVE PERSONS (ENTITIES ONLY)", "")
    s = s.replace("SI.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS (ENTITIES ONLY)", "")
    s = s.replace("S I.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS (ENTITIES ONLY)", "")
    s = s.replace("S.I.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS (ENTITIES ONLY)", "")
    s = s.replace("or I.R.S. Identification Number of Above Person (optional)", "")
    s = s.replace("/ I.R.S. Identification Nos. of Above Persons (ENTITIES ONLY)", "")
    s = s.replace("I.R.S. Identification Nos. of Above Persons (Entities Only)", "")
    s = s.replace("I.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS (ENTITIES ONLY)", "")
    s = s.replace("OR I.R.S. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("or I.R.S. Identification No. of Person", "")
    s = s.replace("I.R.S. Identification Nos. of Above Persons (entities only)", "")
    s = s.replace("I.R.S. Identification No. of Above Persons (Entities Only)", "")
    s = s.replace("/  OR I.R.S. IDENTIFICATION OF ABOVE PERSON", "")
    s = s.replace("or IRS Identification Nos. of Above Person", "")
    s = s.replace("I.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS (entities only)", "")
    s = s.replace("or I.R.S. Identification Nos. of above persons", "")
    s = s.replace("or I.R.S. Identification No. of Reporting Person", "")
    s = s.replace("or I.R.S. Identification No. of above Person", "")
    s = s.replace("I.R.S. Identification No. of Above Person (entities only)", "")
    s = s.replace("I.R.S. Identification No. of above Person", "")
    s = s.replace("SS.S OR I.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS", "")
    s = s.replace("I.R.S. IDENTIFICATION NOS. OF ABOVE PERSON (ENTITIES ONLY)", "")
    s = s.replace("I.R.S. IDENTIFICATION NO. OF ABOVE PERSON", "")
    s = s.replace("I.R.S. Identification Number of Above Person (Entities Only).", "")
    s = s.replace("I.R.S. Identification Nos. Of Above Persons (entities only)", "")
    s = s.replace("I.R.S. Identification No. of above person (entities only)", "")
    s = s.replace("/I.R.S.Identification Nos. of Above Persons(Entities Only)", "")
    s = s.replace("S (entities only)", "")
    s = s.replace("I.R.S. Identification No. of Above Persons (entities only)", "")
    s = s.replace("(ENTITIES ONLY)", "")
    s = s.replace("orI.R.S.IdentificationNos. of Above Persons", "")
    s = s.replace("/I.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS", "")
    s = s.replace("S S", "")
    s = s.replace("SI.R.S. IDENTIFICATION NOS. OF ABOVE PERSONS", "")
    s = s.replace("OR I.R.S. IDENTIFICATION NUMBER OF ABOVE PERSON", "")
    s = s.replace("I.R.S. Identification Nos. of abovepersons (entities only).", "")
    s = s.lstrip("1").lstrip("1")
    s = s.replace("I.R.S. Identification Nos. of above Persons (entities only) ", "")
    return s


# In[9]:


def svpclean(s):
    s = s.replace("OWNED", "").replace("Owned", "").replace("owned", "")
    s = s.replace("WITH", "").replace("With", "").replace("with", "")
    s = s.replace("REPORTING", "").replace("Reporting", "").replace("reporting", "")
    s = s.replace("BENEFICIALLY", "").replace("Beneficially", "").replace("beneficially", "")
    s = s.replace("PERSON", "").replace("Person", "").replace("person", "")
    s = s.replace("BY", "").replace("By", "").replace("by", "")
    s = s.replace("EACH", "").replace("Each", "").replace("each", "")
    s = s.replace("common", "").replace("Common", "")
    s = s.replace("NUMBER OF", "").replace("Number of", "")
    s = s.replace("See Item 5", "").replace("Item 5", "").replace("SEE ITEM 5", "")
    s = s.replace("=", "").replace("|", "").replace("/", "")
    s = s.replace("ing", "").replace("of", "").replace("OF", "")
    s = s.replace("Report", "").replace("report", "")
    s = s.replace("(11)", "").replace("(","").replace(")","")
    s = s.replace("CHECK BOX IF THE AGGREGATE AMOUNT IN ROW", "")
    s = s.replace("Stock", "").replace("See discussion in", "")
    s = s.replace("respect to", "")
    s = s.rstrip("[")
    #s = s.replace("8 ","").replace("9 ", "").replace("10 ", "")
    s = s.split("Page")[0]
    s = s.split("See")[0]
    return s

#%% Main program - info extraction
    
import urllib.request
import re
import time
from urllib.error import HTTPError
#import eventlet
#eventlet.monkey_patch()

start = time.clock()
failedfiles = pd.DataFrame(columns=["Link"])
output = pd.DataFrame(columns=["CIK", "Name", "Type", "Date", "Link", "File", "Subject Company", "Subject Company CIK", "Filed Company", "Filed Company CIK", "Name of Issuer", "Title of Class of Securities", "CUSIP Number", "Date of Event", "Names of Reporting Persons", "Sole Voting Power", "Shared Voting Power", "Sole Dispositive Power", "Shared Dispositive Power", "Aggregate Amount", "Percent","Merger", "Acquisition", "Takeover", "Acquired", "Spinoff", "Reorganization", "Bankruptcy", "Distress", "Engage Managemant", "Undervalued", "Capital Structure", "Corporate Governance", "Business Strategy", "Strategic Alternatives", "Asset Sale", "Block Merger", "Financing", "Proxy", "Recapitalization", "Restructuring", "Board", "Poison Pill", "Director", "Schedule 14A", "Diversification", "Operating Strategy", "Business Line", "Fire", "Officer", "CEO", "Salary", "Cash Dividend", "Repurchase", "Buy Back", "Sell the Firm", "Sell the Company", "Underperforming Division", "Stock Issuance", "Debt Issuance", "Fraud", "Compensation", "Transparency"])
#output.describe()


name_of_issuer = []
cetral_index_key = []
title_of_class_of_Securities = []
CUSIP_number = []
date_of_event = []
name_of_reporting_persons = []
sole_voting_power = []
shared_voting_power = []
sole_dispositive_power = []
shared_dispositive_power = []
aggregate_amout = []
percent_of_class = []
mylist = ["Merger", "Acquisition", "Takeover", "Acquired", "Spinoff", "Reorganization", "Bankruptcy", "Distress", "Engage Managemant", "Undervalued", "Capital Structure", "Corporate Governance", "Business Strategy", "Strategic Alternatives", "Asset Sale", "Block Merger", "Financing", "Proxy", "Recapitalization", "Restructuring", "Board", "Poison Pill", "Director", "Schedule 14A", "Diversification", "Operating Strategy", "Business Line", "Fire", "Officer", "CEO", "Salary", "Cash Dividend", "Repurchase", "Buy Back", "Sell the Firm", "Sell the Company", "Underperforming Division", "Stock Issuance", "Debt Issuance", "Fraud", "Compensation", "Transparency"]

startn = 0
cnt = startn # To name the .txt files
filename = "try_2019_00000.csv"
failfilename = "2019_fails_00.csv"
for m in range(startn,df13d.count()[0]):
#for m in range(207,len(df)):
    #with eventlet.Timeout(90,False):
    URL = "https://www.sec.gov/Archives/" + df13d.iloc[m,4]
    cnt = cnt+1
    print(URL)
    try:
        with urllib.request.urlopen(URL) as url:
            s = str(url.read())
            s = Cleaning_data(s)
            s = clean(s)
            s = addspace(s)
            #print(s)

        if "999999999" in URL:
            pass
        else:
            # Preview the clean files
                name = "parsed_filings/file" + str(cnt) + ".txt"
                file = open(name,"w") 
                file.write(s) 
                file.close()
                print(cnt)
            ### Name of Issuer
                cname_pattern = re.compile("(?<=COMPANY CONFORMED NAME:).*?(?=CENTRAL)", re.IGNORECASE)
                cname = cname_pattern.findall(s)
                for i in range(len(cname)):
                    cname[i] = cname[i].rstrip("-")
                if cname == []:
                    cname = ["Please Check The File", "Please Check The File"]
                print(cname)
                #name_of_issuer.append(cname)
            ### CENTRAL INDEX KEY
                cik_pattern = re.compile(r"CENTRAL INDEX KEY:([0-9]*)", re.IGNORECASE)
                cik = cik_pattern.findall(s)
                if cik == []:
                    cik = ["Please Check The File", "Please Check The File"]
                print(cik)
            ### Title of Class of Securities
                try: 
                    tcs_pattern = re.compile(r"(?<=\(Name of Issuer\)).*?(?=\(Title of Class of Securities\))", re.IGNORECASE)
                    tcs = tcs_pattern.search(s).group().lstrip(" ").lstrip(".").lstrip(" ").replace("-", "").replace("_", "")
                except AttributeError:
                    try:
                        tcs_pattern = re.compile(r"(?<=\(Name of Issuer\)).*?(?=\(Title Class of Securities\))", re.IGNORECASE)
                        tcs = tcs_pattern.search(s).group().lstrip(" ").lstrip(".").lstrip(" ").replace("-", "").replace("_", "")
                    except AttributeError:
                        try:
                            tcs_pattern = re.compile(r"(?<=\(Name of Issuer\)).*?(?=\(Title of Class and Securities\))", re.IGNORECASE)
                            tcs = tcs_pattern.search(s).group().lstrip(" ").lstrip(".").lstrip(" ").replace("-", "").replace("_", "")
                        except AttributeError:
                            #! EDITS START HERE
                            try:
                                tcs_pattern = re.compile(r"(?<=\(Name of Issuer\)).*?(?=\(Title of Securities\))", re.IGNORECASE)
                                tcs = tcs_pattern.search(s).group().lstrip(" ").lstrip(".").lstrip(" ").replace("-", "").replace("_", "")
                            except:
                                tcs = '' # set tcs to missing if none of the four patterns above are found in string s
                            #! EDITS END HERE -- IN PLACE OF THESE EDITS, THE FOLLOWING 2 LINES HAD BEEN USED (NOW COMMENTED OUT)
                            #tcs_pattern = re.compile(r"(?<=\(Name of Issuer\)).*?(?=\(Title of Securities\))", re.IGNORECASE)
                            #tcs = tcs_pattern.search(s).group().lstrip(" ").rstrip("-").lstrip("_").rstrip("_")
                print(tcs)
            ### CUSIP Number 
                try:
                    cusip_pattern = re.compile(r"(?<=\(Title of Class of Securities\)).*?(?=\(CUSIP Number\)|\(CUSIPNumber\)|\(CUSIP Number of Class of Securities\))", re.IGNORECASE)
                    cusip = cusip_pattern.search(s).group().replace(" ","").replace("-","").replace("_","").replace("*", "")
                    cusip = '"' + str(cusip) + '"'
                except AttributeError:
                    try:
                        cusip_pattern = re.compile(r"(?<=\(Title Class of Securities\)).*?(?=\(CUSIP Number\)|\(CUSIPNumber\)|\(CUSIP Number of Class of Securities\))", re.IGNORECASE)
                        cusip = cusip_pattern.search(s).group().replace(" ","").replace("-","").replace("_","").replace("*", "")
                        cusip =  '"' + str(cusip) + '"'
                    except AttributeError:
                        try:
                            cusip_pattern = re.compile(r"(?<=\(Title of Class and Securities\)).*?(?=\(CUSIP Number\)|\(CUSIPNumber\)|\(CUSIP Number of Class of Securities\))", re.IGNORECASE)
                            cusip = cusip_pattern.search(s).group().replace(" ","").replace("-","").replace("_","").replace("*", "")
                            cusip = '"' + str(cusip) + '"'
                        except AttributeError:
                            try:
                                cusip_pattern = re.compile(r"(?<=\(Title of Securities\)).*?(?=\(CUSIP Number\)|\(CUSIPNumber\)|\(CUSIP Number of Class of Securities\))", re.IGNORECASE)
                                cusip = cusip_pattern.search(s).group().replace(" ","").replace("-","").replace("_","").replace("*", "")
                                cusip = '"' + str(cusip) + '"'
                            except AttributeError:
                                cusip = "Please Check The Original Text"
                print(cusip)
            ### Date of Event Which Requires Filing of this Statement
                try:
                    de_pattern = re.compile(r"(?<=Communications\)).*?(?=\(Date)", re.IGNORECASE)
                    de = de_pattern.search(s).group().lstrip(" ").rstrip(" ").replace("_","").replace("-", "").lstrip(" ")
                except AttributeError:
                    try:
                        de_pattern = re.compile(r"(?<=Communications).*?(?=\(Date)", re.IGNORECASE)
                        de = de_pattern.search(s).group().lstrip(" ").rstrip(" ").replace("_","").replace("-", "").lstrip(" ")
                    except AttributeError:
                        try:
                            de_pattern = re.compile(r"(?<=DATE OF EVENT WHICH REQUIRES FILING OF THIS STATEMENT).*?(?=1. NAME)", re.IGNORECASE)
                            de = de_pattern.search(s).group().lstrip(" ").rstrip(" ").replace("_","").replace("-", "").lstrip(" ")
                        except AttributeError:
                            de = "Please Check The Original Text"
                print(de)
            ### NAMES OF REPORTING PERSONS
                nrp_pattern = re.compile(r"(?<=Names of Reporting Persons).*?(?=Check the appropriate box|2check|2 check|2\.check|2\. check|\(2\)Check)", re.IGNORECASE)
                nrp = nrp_pattern.findall(s)
                if nrp == []:
                    nrp_pattern = re.compile(r"(?<=Name of Reporting Persons).*?(?=Check the appropriate box|2check|2 check|2\.check|2\. check|\(2\)Check)", re.IGNORECASE)
                    nrp = nrp_pattern.findall(s)
                if nrp == []:
                    nrp_pattern = re.compile(r"(?<=Names of Reporting Person).*?(?=Check the appropriate box|2check|2 check|2\.check|2\. check|\(2\)Check)", re.IGNORECASE)
                    nrp = nrp_pattern.findall(s)
                if nrp == []:
                    nrp_pattern = re.compile(r"(?<=Name of Reporting Person).*?(?=Check the appropriate box|2check|2 check|2\.check|2\. check|\(2\)Check)", re.IGNORECASE)
                    nrp = nrp_pattern.findall(s)
                for i in range(len(nrp)):
                    nrp[i] = nprclean(nrp[i])
                    nrp[i] = nrp[i].lstrip(".")
                    nrp[i] = nrp[i].strip(" ").lstrip(".").lstrip(" ").replace("_","").replace("-","").replace("(1)","").replace(":","").replace("#" ,"").replace("\\", "")
                    nrp[i] = nrp[i].rstrip(".").lstrip(" ").rstrip(" ")
                nrp_ = list(filter(lambda a: a != "", nrp))

            ### SOLE VOTING POWER
                svp_pattern = re.compile(r"(?<=7Sole Voting Power).*?(?=Units|shares|8. SHARED|8.SHARED VOTING POWER|8SHARED|10Shared Voting Power|8 Shared Voting|[(]|VOTING SHARES|Number|SHARED VOTING POWER)", re.IGNORECASE)
                svp = svp_pattern.findall(s)
                if svp == []:
                    svp_pattern = re.compile(r"(?<=Sole Voting Power).*?(?=Units|shares|8. SHARED|8.SHARED VOTING POWER|8SHARED|10Shared Voting Power|8 Shared Voting|[(]|VOTING SHARES|Number|SHARED VOTING POWER)", re.IGNORECASE)
                    svp = svp_pattern.findall(s)
                for i in range(len(svp)):
                    svp[i] = svpclean(svp[i])
                    svp[i] = svp[i].replace("(1)","").replace("*","").replace("-","").replace(":","").replace("_", "")
                    svp[i] = svp[i].lstrip(".").lstrip(" ").rstrip(" ").lstrip(".").rstrip(".")
                    if svp[i] == '' or svp[i] == "None" or svp[i] == "N/A":
                        svp[i] = "0"
                #svp = digitonly(svp)
                if len(nrp_) == len(svp):
                    print(nrp_)
                    print(svp)
                elif len(nrp_) > len(svp):
                    for i in range(len(nrp_)-len(svp)):
                        svp.append("Please Check The File")
                    print(nrp_)
                    print(svp)
                else:
                    nrp_ = nrp_[0:len(svp)]
                    print(nrp_)
                    print(svp)
                    print('\x1b[6;30;42m' + '!!!!!MIGHT BE A PROBLEM HERE!!!!!' + '\x1b[0m')
                    
            ### SHARED VOTING POWER
                shvp_pattern = re.compile(r"(?<=SHARED VOTING POWER).*?(?=Units|9SOLE DISPOSITIVE|9. SOLE|9.SOLE|SOLE DISPOSITIVE POWER|shares|11Aggregate Amount|[(])", re.IGNORECASE)
                shvp = shvp_pattern.findall(s)
                #print(shvp)
                for i in range(len(shvp)):
                    shvp[i] = svpclean(shvp[i])
                    #print(shvp[i])
                    #shvp[i] = digitonly(shvp[i]).lstrip(" ").rstrip(" ")
                    shvp[i] = shvp[i].replace("*","").replace("-","").replace(":","").replace("_", "")
                    shvp[i] = shvp[i].lstrip(".").lstrip(" ").rstrip(" ").lstrip(".").rstrip(".")
                    if shvp[i] == '' or shvp[i] == "None" or shvp[i] == "N/A":
                        shvp[i] = "0"
                    #print(shvp[i])
                if shvp == [] or len(shvp)!=len(nrp_):
                    for i in range(len(nrp_)-len(shvp)):
                        shvp.append("Please Check The File")
                #shvp = digitonly(shvp)
                print(shvp)
            ### SOLE DISPOSITIVE POWER
                sdp_pattern = re.compile(r"(?<=SOLE DISPOSITIVE POWER).*?(?=Units|shares|10SHARED|VOTING SHARES|10. SHARED|10.SHARED DISPOSITIVE POWER|SHARED DISPOSITIVE POWER|11Aggregate|[(])", re.IGNORECASE)
                sdp = sdp_pattern.findall(s)
                for i in range(len(sdp)):
                    sdp[i] = svpclean(sdp[i])
                    #sdp[i] = digitonly(sdp[i])
                    sdp[i] = sdp[i].replace("_","").replace("*","").replace("-","").replace(":","").replace("_", "")
                    sdp[i] = sdp[i].lstrip(".").lstrip(" ").rstrip(" ").lstrip(".").rstrip(".")
                    if sdp[i] == '' or sdp[i] == "None" or sdp[i] == "N/A":
                        sdp[i] = "0"
                if sdp == [] or len(sdp)!=len(nrp_):
                    for i in range(len(nrp_)-len(sdp)):
                        sdp.append("Please Check The File")
                print(sdp)
            ### SHARED DISPOSITIVE POWER
                shdp_pattern = re.compile(r"(?<=SHARED DISPOSITIVE POWER).*?(?=Units|11Aggregate|11. AGGREGATE|11.Aggregate Amount Beneficially|shares|[(]|Aggregate)", re.IGNORECASE)
                shdp = shdp_pattern.findall(s)
                for i in range(len(shdp)):
                    shdp[i] = svpclean(shdp[i])
                    #shdp[i] = digitonly(shdp[i]).lstrip(".").lstrip(" ").lstrip("-").rstrip("-").rstrip(" ")
                    shdp[i] = shdp[i].replace("*","").replace("-","").replace(":","").replace("_", "")
                    shdp[i] = shdp[i].lstrip(".").lstrip(" ").rstrip(" ").lstrip(".").rstrip(".")
                    if shdp[i] == '' or shdp[i] == "None" or shdp[i] == "N/A":
                        shdp[i] = "0"
                #shdp = digitonly(shdp)
                if shdp == [] or len(shdp)!=len(nrp_):
                    for i in range(len(nrp_)-len(shdp)):
                        shdp.append("Please Check The File")
                print(shdp)
            ### AGGREGATE AMOUNT BENEFICIALLY OWNED BY EACH REPORTING PERSON
                aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially Owned by Each Reporting Person).*?(?=Units|12. CHECK BOX|shares|12CHECK|12.CHECK|. CHECK BOX|12. Check if|[(])", re.IGNORECASE)
                aa = aa_pattern.findall(s)
                if aa == []:
                    aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially Owned by the Reporting Person).*?(?=Units|12. CHECK BOX|shares|12CHECK|12.CHECK|. CHECK BOX|12. Check if|[(])", re.IGNORECASE)
                    aa = aa_pattern.findall(s)
                    if aa == []:
                        aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially Owned by each Person).*?(?=Units|12. CHECK BOX|shares|12CHECK|12.CHECK|. CHECK BOX|12. Check if|[(])", re.IGNORECASE)
                        aa = aa_pattern.findall(s)
                        if aa == []:
                            aa_pattern = re.compile(r"(?<=Aggregate Amount Beneficially Owned by reporting Person).*?(?=Units|12. CHECK BOX|shares|12CHECK|12.CHECK|. CHECK BOX|12. Check if|[(])", re.IGNORECASE)
                            aa = aa_pattern.findall(s)
                for i in range(len(aa)):
                    #aa[i] = digitonly(aa[i])
                    aa[i] = svpclean(aa[i])
                    aa[i] = aa[i].lstrip(".").lstrip(" ").rstrip(" ").replace("*","").replace("-","").replace(":","").replace("_", "")
                    aa[i] = aa[i].lstrip(" ").rstrip(" ").lstrip(".").rstrip(".")
                    if aa[i] == '' or aa[i] == "None" or aa[i] == "N/A" in aa:
                        aa[i] = "0"
                #aa = digitonly(aa)
                if aa == [] or len(aa)!=len(nrp_):
                    for i in range(len(nrp_)-len(aa)):
                        aa.append("Please Check The File")
                print(aa)
            ### PERCENT OF CLASS REPRESENTED BY AMOUNT IN ROW 
                pcr_ = []
                pcr_pattern = re.compile(r"(?<=PERCENT OF CLASS REPRESENTED BY AMOUNT IN ROW).*?(?=14. Type of|14.Type of|14Type of|Type of|14 TYPE|CUSIP)", re.IGNORECASE)
                pcr = pcr_pattern.findall(s)
                if pcr == []:
                    for i in range(len(svp)):
                        pcr.append(str(0))
                else:
                #print(pcr)
                    for i in range(len(pcr)):
                        pcr[i] = pcr[i].replace("*","").replace("-", "")
                        num_pattern = re.compile(r"([0-9.]+)[ ]*%|0")
                        try:
                            pcr_.append(num_pattern.search(pcr[i]).group())
                        except AttributeError:
                            pcr_.append(str(0))
                    #pcr_.append(pcr[i])
                if pcr_ == [] or len(pcr_)!=len(nrp_):
                    for i in range(len(svp) - len(pcr_)):
                        pcr_.append("Please Check The File")
                for i in range(len(pcr_)):
                    pcr_[i] = svpclean(pcr_[i])
                    #pcr_[i] = pcr[i].lstrip(".")
                print(pcr_)


            ### Purpose of Transaction
                pot_list = []
                pot_pattern = re.compile(r"(?<=Item 4).*?(?=Item 5|SIGNATURES)", re.IGNORECASE)
                try:
                    item4 = pot_pattern.search(s).group()
                    #print(item4)
                    for i in mylist:
                        pattern = re.compile(i, re.IGNORECASE)
                        a = pattern.findall(item4)
                        if a == []:
                            pot_list.append(0)
                        else:
                            pot_list.append(1) 
                    print(pot_list)
                except AttributeError:
                    pot_list = []
                    print("No Item4.")

                    #if nrp_==[] or " " in svp[i] or " " in shvp[i] or " " in sdp[i] or " " in shdp[i] or "Please Check The File" in shvp[i] or "Please Check The File" in sdp[i] or "Please Check The File" in shdp[i] or "Please Check The File" in aa[i] or "Please Check The File" in pcr_[i]:
                if nrp_==[]:
                    failoutput = pd.DataFrame(index=range(0,1), columns=["Link"])
                    failoutput["Link"] = "https://www.sec.gov/Archives/" + df13d.iloc[m,5]
                    failedfiles = failedfiles.append(failoutput, ignore_index=True)
                    failedfiles.to_csv(failfilename, float_format='{:f}'.format, encoding='utf-8', index = False)

            ### Write the information into the output file
                df_temp = pd.DataFrame(index=range(len(nrp_)), columns=["CIK", "Name", "Type", "Date", "Link", "File", "Subject Company", "Subject Company CIK", "Filed Company", "Filed Company CIK", "Name of Issuer", "Title of Class of Securities", "CUSIP Number", "Date of Event", "Names of Reporting Persons", "Sole Voting Power", "Shared Voting Power", "Sole Dispositive Power", "Shared Dispositive Power", "Aggregate Amount", "Percent","Merger", "Acquisition", "Takeover", "Acquired", "Spinoff", "Reorganization", "Bankruptcy", "Distress", "Engage Managemant", "Undervalued", "Capital Structure", "Corporate Governance", "Business Strategy", "Strategic Alternatives", "Asset Sale", "Block Merger", "Financing", "Proxy", "Recapitalization", "Restructuring", "Board", "Poison Pill", "Director", "Schedule 14A", "Diversification", "Operating Strategy", "Business Line", "Fire", "Officer", "CEO", "Salary", "Cash Dividend", "Repurchase", "Buy Back", "Sell the Firm", "Sell the Company", "Underperforming Division", "Stock Issuance", "Debt Issuance", "Fraud", "Compensation", "Transparency"])
                for i in range(len(nrp_)):
                    df_temp["CIK"] = df13d.iloc[m,0]
                    df_temp["Name"] = df13d.iloc[m,1]
                    df_temp["Type"] = df13d.iloc[m,2]
                    df_temp["Date"] = df13d.iloc[m,3]
                    df_temp["Link"] = "https://www.sec.gov/Archives/" + df13d.iloc[m,5]
                    df_temp["File"] = "https://www.sec.gov/Archives/" + df13d.iloc[m,4]
                    df_temp["Subject Company"][i] = cname[0]
                    df_temp["Subject Company CIK"][i] = cik[0]
                    df_temp["Filed Company"][i] = cname[1]
                    df_temp["Filed Company CIK"][i] = cik[1]
                    df_temp["Name of Issuer"][i] = cname[1]
                    df_temp["Title of Class of Securities"][i] = tcs
                    df_temp["CUSIP Number"][i] = cusip
                    df_temp["Date of Event"][i] = de
                    df_temp["Names of Reporting Persons"][i] = nrp_[i]
                    df_temp["Sole Voting Power"][i] = svp[i]
                    df_temp["Shared Voting Power"][i] = shvp[i]
                    df_temp["Sole Dispositive Power"][i] = sdp[i]
                    df_temp["Shared Dispositive Power"][i] = shdp[i]
                    df_temp["Aggregate Amount"][i] = aa[i]
                    df_temp["Percent"][i] = pcr_[i]

                    if pot_list == []:
                        df_temp["Merger"][i] = 0
                        df_temp["Acquisition"][i] = 0
                        df_temp["Takeover"][i] = 0
                        df_temp["Acquired"][i] = 0
                        df_temp["Spinoff"][i] = 0
                        df_temp["Reorganization"][i] = 0
                        df_temp["Bankruptcy"][i] = 0
                        df_temp["Distress"][i] = 0
                        df_temp["Engage Managemant"][i] = 0
                        df_temp["Undervalued"][i] = 0
                        df_temp["Capital Structure"][i] = 0
                        df_temp["Corporate Governance"][i] = 0
                        df_temp["Business Strategy"][i] = 0
                        df_temp["Strategic Alternatives"][i] = 0
                        df_temp["Asset Sale"][i] = 0
                        df_temp["Block Merger"][i] = 0
                        df_temp["Proxy"][i] = 0
                        df_temp["Recapitalization"][i] = 0
                        df_temp["Restructuring"][i] = 0
                        df_temp["Board"][i] = 0
                        df_temp["Financing"][i] = 0
                        df_temp["Director"][i] = 0
                        df_temp["Poison Pill"][i] = 0
                        df_temp["Schedule 14A"][i] = 0
                        df_temp["Diversification"][i] = 0
                        df_temp["Operating Strategy"][i] = 0
                        df_temp["Business Line"][i] = 0
                        df_temp["Fire"][i] = 0
                        df_temp["Officer"][i] = 0
                        df_temp["CEO"][i] = 0
                        df_temp["Salary"][i] = 0
                        df_temp["Cash Dividend"][i] = 0
                        df_temp["Repurchase"][i] = 0
                        df_temp["Buy Back"][i] = 0
                        df_temp["Sell the Firm"][i] = 0
                        df_temp["Sell the Company"][i] = 0
                        df_temp["Underperforming Division"][i] = 0
                        df_temp["Stock Issuance"][i] = 0
                        df_temp["Debt Issuance"][i] = 0
                        df_temp["Fraud"][i] = 0
                        df_temp["Compensation"][i] = 0
                        df_temp["Transparency"][i] = 0
                    else:
                        df_temp["Merger"][i] = pot_list[0]
                        df_temp["Acquisition"][i] = pot_list[1]
                        df_temp["Takeover"][i] = pot_list[2]
                        df_temp["Acquired"][i] = pot_list[3]
                        df_temp["Spinoff"][i] = pot_list[4]

                        df_temp["Reorganization"][i] = pot_list[5]
                        df_temp["Bankruptcy"][i] = pot_list[6]
                        df_temp["Distress"][i] = pot_list[7]
                        df_temp["Engage Managemant"][i] = pot_list[8]
                        df_temp["Undervalued"][i] = pot_list[9]

                        df_temp["Capital Structure"][i] = pot_list[10]
                        df_temp["Corporate Governance"][i] = pot_list[11]
                        df_temp["Business Strategy"][i] = pot_list[12]
                        df_temp["Strategic Alternatives"][i] = pot_list[13]
                        df_temp["Asset Sale"][i] = pot_list[14]

                        df_temp["Block Merger"][i] = pot_list[15]
                        df_temp["Financing"][i] = pot_list[16]
                        df_temp["Proxy"][i] = pot_list[17]
                        df_temp["Recapitalization"][i] = pot_list[18]
                        df_temp["Restructuring"][i] = pot_list[19]

                        df_temp["Board"][i] = pot_list[20]
                        df_temp["Poison Pill"][i] = pot_list[21]             
                        df_temp["Director"][i] = pot_list[22]             
                        df_temp["Schedule 14A"][i] = pot_list[23]
                        df_temp["Diversification"][i] = pot_list[24]

                        df_temp["Operating Strategy"][i] = pot_list[25]
                        df_temp["Business Line"][i] = pot_list[26]
                        df_temp["Fire"][i] = pot_list[27]
                        df_temp["Officer"][i] = pot_list[28]
                        df_temp["CEO"][i] = pot_list[29]

                        df_temp["Salary"][i] = pot_list[30]
                        df_temp["Cash Dividend"][i] = pot_list[31]
                        df_temp["Repurchase"][i] = pot_list[32]
                        df_temp["Buy Back"][i] = pot_list[33]
                        df_temp["Sell the Firm"][i] = pot_list[34]

                        df_temp["Sell the Company"][i] = pot_list[35]
                        df_temp["Underperforming Division"][i] = pot_list[36]
                        df_temp["Stock Issuance"][i] = pot_list[37]
                        df_temp["Debt Issuance"][i] = pot_list[38]
                        df_temp["Fraud"][i] = pot_list[39]

                        df_temp["Compensation"][i] = pot_list[40]
                        df_temp["Transparency"][i] = pot_list[41]
                #print(df_temp)
                output = output.append(df_temp, ignore_index=True)
                elapsed = (time.clock() - start)
                print("Time used:",elapsed)

                print("\n")
                output.to_csv(filename, float_format='{:f}'.format, encoding='utf-8', index = False)
    except HTTPError:
        try: 
            pass
        except NameError:
            pass

