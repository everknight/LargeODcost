import os, sys, ast
sys.path.append(r"C:\Users\lirui\OneDrive\Desktop\OD_git\LargeODcost")
import timer_class as timer

# Input file path
#input_csv = r"D:\US_Estimated_ODMatrix\US_Estimated_ODMatrix\US_ODMatrix_3_3-6hours_Division\NA_OD_3hours.csv"
#output_folder = r"D:\US_Estimated_ODMatrix\US_OD_data\hour03"
#lvl = 1
input_csv = r"D:\US_Estimated_ODMatrix\US_Estimated_ODMatrix\US_ODMatrix_3_3-6hours_Division\NA_OD_3-6hours.csv"
output_folder = r"D:\US_Estimated_ODMatrix\US_OD_data\hour36"
lvl = 2

def init_io (output_folder, ozcta, lvl, dzcta = ""):
    previous_file_content = ""
    if lvl == 1:
        if not os.path.exists(output_folder + "\\" + ozcta[0:3]):
            os.mkdir(output_folder + "\\" + ozcta[0:3])
        if os.path.exists(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:] + ".data"):
            temp_input = open(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:] + ".data", "r")
            previous_file_content = temp_input.read()
            temp_input.close()
    else:
        if not os.path.exists(output_folder + "\\" + ozcta[0:3]):
            os.mkdir(output_folder + "\\" + ozcta[0:3])
        if not os.path.exists(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:]):
            os.mkdir(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:])
        if os.path.exists(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:] + "\\" + dzcta[0:2] + ".data"):
            temp_input = open(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:] + "\\" + dzcta[0:2] + ".data", "r")
            previous_file_content = temp_input.read()
            temp_input.close()
    return previous_file_content
    
def write_current_io (current_io, lvl):
    print("Writing to file!!!")
    if lvl == 1:
        for ozcta in current_io:
            if not os.path.exists(output_folder + "\\" + ozcta[0:3]):
                os.mkdir(output_folder + "\\" + ozcta[0:3])
            fout = open(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:] + ".data", "w")
            fout.write(str(current_io[ozcta]))
            fout.close()
    else:
        for ozcta in current_io:
            if not os.path.exists(output_folder + "\\" + ozcta[0:3]):
                os.mkdir(output_folder + "\\" + ozcta[0:3])
            if not os.path.exists(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:]):
                os.mkdir(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:])
            for dzcta2 in current_io[ozcta]:
                fout = open(output_folder + "\\" + ozcta[0:3] + "\\" + ozcta[3:] + "\\" + dzcta2 + ".data", "w")
                fout.write(str(current_io[ozcta][dzcta2]))
                fout.close()


f = open(input_csv, "r")
field_name = f.readline()[0:-1].split(",")

current_io = {}
previous_ozcta = ""
if lvl == 2:
    previous_dzcta2 = ""
out_io = ""
i = 0

t = timer.timer()
row = f.readline()
while row:
    row_content = row[0:-1].split(",")
    ozcta = row_content[field_name.index("OZCTA")]
    dzcta = row_content[field_name.index("DZCTA")]
    if ozcta == dzcta:
        row = f.readline()
        continue  
    if lvl == 1:            
        if previous_ozcta != ozcta:
            previous_ozcta = ozcta
            if sys.getsizeof(current_io) > 300*1000:
                write_current_io(current_io, lvl)
                del current_io
                current_io = {}
            if ozcta not in current_io:
                prev_cont = init_io(output_folder, ozcta, lvl)
                if prev_cont != "":
                    current_io[ozcta] = ast.literal_eval(prev_cont)
                else:
                    current_io[ozcta] = {}    
        if dzcta in current_io[ozcta]:
            print("{0} already in {1} dictionary!!!".format(dzcta, ozcta))
        current_io[ozcta][dzcta] = [row_content[field_name.index("EstTime")], row_content[field_name.index("EstDist")]]  # Time, Distance   
    else: 
        if previous_ozcta != ozcta:
            previous_ozcta = ozcta
            if sys.getsizeof(current_io) > 300*1000:
                write_current_io(current_io, lvl)
                del current_io
                current_io = {}
            if ozcta not in current_io:
                prev_cont = init_io(output_folder, ozcta, lvl, dzcta)
                current_io[ozcta] = {}
                if prev_cont != "":
                    current_io[ozcta][dzcta[0:2]] = ast.literal_eval(prev_cont)
                else:
                    current_io[ozcta][dzcta[0:2]] = {}    
            else:
                if dzcta[0:2] not in current_io[ozcta]:
                    prev_cont = init_io(output_folder, ozcta, lvl, dzcta)
                    if prev_cont != "":
                        current_io[ozcta][dzcta[0:2]] = ast.literal_eval(prev_cont)
                    else:
                        current_io[ozcta][dzcta[0:2]] = {}
        if dzcta in current_io[ozcta]:
            print("{0} already in {1} dictionary!!!".format(dzcta, ozcta))
        current_io[ozcta][dzcta[0:2]][dzcta[2:]] = [row_content[field_name.index("EstTime")], row_content[field_name.index("EstDist")]]  # Time, Distance   
        
    i += 1
    if i % 10000 == 0:
        t.lap()
        print("{0} : avg time - {1}".format(i,t.avg_sec))
    row = f.readline()


if current_io != {}:
    write_current_io (current_io, lvl)
    del current_io
