import os, sys, ast
sys.path.append(r"C:\Users\lirui\OneDrive\Desktop\OD_git\LargeODcost")
import timer_class as timer

#input_csv = r"D:\US_Estimated_ODMatrix\US_Estimated_ODMatrix\US_ODMatrix_3_3-6hours_Division\NA_OD_3hours.csv"
input_csv = r"D:\US_Estimated_ODMatrix\US_Estimated_ODMatrix\US_ODMatrix_3_3-6hours_Division\NA_OD_3-6hours.csv"
#output_folder = r"D:\US_Estimated_ODMatrix\US_OD_data_plain\hour03"
output_folder = r"D:\US_Estimated_ODMatrix\US_OD_data_plain\hour36"
lvl = 2

f = open(input_csv, "r")
field_name = f.readline()[0:-1].split(",")

on = 0
ot = 0

t = timer.timer()
row = f.readline()
while row:
    row_content = row[0:-1].split(",")
    ozcta = row_content[field_name.index("OZCTA")]
    dzcta = row_content[field_name.index("DZCTA")]
    if ozcta == dzcta:
        ot += 1
    else:
        on += 1
    if on % 10000 == 0 and on > 0:
        print(on)
    row = f.readline()

f.close()    
t.lap()
print(t.avg_sec)

t1 = timer.timer()
myn = 0
empty_file = []
# folders = os.listdir(output_folder)
# for folder in folders:
    # print(folder)
    # files = os.listdir(output_folder + "\\" + folder)
    # for file in files:
        # f = open(output_folder + "\\" + folder + "\\" + file, "r")
        # fcontent = f.read()
        # if fcontent == "":
            # empty_file.append(folder + file)
        # else:
            # temp = ast.literal_eval(fcontent)
            # myn += len(temp)
        # f.close()

if lvl == 1:   
    folders = os.listdir(output_folder)
    for folder in folders:
        print(folder)
        files = os.listdir(output_folder + "\\" + folder)
        for file in files:
            f = open(output_folder + "\\" + folder + "\\" + file, "r")
            fcontent = f.readline()
            if fcontent == "":
                empty_file.append(folder + file)
            else:
                while fcontent:
                    myn += 1
                    fcontent = f.readline() 
            f.close()
else:
    folders = os.listdir(output_folder)
    for folder in folders:
        print(folder)
        subfolders = os.listdir(output_folder + "\\" + folder)
        for subfolder in subfolders:
            files = os.listdir(output_folder + "\\" + folder + "\\" + subfolder)
            for file in files:
                f = open(output_folder + "\\" + folder + "\\" + subfolder + "\\" + file, "r")
                fcontent = f.readline()
                if fcontent == "":
                    empty_file.append(folder + file)
                else:
                    while fcontent:
                        myn += 1
                        fcontent = f.readline() 
                f.close()

t1.lap()

print("{0} - {1}".format(on,myn))
print("{0} - {1}".format(t.avg_sec, t1.avg_sec))
