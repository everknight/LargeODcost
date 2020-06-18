import os, arcpy

#input = r"C:\Users\rl53\Desktop\zip_usa\zip_usa.gdb\zip_usa"
#outputfolder = r"C:\Users\rl53\Desktop\test\OD_test\test1"
#snapStreetfile = r"C:\Users\rl53\Desktop\test\OD_test\streets.gdb\drivable_st"

input = arcpy.GetParameterAsText(0)
outputfolder = arcpy.GetParameterAsText(1)
snapStreetfile = arcpy.GetParameterAsText(2)
snapDist = arcpy.GetParameterAsText(3)
if snapDist == '#' or snapDist == '':
	snapDist = "500 Meters"

arcpy.AddMessage(snapDist)
	
tempgdb = outputfolder + '\\temp.gdb'
if not os.path.exists(tempgdb):
	arcpy.AddMessage("Creating temp geodatabase...")
	arcpy.CreateFileGDB_management(outputfolder, 'temp.gdb')

ref_input = arcpy.Describe(input).spatialReference
ref_street = arcpy.Describe(snapStreetfile).spatialReference	
if ref_street.name <> ref_input.name:
	input_copy = arcpy.Project_management(input, tempgdb+'\\'+os.path.split(input)[1]+'_prj', snapStreetfile)
else:
	input_copy = arcpy.FeatureClassToFeatureClass_conversion(input, tempgdb, os.path.split(input)[1]+'_copy')
	
arcpy.AddMessage("Start to Snap points to Road... The process may take up to a few days...")
arcpy.Snap_edit(input_copy,[[snapStreetfile, "EDGE", snapDist]])	
