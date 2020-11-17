from bs4 import BeautifulSoup
import sys
import os
import xlwt
from xlwt import Workbook
from xlrd import open_workbook
from xlutils.copy import copy

                
def find_algo_name(str_str):

    t=str_str.find("html")
    str_str=str_str[:t]
    str_lst=str_str.split('.')
    str_lst=[v for v in str_lst if v]
    return str_lst[-1]

if __name__=="__main__":
    root_dir="/home/shmoon/algorithm_parameter_parser/html/"
    wb=xlwt.Workbook(encoding='utf-8')
    for(root, dirs,files) in os.walk(root_dir):
        if len(files) > 0:
            for file_name in files:
                html_title=file_name
                with open(root_dir+html_title,'r',-1,"utf-8") as fp:
                    soup=BeautifulSoup(fp,'html.parser')
                    all_divs=soup.find('dl',{'class':'field-list'})

                tags_all=all_divs.find_all('dt')

                tags=[]
                for i in range(0,len(tags_all)):
                    tags.append(tags_all[i])
                
                # getting names
                tag_count=0
                names=[]
                for i in range(1,len(tags)):
                    try:
                        names.append(tags[i].find('strong').get_text())
                        tag_count=tag_count+1
                    except AttributeError:
                        break

                # getting info
                info=[]
                for i in range(1,len(tags)):
                    try:
                        info.append(tags[i].find('span').get_text())
                    except AttributeError:
                        break
                
                # getting tag default and type
                tag_dft=[]
                tag_type=[]

                for i in range(0,tag_count):
                    spl=info[i].split('default')
                    tag_dft.append(spl[1])
                    tag_type.append(spl[0])
                
                # type 형성
                types=[]
    
                # string type 
                strings=[]

                for i in range(tag_count):
                    types.append([])
                    strings.append([])
                    
                    # put strings
                    b_s=tag_type[i].find('{')
                    b_e=tag_type[i].find('}')
                    
                    if(b_s!=-1): # if string is included
                        temp=tag_type[i][b_s+1:b_e]
                        for j in temp.split(','):
                            # to put commas instead of blanks
                            j=j.replace('’','’,')
                            j=j.replace('”','”,')
                            strings[i].append(j)
                            temp2=tag_type[i][:b_s]+tag_type[i][b_e+1:]
                            temp2=temp2.replace('or',',').split(',')
                            types[i]=[v.strip()+', ' for v in temp2 if not not v.split()]
                            types[i].append('string')
                    else: # if string is not included
                        temp2=tag_type[i]
                        temp2=temp2.replace('or',',').split(',')
                        types[i]=[v.strip()+', ' for v in temp2 if not not v.split()]

                # defaults
                defaults=[]
                # nones
                nones=[]
    
                for i in range(tag_count):
                    defaults.append([])
                    nones.append([])
    
                    temp=tag_dft[i].split('=')[-1]
                    if temp=='None':
                        nones[i].append('True')
                        defaults[i].append('None')
                    else:
                        nones[i].append('False')
                        defaults[i].append(temp)

                
                algo_name=find_algo_name(html_title)
                sheet1=wb.add_sheet(algo_name)
                sheet1.write(3,0,"파라메터 번호")
                sheet1.write(3,1,"파라메터 이름")
                sheet1.write(3,2,"types")
                sheet1.write(3,3,"strings")
                sheet1.write(3,4,"default")
                sheet1.write(3,5,"none")
                sheet1.write(3,6,"중요도")
                sheet1.write(3,7,"공개 여부")
        
                for i in range(tag_count):
                    sheet1.write(i+4,0,i)
                    sheet1.write(i+4,1,names[i])
                    sheet1.write(i+4,2,types[i])
                    sheet1.write(i+4,3,strings[i])
                    sheet1.write(i+4,4,defaults[i])
                    sheet1.write(i+4,5,nones[i])

wb.save("/home/shmoon/algorithm_parameter_parser/xls/algo_info.xls")
                
