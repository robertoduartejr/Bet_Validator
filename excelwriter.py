import datetime

import xlsxwriter
import datetime
from datetime import datetime
import os

info = [['Heroes de Falcon', 'Rayo Zuliano', 'VENEZUELA: SEGUNDA DIVISÃO - DISPUTA DO TÍTULO - RODADA 4', False, 0, '0a0'],['Flamengo', 'São Paulo', 'BRASIL: COPA DO BRASIL - SEMIFINAIS', False, 23, '0a0 É Copa']]



def create_file(info):
#create file (workbook) and worksheet
    now = datetime.now()
    data = now.strftime("%d-%m-%Y-%H-%M-%S")
    file1 = r'C:\Users\rober\OneDrive\Documentos\Apostas'
    file2 = f"\Aposta-{data}.xlsx"
    file = file1+file2
    outWorkbook = xlsxwriter.Workbook(file)
    outSheet = outWorkbook.add_worksheet()

    #declare dataclasses
    names = ["name1","name2","name3"]
    values = [70,82,71]
    #write headers
    outSheet.write("A1","Time 1")
    outSheet.write("B1","Time 2")
    outSheet.write("C1","Liga")
    outSheet.write("D1","Goals")
    outSheet.write("E1","Flag")
    outSheet.write("F1","Criterio")

    #write data fo files
    print(len(info))
    for i in range(1,len(info)+1):
        outSheet.write(i,0,info[i-1][0]) #write time1
        outSheet.write(i, 1, info[i - 1][1])  # write time2
        outSheet.write(i, 2, info[i - 1][2]) #league
        outSheet.write(i, 3, info[i - 1][4]) #flag
        outSheet.write(i, 4, info[i - 1][3]) #goals
        outSheet.write(i, 5, info[i - 1][5]) #criterio
    outWorkbook.close()
    os.system(f"start {file}")

#create_file(info)