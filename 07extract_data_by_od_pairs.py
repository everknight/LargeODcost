import arcpy
import sys, os, math
#sys.path.append(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(r"C:\Users\lirui\OneDrive\Desktop\OD_git\LargeODcost")
import timer_class as tc

input_csv = r"D:\US_Estimated_ODMatrix\tx_la_2010_zctas_pairs.csv"
output_csv = r"D:\US_Estimated_ODMatrix\tx_la_2010_zctas_OD_extracts.csv"
db1 = r"D:\US_Estimated_ODMatrix\US_OD_data_plain\hour03"
db2 = r"D:\US_Estimated_ODMatrix\US_OD_data_plain\hour36"
lvl3_at = 33.91
lvl3_bt = 0.88
lvl3_ad = 20.86
lvl3_bd = 1.18
lvl3_speed = 50

def cal_geodesic_dist (x1, y1, x2, y2):
    r = 3959 #miles 
    p1 = math.radians(y1)
    p2 = math.radians(y2)
    dp = math.radians(y1-y2)
    dl = math.radians(x1-x2)
    a = math.sin(dp/2) ** 2 + math.cos(p1)*math.cos(p2)*(math.sin(dl/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = r * c
    return d

class data_station:
    def __init__ (self, nlimit = 100000):
        self.n = 0
        self.data = {}
        self.nlimit = nlimit
    
    def push_data(self, key, key1, d):
        self.n += 1
        if key in self.data:
            if key1 in self.data[key]:
                arcpy.AddWarning("Repetitive key pair found: {0} - {1}".format(key, key1))
            self.data[key][key1] = d
        else: 
            self.data[key] = {}
            self.data[key][key1] = d
    
    def reset(self):
        self.n = 0
        self.data = {}
        
def get_data_from_lv1(ozcta, odict, db1, output_csv):
    target_path = db1 + "\\" + ozcta[0:3] + "\\" + ozcta[3:] + ".data"
    if os.path.exists(target_path):
        f = open(target_path, "r")
        outio = open(output_csv,"a")
        row = f.readline()
        while row:
            row_content = row.replace("\n","").split(",")
            if row_content[0] in odict:
                outio.write("{0},{1},{2},{3},1\n".format(ozcta, row_content[0], row_content[1], row_content[2]))
                del odict[row_content[0]]
            row = f.readline()
        f.close()
        outio.close()
    return odict
    
def get_data_from_lv2(ozcta, odict, db2, output_csv):
    base_path = db2 + "\\" + ozcta[0:3] + "\\" + ozcta[3:]
    dzcta2_index = {}
    for each_dzcta in odict:
        dzcta2 = each_dzcta[0:2]
        if dzcta2 in dzcta2_index:
            dzcta2_index[dzcta2][each_dzcta[2:]] = True
        else:
            dzcta2_index[dzcta2] = {}
            dzcta2_index[dzcta2][each_dzcta[2:]] = True
    for each_dzcta2 in dzcta2_index:
        target_path = base_path + "\\" + each_dzcta2 + ".data"
        if os.path.exists(target_path):
            f = open(target_path, "r")
            outio = open(output_csv,"a")
            row = f.readline()
            while row:
                row_content = row.replace("\n","").split(",")
                temp_dzcta = each_dzcta2+row_content[0]
                if temp_dzcta in odict:
                    outio.write("{0},{1},{2},{3},2\n".format(ozcta, temp_dzcta, row_content[1], row_content[2]))
                    del odict[temp_dzcta]
                row = f.readline()
            f.close()
            outio.close()
    return odict
    
def cal_data_lv3(ozcta, odict, lvl3_at, lvl3_bt, lvl3_ad, lvl3_bd, output_csv, speed):
    for each_dzcta in odict:
        dist = cal_geodesic_dist (float(odict[each_dzcta][1]), float(odict[each_dzcta][0]), float(odict[each_dzcta][3]), float(odict[each_dzcta][2]))
        adj_dist = lvl3_bd*dist + lvl3_ad
        adj_time = lvl3_bt*dist/speed + lvl3_at
        outio = open(output_csv,"a")
        outio.write("{0},{1},{2},{3},3\n".format(ozcta, each_dzcta, adj_time, adj_dist))
        outio.close()
        
        
def fetch_info_and_write(rs, db1, db2, output_csv, lvl3_at, lvl3_bt, lvl3_ad, lvl3_bd, lvl3_speed):
    for each_ozcta in rs.data:
        lv11_leftover = get_data_from_lv1(each_ozcta, rs.data[each_ozcta], db1, output_csv)
        lvl2_leftover = get_data_from_lv2(each_ozcta, lv11_leftover, db1, output_csv)
        cal_data_lv3(each_ozcta, lvl2_leftover, lvl3_a, lvl3_b, output_csv, lvl3_speed)
    rs.reset()


t1 = tc.timer()
indata = open(input_csv, "r")
outdata = open(output_csv, "w")
outdata.write("ozcta, dzcta, minutes, miles, lvl\n")
outdata.close()

rs = data_station()

header = indata.readline().replace("\n", "").split(",")
iozcta = header.index("OZCTA")
idzcta = header.index("DZCTA")
i = 0
row = indata.readline()
while row:
    if i % 10000 == 0:
        #arcpy.AddMessage("Retrieving {0} records...".format(i))
        print("Retrieving {0} records...".format(i))
    row_content = row.replace("\n", "").split(",")
    temp_ozcta = row_content[iozcta]
    temp_dzcta = row_content[idzcta]
    rs.push_data(temp_ozcta, temp_dzcta, row_content[2:])
    if rs.n >= rs.nlimit:
        fetch_info_and_write(rs, db1, db2, output_csv, lvl3_at, lvl3_bt, lvl3_ad, lvl3_bd, lvl3_speed)
    row = indata.readline()
    i += 1

indata.close()
outdata.close()
t1.lap()
print(t1.format_time(t1.total_sec))



