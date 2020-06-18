import arcpy, os

#od_input = r'C:\Users\rl53\Desktop\Active_provider_2014\OtherPCP_OD_14'
#output = r'C:\Users\rl53\Desktop\Active_provider_2014\OD_2014Active.gdb\OD_cost_OTHERPCP_2014'
od_input = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)
org_name = arcpy.GetParameterAsText(2)
if org_name == '#' or org_name == '':
	org_name = 'GEOID'
dest_name = arcpy.GetParameterAsText(3)
if dest_name == '#' or dest_name == '':
	dest_name = 'destID'
IDfield_length = arcpy.GetParameterAsText(4)
if IDfield_length == '#' or IDfield_length == '':
	IDfield_length = 20
else: 
	IDfield_length = int(IDfield_length)
	


arcpy.env.workspace = od_input	
tables = arcpy.ListTables()
arcpy.AddMessage('Merging... This process may take a few hours...')
outfile = arcpy.Merge_management(tables, output)

arcpy.AddMessage('Adding {0} field...'.format(org_name))
arcpy.AddField_management(outfile, org_name, "TEXT", field_length = IDfield_length)

arcpy.AddMessage('Adding {0} field...'.format(dest_name))
arcpy.AddField_management(outfile, dest_name, "TEXT", field_length = IDfield_length)

arcpy.AddMessage('Calculating {0} field...'.format(org_name))
arcpy.CalculateField_management(outfile, org_name, '!Name!.split(\' - \')[0]', "PYTHON")

arcpy.AddMessage('Calculating {0} field...'.format(dest_name))
arcpy.CalculateField_management(outfile, dest_name, '!Name!.split(\' - \')[1]', "PYTHON")