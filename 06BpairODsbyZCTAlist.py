import sys, os, arcpy
sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import timer_class as tc

zcta_file = arcpy.GetParameterAsText(0)
input_zctas = arcpy.GetParameterAsText(1)
zip_field = arcpy.GetParameterAsText(2)
output_folder = arcpy.GetParameterAsText(3)

output_file = output_folder + "\\user_selected_2010_zctas_pairs.csv"
    
arcpy.AddMessage(output_file)

t1 = tc.timer()

arcpy.AddMessage("Reading zipcodes from the input list...")
selected_zctas = {}
sc = arcpy.SearchCursor(input_zctas)
row = sc.next()
while row:
    zcta = row.getValue(zip_field)
    if zcta not in selected_zctas:
        selected_zctas[zcta] = False
    else:
        arcpy.AddWarning("Zip code {0} in the list found one duplicate.".format(zcta))
    row = sc.next()

arcpy.AddMessage("Gathering info for zctas list...")
zctas = {}
sc = arcpy.SearchCursor(zcta_file)
row = sc.next()
while row:
    zip = row.getValue("ZCTA5CE10")
    if zip in selected_zctas:
        if zip not in zctas:
            zctas[zip] = [row.getValue("POINT_X"), row.getValue("POINT_Y")]
        else: 
            arcpy.AddWarning("{0} zcta duplicated!!!".format(zip))
    row = sc.next()
arcpy.AddMessage("{0} zctas information found in the zcta shape...".format(len(zctas)))

notfound = 0
for each_zcta in selected_zctas:
    if each_zcta not in zctas:
        arcpy.AddWarning("{0} is not found in ZCTA file... Please contact rli24@nd.edu to update the tool!!!".format(each_zcta))
        notfound += 1
if notfound == 0:
    arcpy.AddMessage("All zcta(s) have been found!!")
    
arcpy.AddMessage("Generating tables...")
f = open(output_file, "w")
f.write("OZCTA,DZCTA,olat,olong,dlat,dlong\n")
i = 0
for each_ozcta in zctas:
    for each_dzcta in zctas:
        if i%10000 == 0:
            arcpy.AddMessage("Processing {0} records...".format(i))
            #print("Printing {0} records...".format(i))
        if each_ozcta != each_dzcta:
            f.write( "{0},{1},{2},{3},{4},{5}\n".format(each_ozcta, each_dzcta, zctas[each_ozcta][1], zctas[each_ozcta][0], zctas[each_dzcta][1], zctas[each_dzcta][0]))
            i += 1
f.close()
t1.lap()
time_used = t1.format_time(t1.total_sec)
print(time_used)
arcpy.AddMessage("Process finished in {0} hours {1} minutes {2} seconds.".format(time_used[0], time_used[1], time_used[2]))


