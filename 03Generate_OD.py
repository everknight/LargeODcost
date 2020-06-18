import os, arcpy, datetime, ast, sys
from multiprocessing import Process

arcpy.env.overwriteOutput = True

def add_zero (num, digit):
	string = str(num)
	while len(string) < digit:
		string = '0' + string
	return string
	
def file_search (folder, ext):
	result = []
	all_file = os.listdir(folder)
	for file in all_file:
		if(file.split(".")[-1].upper() == ext.upper()):
			result.append(folder + '\\' + file)
	return result

def set_up_OD_matrix(provider_file, u_shp, na_layer, smp, tempfolder, desID, cost, accost, restrict, hier, max_time_limit):
	temp_layer = arcpy.MakeFeatureLayer_management(provider_file, "Temp_Provider")
	selected_layer = arcpy.SelectLayerByLocation_management("Temp_Provider", "WITHIN_A_DISTANCE", u_shp, str(max_time_limit) + " Miles", "NEW_SELECTION")
	temp_output = arcpy.FeatureClassToFeatureClass_conversion(selected_layer, tempfolder, "temp.shp")
	exe_layer = arcpy.na.MakeODCostMatrixLayer(smp, na_layer, cost, max_time_limit, "", accost, "ALLOW_UTURNS", restrict, hier,"","NO_LINES")
	arcpy.na.AddLocations(exe_layer, "Destinations", temp_output, "Name "+desID+" #", "5000 meter")			
	return exe_layer
	
def str0(input, length):
	temp = str(input)
	while len(temp) < length:
		temp = '0' + temp
	return temp
	
def get_formatted_time():
	time_now = datetime.datetime.now()
	result = str(time_now.year) + "." + str0(time_now.month,2) + "." + str0(time_now.day,2) + " " + str0(time_now.hour,2) + ":" + str0(time_now.minute,2) + "." + str0(time_now.second,2)
	return result
	
	
def get_ODCost(provider_file, u_shp, n, na_layer, ODfolder, smp, tempfolder, log_file, orgID, desID, cost, accost, restrict, hier, max_time_limit):
	arcpy.CheckOutExtension("Network")
	f=open(log_file, 'a')
	try:
		ODcostout = ODfolder + '\\OD_cost_out.gdb'
		if not os.path.exists(ODcostout):
			arcpy.CreateFileGDB_management(ODfolder, 'OD_cost_out.gdb')
		f.write(get_formatted_time() + " Start working on " + os.path.split(u_shp)[1] + "...\n")
		f.write(get_formatted_time() + " Setting up OD cost matrix...\n")
		exe_layer = set_up_OD_matrix(provider_file, u_shp, na_layer, smp, tempfolder, desID, cost, accost, restrict, hier, max_time_limit)
		f.write(get_formatted_time() + " Adding Locations...\n")
		arcpy.na.AddLocations(exe_layer, "Origins", u_shp, "Name " + orgID + " #", "5000 meter")
		f.write(get_formatted_time() + " Solving...\n")
		arcpy.na.Solve(exe_layer)
		f.write(get_formatted_time() + " Exporting...\n")
		N = int(str(arcpy.GetCount_management(r"OD Cost Matrix\Lines")))
		if N:
			arcpy.TableToTable_conversion(r"OD Cost Matrix\Lines", ODcostout , "OD_cost_out" + str(n))
		f.write("Successful with no Error!!!\n")
		f.close()
	except Exception as e:
		f.write(get_formatted_time() + " ")
		f.write(e.message)
		f.write("\n")
		f.close()
		
		ef = open(ODfolder + '\\error.txt', 'a')
		ef.write("Error when working on file: " + u_shp + '\n')
		ef.write(get_formatted_time() + " ")
		ef.write(e.message)
		ef.write("\n\n")
		ef.close()
		
		if not os.path.exists(ODfolder + '\\error_shp.gdb'):
			arcpy.CreateFileGDB_management(ODfolder, 'error_shp.gdb')
		arcpy.FeatureClassToFeatureClass_conversion(u_shp, ODfolder + '\\error_shp.gdb' , os.path.split(u_shp)[1])
		
def remove_leading_space(string):
	while string[0] == ' ' and string != '':
		string  = string[1:]
	return string
		
		

