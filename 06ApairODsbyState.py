import sys, os, arcpy
sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import timer_class as tc

zcta_file = arcpy.GetParameterAsText(0)
selected_states = arcpy.GetParameterAsText(1)
output_folder = arcpy.GetParameterAsText(2)
output_file = output_folder + "\\"

selected_states = selected_states.replace("\'", "").split(";")
for each_state in selected_states:
    output_file += each_state.replace(" ", "_") + "_"
    
output_file += "2010_zctas_pairs.csv"
arcpy.AddMessage(output_file)

t1 = tc.timer()

arcpy.AddMessage("Gathering all zctas from the selected state...")
zctas = {}
states = {}
sc = arcpy.SearchCursor(zcta_file)
row = sc.next()
while row:
    state = row.getValue("NAME10")
    if state in selected_states:
        zctas[row.getValue("ZCTA5CE10")] = [row.getValue("POINT_X"), row.getValue("POINT_Y")]
    if state not in states:
        states[state] = 1
    row = sc.next()

notfound = 0
for each_state in selected_states:
    if each_state not in states:
        arcpy.AddWarning("{0} state is not found in ZCTA file... Please contact rli24@nd.edu to update the tool!!!".format(each_state))
        notfound += 1
if notfound == 0:
    arcpy.AddMessage("All state(s) have been found!!")
    
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


