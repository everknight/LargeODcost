import os, arcpy, datetime, ast, sys, importlib
from multiprocessing import Process, set_executable, Pool

arcpy.env.overwriteOutput = True
set_executable(os.path.join(sys.exec_prefix, 'pythonw.exe'))


sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import timer_class as tc
import Module_Generate_OD_Pro_single
importlib.reload(Module_Generate_OD_Pro_single)
from Module_Generate_OD_Pro_single import *


if __name__ == '__main__':
	try:
		
		default_workspace = arcpy.env.workspace

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

		arcpy.env.workspace = inputfolder
		allshps = arcpy.ListFeatureClasses()
		usable_shp = []
		for each_shp in allshps:
			usable_shp.append(inputfolder + '\\' + each_shp)
		
		if not os.path.exists(ODfolder + '\\error_shp.gdb'):
			error_gdb = arcpy.CreateFileGDB_management(ODfolder, '\\error_shp.gdb')
			
		if not os.path.exists(ODfolder + '\\OD_cost_out.gdb'):
			arcpy.CreateFileGDB_management(ODfolder, 'OD_cost_out.gdb')
			
		arcpy.SetProgressor("step", "Generating OD cost matrix...")

		totaln = int(len(usable_shp))
		watch=tc.timer()
		
		
		n = 0
		while n < totaln:
			u_shp = usable_shp[n]
			# for i in range(0,6):
				# if n < len(shps_list_list[i]):
					# u_shp.append(shps_list_list[i][n])
			arcpy.AddMessage("Working on "+str(u_shp)+"...")
			progress = int(float(n)/totaln * 100)
			arcpy.SetProgressorPosition (progress)

			#arcpy.AddMessage(str(argv))
			
			#get_ODCost(provider_file, u_shp, n, na_layer, ODfolder, smp, tempfolder, log_file, orgID, desID, cost, accost, restrict, hier, max_time_limit)
			p = Process(target = get_ODCost, args = (provider_file, u_shp, n, na_layer, ODfolder, smp, tempfolder, log_file, orgID, desID, cost, accost, restrict, hier, max_time_limit))
			p.start()
			p.join()
			#with Pool(processes=6) as p:
			#	results = p.starmap(get_ODCost, argv)
			
			watch.lap()
			togo = watch.format_time(watch.avg_sec*(totaln-n-1))
			arcpy.AddMessage('Each batch take about {0}secs. {1} hours  {2} mins {3} secs to go...'.format(str(watch.avg_sec)[0:5], togo[0], togo[1], togo[2]))
			
			n += 1
		#p.join()
			
		
	except Exception as e:
		arcpy.AddError(str(e))
