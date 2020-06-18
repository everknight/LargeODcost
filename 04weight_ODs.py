import arcpy, os, sys

inputfile = arcpy.GetParameterAsText(0)
org_id = arcpy.GetParameterAsText(1)
dest_id = arcpy.GetParameterAsText(2)
weight_id = arcpy.GetParameterAsText(3)
inputgdb = arcpy.GetParameterAsText(4)
name_field = arcpy.GetParameterAsText(5)
field_to_be_weight = arcpy.GetParameterAsText(6)


sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import timer_class as tc


totaln = int(str(arcpy.GetCount_management(inputfile)))

if totaln > 20000000:
	arcpy.AddError("The matrix file is too big...\nPlease split the file to less than 20M records and rerun this tool multiple times.")

arcpy.AddMessage("Reading weight file into memories......")
sc = arcpy.SearchCursor(inputfile)
weight_matrix = dict()
row = sc.next()
while row:
	key = str(row.getValue(org_id)) + ',' + str(row.getValue(dest_id))
	weight_matrix[key] = row.getValue(weight_id)
	row = sc.next()

arcpy.env.workspace = inputgdb
tbs = arcpy.ListTables()

i = 0
watch = tc.timer()

for each_tb in tbs:
	arcpy.AddField_management(each_tb, 'Cost_wt', "FLOAT")	
	uc = arcpy.UpdateCursor(each_tb)
	row = uc.next()
	while row:
		keyid = str(row.getValue(name_field)).replace(' - ', ',')
		if keyid in weight_matrix:
			wt = weight_matrix[keyid]
		else:
			wt = 1
		wt_cost_value = float(row.getValue(field_to_be_weight)) * wt
		row.setValue('Cost_wt', wt_cost_value)
		uc.updateRow(row)
		row = uc.next()
	i += 1
	watch.lap()
	togo = watch.format_time(watch.avg_sec*(len(tbs)-i))
	arcpy.AddMessage('Each batch take about {0}secs. {1} hours  {2} mins {3} secs to go...'.format(str(watch.avg_sec)[0:5], togo[0], togo[1], togo[2]))
