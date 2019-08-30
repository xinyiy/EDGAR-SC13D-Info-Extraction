"""
@author: yxy
"""

# coding: utf-8

import pandas as pd
import os

#%% Merge downloeaded files (orginnaly spilt by quarters)

Folder_Path = r'/Users/yxy/Downloads/merge_sec_output_index_2019'          
SaveFile_Path =  r'/Users/yxy/Downloads'       
SaveFile_Name = r'2019_secfiling_index.csv'       # Change      

os.chdir(Folder_Path)
file_list = os.listdir()
file_list.sort(key= lambda x:str(x[:-4]))
print(file_list)

file_list.pop(0) # Comment out if the first file name is not "_DS.Store"
print(file_list)

df = pd.read_csv(Folder_Path +'/'+ file_list[0], sep='|', header = None)
df.to_csv(SaveFile_Path+'/'+ SaveFile_Name,encoding="utf_8_sig",index=False)


for i in range(1,len(file_list)):
    df = pd.read_csv(Folder_Path + '/'+ file_list[i], sep='|', header = None)
    df.to_csv(SaveFile_Path+'/'+ SaveFile_Name,encoding="utf_8_sig",index=False, header=False, mode='a+')
    
#%% Merge unparseable filings
Folder_Path = r'/Users/yxy/Downloads/merge_sec_output_failed_2018'          
SaveFile_Path =  r'/Users/yxy/Downloads'       
SaveFile_Name = r'2018_secfiling_failed.csv'

os.chdir(Folder_Path)
file_list = os.listdir()
file_list.sort(key= lambda x:str(x[:-4]))
print(file_list)

file_list.pop(0) # Comment out if the first file name is not "_DS.Store"
print(file_list)

df = pd.read_csv(Folder_Path +'/'+ file_list[0])
df.to_csv(SaveFile_Path+'/'+ SaveFile_Name, encoding="utf_8_sig",index=False)


for i in range(1,len(file_list)):
    df = pd.read_csv(Folder_Path + '/'+ file_list[i])
    df.to_csv(SaveFile_Path+'/'+ SaveFile_Name, encoding="utf_8_sig",index=False, header=False, mode='a+')

#%% Merge files with extracted information
Folder_Path = r'/Users/yxy/Downloads/merge_sec_output_2018'          
SaveFile_Path =  r'/Users/yxy/Downloads'       
SaveFile_Name = r'2018_secfiling_all.csv'

os.chdir(Folder_Path)
file_list = os.listdir()
file_list.sort(key= lambda x:str(x[:-4]))
print(file_list)

file_list.pop(0) # Comment out if the first file name is not "_DS.Store"
print(file_list)

df = pd.read_csv(Folder_Path +'/'+ file_list[0])
df.to_csv(SaveFile_Path+'/'+ SaveFile_Name, encoding="utf_8_sig",index=False)


for i in range(1,len(file_list)):
    df = pd.read_csv(Folder_Path + '/'+ file_list[i])
    df.to_csv(SaveFile_Path+'/'+ SaveFile_Name, encoding="utf_8_sig",index=False, header=False, mode='a+')