if __name__ == '__main__':
	try:
		##### ZCTA or other geoid slice folder usually don't need to change
		#inputfolder = r"C:\Users\rl53\Desktop\Chiro_Active\ZCTS_slice" #Testing Default
		inputfolder = arcpy.GetParameterAsText(0)


		##### Table ID Need to change!!!!
		#orgID = 'ZCTA5CE10'  #Testing Default
		#desID = 'NPI'  #Testing Default
		orgID = arcpy.GetParameterAsText(1)
		desID = arcpy.GetParameterAsText(3)

		##### Provider file Need to specify every time
		#provider_file = r"R:\Projects\Davis_NIH\NPPES_2010_2015\Active_2014_geocoded.gdb\OTHERPCP_14_active_match"  #Testing Default
		provider_file = arcpy.GetParameterAsText(2)
				
		##### Outpt folder Need to change every time
		#ODfolder = r"C:\Users\rl53\Desktop\Active_provider_2014\OTHERPCP_OD_14"
		ODfolder = arcpy.GetParameterAsText(4)

		max_time_limit = int(arcpy.GetParameterAsText(5))
		if max_time_limit == '#' or max_time_limit =='':
			max_time_limit = 60

		NTsetting = os.path.split(os.path.realpath(__file__))[0]+'\\Default_NetworkData_Setting.txt'
		ntf = open(NTsetting, 'r')
		default_nt = ast.literal_eval(remove_leading_space(ntf.readline().split('=')[1].replace('\n', '')))
		default_cost = ast.literal_eval(remove_leading_space(ntf.readline().split('=')[1].replace('\n', '')))
		default_accost = ast.literal_eval(remove_leading_space(ntf.readline().split('=')[1].replace('\n', '')))
		default_restrict = ast.literal_eval(remove_leading_space(ntf.readline().split('=')[1].replace('\n', '')))
		default_hierarchy = ast.literal_eval(remove_leading_space(ntf.readline().split('=')[1].replace('\n', '')))
		ntf.close()


		##### street map premium path usually don't need to change
		#smp = r"C:\Users\rl53\Desktop\StreetMapPremium2017_Release1\StreetMap_Data\NorthAmerica.gdb\Routing\Routing_ND"  
		smp = arcpy.GetParameterAsText(6)
		if smp == '#' or smp =='':
			smp = default_nt

		#cost = "TravelTime"
		cost = arcpy.GetParameterAsText(7)
		if cost == '#' or cost =='':
			cost = default_cost

		#accost = ["TravelTime", "Miles"]
		accost = arcpy.GetParameterAsText(8).split(';')
		if accost ==['#'] or accost == '' or accost == ['']:
			accost = default_accost

		#restrict = ["Driving an Automobile"]
		restrict = arcpy.GetParameterAsText(9).split(';')
		if restrict == ['#'] or restrict == '' or restrict == ['']:
			restrict = default_restrict

		#hierarchy='TRUE'
		hierarchy = arcpy.GetParameterAsText(10).upper()
		if hierarchy == '#' or hierarchy == '':
			hierarchy = default_hierarchy
		if hierarchy=='TRUE':
			hier = "USE_HIERARCHY"
		else:
			hier = "NO_HIERARCHY"
			
		i = 0	
		while i < len(restrict):
			restrict[i] = restrict[i].replace('\'', '').replace('\"','')
			i += 1
			
		i = 0	
		while i < len(accost):
			accost[i] = accost[i].replace('\'', '').replace('\"','')
			i += 1


		##### Temp folder and log file
		tempfolder = ODfolder + "\\temp"
		log_file = ODfolder + "\\log.txt"

		na_layer = "OD Cost Matrix"

		if not os.path.exists(tempfolder):
			os.mkdir(tempfolder)

		sys.path.append(os.path.split(os.path.realpath(__file__))[0])
		import timer_class as tc	
			
		arcpy.env.workspace = inputfolder
		allshps = arcpy.ListFeatureClasses()
		usable_shp = []
		for each_shp in allshps:
			usable_shp.append(inputfolder + '\\' + each_shp)

		arcpy.SetProgressor("step", "Generating OD cost matrix...")

		totaln = len(usable_shp)
		watch=tc.timer()
		n = 0
		while n < len(usable_shp):
			u_shp = usable_shp[n]
			arcpy.AddMessage("Working on "+u_shp+"...")
			progress = int(float(n)/totaln * 100)
			arcpy.SetProgressorPosition (progress)
			
			#get_ODCost(provider_file, u_shp, n, na_layer, ODfolder, smp, tempfolder, log_file, orgID, desID, cost, accost, restrict, hier)
			p = Process(target = get_ODCost, args = (provider_file, u_shp, n, na_layer, ODfolder, smp, tempfolder, log_file, orgID, desID, cost, accost, restrict, hier, max_time_limit))
			p.start()
			p.join()
			
			watch.lap()
			togo = watch.format_time(watch.avg_sec*(totaln-n-1))
			arcpy.AddMessage('Each batch take about {0}secs. {1} hours  {2} mins {3} secs to go...'.format(str(watch.avg_sec)[0:5], togo[0], togo[1], togo[2]))
			
			n += 1
			
		
	except Exception as e:
		arcpy.AddError(e.message)
