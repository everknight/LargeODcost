import arcpy, math, os

zcta_area_file = arcpy.GetParameterAsText(0)  
zcta_field_name = arcpy.GetParameterAsText(1)  
output_folder = arcpy.GetParameterAsText(2)  
output_csv = output_folder+"\\intra_zcta_OD_for_" + os.path.splitext(os.path.split(zcta_area_file)[1])[0] + ".csv"

b_peri_t = arcpy.GetParameterAsText(3)
if b_peri_t == "":
    b_peri_t = 0.04
    
b_area_t = arcpy.GetParameterAsText(4)
if b_area_t == "":
    b_area_t = 0.88

a_t = arcpy.GetParameterAsText(5)
if a_t == "":
    a_t = -0.02

b_peri_d = arcpy.GetParameterAsText(6)
if b_peri_d == "":
    b_peri_d = 0.02
    
b_area_d = arcpy.GetParameterAsText(7)
if b_area_d == "":
    b_area_d = 0.37
    
a_d = arcpy.GetParameterAsText(8)
if a_d == "":
    a_d = -0.01


outdata = open(output_csv, "w")
outdata.write("ozcta, dzcta, minutes, miles, lvl\n")


all_fields = arcpy.ListFields(zcta_area_file)
pari = False
ar = False
for field in all_fields:
    print(field.name)
    if field.name == "PariLenMI":
       arcpy.DeleteField_management(zcta_area_file, "PariLenMI")
    if field.name == "AreaMI":
       arcpy.DeleteField_management(zcta_area_file, "AreaMI")
    if pari and ar:
        break

arcpy.AddField_management(zcta_area_file, "PariLenMI", "float")
arcpy.AddField_management(zcta_area_file, "AreaMI", "float")
arcpy.CalculateGeometryAttributes_management(zcta_area_file, [["PariLenMI", "PERIMETER_LENGTH"]], "MILES_US")
arcpy.CalculateGeometryAttributes_management(zcta_area_file, [["AreaMI", "AREA"]], area_unit = "SQUARE_MILES_US")

sc = arcpy.SearchCursor(zcta_area_file)
row = sc.next()
while row:
    zcta = row.getValue(zcta_field_name)
    pari = row.getValue("PariLenMI")
    area = row.getValue("AreaMI")
    time = a_t + b_peri_t * pari + b_peri_t*math.sqrt(area)
    distance = a_d + b_peri_d * pari + b_peri_d*math.sqrt(area)
    outdata.write("{0},{1},{2},{3},0\n".format(zcta, zcta, time, distance))
    row = sc.next()
    
outdata.close()