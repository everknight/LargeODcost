import os, arcpy

# input = r"C:\Users\rl53\Desktop\test\OD_test\test1\temp.gdb\zip_usa_prj_albert"
# outputgdb = r"C:\Users\rl53\Desktop\test\OD_test\test1\zip_slice.gdb"
# ID = 'ZIP_CODE'
# step = 200

input = arcpy.GetParameterAsText(0)
outputgdb = arcpy.GetParameterAsText(1)
ID = arcpy.GetParameterAsText(2)
step = arcpy.GetParameterAsText(3)
if step == '#' or step == '':
	step = 200
else:
	step = int(step)

sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import timer_class as tc

i = 1
sc = arcpy.SearchCursor(input)

select_list = []
totaln = float(str(arcpy.GetCount_management(input)))

arcpy.SetProgressor("step", "Reading files...")
row = sc.next()
while row:
	select_list.append(str(row.getValue(ID)))
	if i % 10000 == 0:
		arcpy.SetProgressorPosition(int(i/totaln*100))
	i += 1
	row = sc.next()

select_list.sort()
arcpy.ResetProgressor()
	
i = 0
watch = tc.timer()	
arcpy.SetProgressor("step", "Splitting files in to smaller trunks...")	
while i < totaln:
	criteria = str(select_list[i:i+step])
	arcpy.FeatureClassToFeatureClass_conversion(input, outputgdb, os.path.splitext(os.path.split(input)[1])[0]+"_"+str(i), "{0} IN ({1})".format(ID, str(criteria[1:len(criteria)-1])))
	progress = int(i/totaln*100)
	watch.lap()
	arcpy.SetProgressorPosition (progress)
	
	if i % (step*5) == 0 and i > 0:
		togo = watch.format_time(watch.avg_sec*(int((totaln-i)/step)+1))
		arcpy.AddMessage('Each batch take about {0}secs. {1} hours  {2} mins {3} secs to go...'.format(str(watch.avg_sec)[0:5], togo[0], togo[1], togo[2]))
	
	i += step