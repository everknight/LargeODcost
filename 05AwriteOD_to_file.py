import os, sys, arcpy, math

OD_id = arcpy.GetParameterAsText(0) #It's usually 'Name'

ODlv1 = arcpy.GetParameterAsText(1)
ODlv2 = arcpy.GetParameterAsText(2)

outputfolder = arcpy.GetParameterAsText(3) 

zcta_file = arcpy.GetParameterAsText(4) 
zcta_field = arcpy.GetParameterAsText(5) 
x_field = arcpy.GetParameterAsText(6) 
y_field = arcpy.GetParameterAsText(7) 
   

ODlv1_time_name = arcpy.GetParameterAsText(8)  # "Total_TravelTime"
ODlv1_mile_name = arcpy.GetParameterAsText(9)  #'Total_Miles'

ODlv2_time_name = arcpy.GetParameterAsText(10)  #"Total_Time"
ODlv2_mile_name = arcpy.GetParameterAsText(11)  #'Total_Miles'

speed_Geodesic = arcpy.GetParameterAsText(12) 
if speed_Geodesic == '#' or speed_Geodesic == '':
    speed_Geodesic = 50
else:
    speed_Geodesic = int(speed_Geodesic) 

# Handles lv1 returns (within 3 hrs drive, snap to none pedestrain road)
arcpy.env.workspace = ODlv1
all_tbs = arcpy.ListTables()
for each_tb in all_tbs:
    print (each_tb)
    sc = arcpy.SearchCursor(each_tb)
    row = sc.next()
    O_id = ''
    zcta_dict = dict()
    while row:
        od_id_row = row.getValue(OD_id)
        cO_id = od_id_row.split(' - ')[0]
        D_id = od_id_row.split(' - ')[1]
        if cO_id != O_id:
            if len(zcta_dict) != 0:
                #print(outputfolder+'\\'+O_id[0:3]+'\\'+O_id+'.txt')
                f = open(outputfolder+'\\'+O_id[0:3]+'\\'+O_id+'.txt', 'w')
                f.write(str(zcta_dict))
                f.close()
                #break
            O_id = cO_id
            if not os.path.exists(outputfolder+'\\'+O_id[0:3]):
                os.makedirs(outputfolder+'\\'+O_id[0:3])
            if os.path.exists(outputfolder+'\\'+O_id[0:3]+'\\'+O_id+'.txt'):
                f = open(outputfolder+'\\'+O_id[0:3]+'\\'+O_id+'.txt', 'r')
                zcta_dict = eval(f.read())
                f.close()
            else:
                zcta_dict = dict()
        else:
            if D_id != O_id and (D_id not in zcta_dict):
                #zcta_dict[D_id] = [max(float('{0:.2f}'.format(row.getValue('Total_TravelTime'))),180), float('{0:.2f}'.format(row.getValue('Total_Miles'))), 2]  for formal ZCTAs
                zcta_dict[D_id] = [float('{0:.2f}'.format(row.getValue(ODlv1_time_name))), float('{0:.2f}'.format(row.getValue(ODlv1_mile_name))), 1]
        row = sc.next()
    

# Handles lv2 returns (3-6 hrs drive, snap to highway that within 5 miles) Part I
arcpy.env.workspace = ODlv2
all_tbs = arcpy.ListTables()
for each_tb in all_tbs:
    print (each_tb)
    sc = arcpy.SearchCursor(each_tb)
    row = sc.next()
    O_id = ''
    zcta_dict = dict()
    while row:
        od_id_row = row.getValue(OD_id)
        cO_id = od_id_row.split(' - ')[0]
        D_id = od_id_row.split(' - ')[1]
        if cO_id != O_id:
            if len(zcta_dict) != 0:
                #print(outputfolder+'\\'+O_id[0:3]+'\\'+O_id+'.txt')
                f = open(outputfolder+'\\'+O_id[0:3]+'\\'+O_id+'.txt', 'w')
                f.write(str(zcta_dict))
                f.close()
                #break
            O_id = cO_id
            if not os.path.exists(outputfolder+'\\'+O_id[0:3]):
                os.makedirs(outputfolder+'\\'+O_id[0:3])
            if os.path.exists(outputfolder+'\\'+O_id[0:3]+'\\'+O_id+'.txt'):
                f = open(outputfolder+'\\'+O_id[0:3]+'\\'+O_id+'.txt', 'r')
                zcta_dict = eval(f.read())
                f.close()
            else:
                zcta_dict = dict()
        else:
            if D_id != O_id and (D_id not in zcta_dict):
                #zcta_dict[D_id] = [max(float('{0:.2f}'.format(row.getValue('Total_TravelTime'))),180), float('{0:.2f}'.format(row.getValue('Total_Miles'))), 2]  for formal ZCTAs
                zcta_dict[D_id] = [float('{0:.2f}'.format(row.getValue(ODlv2_time_name))), float('{0:.2f}'.format(row.getValue(ODlv2_mile_name))), 2]
        row = sc.next()
        
        


# Handles lv3 returns (Geodesic distance and time based on 50mph)            
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
    
sc = arcpy.SearchCursor(zcta_file)
row = sc.next()
zcta_coord_dict = dict()
while row:
    zcta_coord_dict[row.getValue(zcta_field)] = [row.getValue(x_field), row.getValue(y_field)]
    row = sc.next()

for each_org_key in zcta_coord_dict:
    print(outputfolder+'\\'+each_org_key[0:3]+'\\'+each_org_key+'.txt')
    if not os.path.exists(outputfolder+'\\'+each_org_key[0:3]):
        os.makedirs(outputfolder+'\\'+each_org_key[0:3])
    if os.path.exists(outputfolder+'\\'+each_org_key[0:3]+'\\'+each_org_key+'.txt'):
        f = open(outputfolder+'\\'+each_org_key[0:3]+'\\'+each_org_key+'.txt', 'r')
        zcta_dict = eval(f.read())
        f.close()
    else:
        zcta_dict = dict()
    for each_dest_key in zcta_coord_dict:
        if each_dest_key not in zcta_dict and each_dest_key != each_org_key:
            dist = cal_geodesic_dist(zcta_coord_dict[each_org_key][0], zcta_coord_dict[each_org_key][1], zcta_coord_dict[each_dest_key][0], zcta_coord_dict[each_dest_key][1])
            #time = max(dist/5*6, 300)
            time = dist/float(speed_Geodesic)*60
            zcta_dict[each_dest_key] = [float('{0:.2f}'.format(time)), float('{0:.2f}'.format(dist)), 3]
    f = open(outputfolder+'\\'+each_org_key[0:3]+'\\'+each_org_key+'.txt', 'w')
    f.write(str(zcta_dict))
    f.close()


# Check if file created correctly
def FileSearcher(folder, suffix): #suffix should not include '.'
    allfile = os.listdir(folder)
    return_value = []
    if(len(allfile) > 0):
        i = 0
        while(i < len(allfile)):
            temp = allfile[i].split('.')
            if (len(temp) > 1):
                act_suffix = temp[len(temp)-1]
            else:
                act_suffix = ''
            if(act_suffix == suffix):
                wholepath = folder + "\\" + allfile[i]
                return_value.append(wholepath)
            i += 1
    return return_value

all_out_folders = FileSearcher(outputfolder, '')    
for each_out_folder in all_out_folders:
    all_text = FileSearcher(each_out_folder, 'txt')
    for each_text in all_text:
        f = open(each_text, 'r')
        test_dict = eval(f.read())
        f.close()
        print ('{0}:{1}'.format(os.path.split(each_text)[1], len(test_dict)))
    


    
        
        
