import sys, os, arcpy
#sys.path.append(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(r"C:\Users\lirui\OneDrive\Desktop\OD_git\LargeODcost")
import timer_class as tc

zcta_file = r"C:\Users\lirui\OneDrive\Desktop\ZCTA_PWC_SNAP.gdb\ZCTA_PWC_SNAP.gdb\ZCTA_Pop_weighted_Centroid_2010_Snap_state_cnty"
selected_states = ["Texas", "Louisiana"]
output_file = r"D:\US_Estimated_ODMatrix\tx_la_2010_zctas_pairs.csv"

t1 = tc.timer()

arcpy.AddMessage("Gathering all zctas from the selected state...")
zctas = {}
sc = arcpy.SearchCursor(zcta_file)
row = sc.next()
while row:
    state = row.getValue("NAME10")
    if state in selected_states:
        zctas[row.getValue("ZCTA5CE10")] = [row.getValue("POINT_X"), row.getValue("POINT_Y")]
    row = sc.next()
    
    
arcpy.AddMessage("Generating tables...")
f = open(output_file, "w")
f.write("OZCTA,DZCTA,olat,olong,dlat,dlong\n")
i = 0
for each_ozcta in zctas:
    for each_dzcta in zctas:
        if i%10000 == 0:
            arcpy.AddMessage("Printing {0} records...".format(i))
            print("Printing {0} records...".format(i))
        if each_ozcta != each_dzcta:
            f.write( "{0},{1},{2},{3},{4},{5}\n".format(each_ozcta, each_dzcta, zctas[each_ozcta][1], zctas[each_ozcta][0], zctas[each_dzcta][1], zctas[each_dzcta][0]))
            i += 1
f.close()
t1.lap()
print(t1.format_time(t1.total_sec))
