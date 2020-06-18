import arcpy, os

smp = arcpy.GetParameterAsText(0)
cost = arcpy.GetParameterAsText(1)
accost = arcpy.GetParameterAsText(2).split(';')
restrict = arcpy.GetParameterAsText(3).split(';')
hierarchy = arcpy.GetParameterAsText(4).upper()
if hierarchy=='#':
	hierarchy = 'FALSE'
	
NTsetting = os.path.split(os.path.realpath(__file__))[0]+'\\Default_NetworkData_Setting.txt'
ntf = open(NTsetting, 'w')
ntf.write('path = r\"{0}\"\n'.format(smp))
ntf.write('cost = \"{0}\"\n'.format(cost))
ntf.write('accost = '+str(accost)+'\n')
if restrict == '#' or restrict == '':
    ntf.write('restrict = ""\n')
else:
    ntf.write('restrict = '+str(restrict)+'\n')
ntf.write('hierarchy = \"'+hierarchy.upper()+'\"\n')
ntf.close()

arcpy.AddMessage('\n\nSuccessfully Seting the Default Network Data setting!!!\n')
arcpy.AddMessage('path = r\"{0}\"'.format(smp))
arcpy.AddMessage('cost = \"{0}\"'.format(cost))
arcpy.AddMessage('accost = '+str(accost))
arcpy.AddMessage('restrict = '+str(restrict)+'')
arcpy.AddMessage('hierarchy = \"'+hierarchy.upper()+'\"\n')