import urllib2, zipfile, os, json, arcpy

apikey = arcpy.GetParameterAsText(0) 
inputfile = arcpy.GetParameterAsText(1)
org_name = arcpy.GetParameterAsText(2)
org_id = arcpy.GetParameterAsText(3)
dest_name = arcpy.GetParameterAsText(4)
dest_id = arcpy.GetParameterAsText(5)
outputfile = arcpy.GetParameterAsText(6)


def fetch_google_OD (download_link):
	download_link = basestring.format(org_add, dest_add, apikey)
	req = urllib2.urlopen(download_link)
	jsonout = json.loads(req.read())
	nt_time = jsonout['rows'][0]['elements'][0]['duration']['text']
	nt_dist = jsonout['rows'][0]['elements'][0]['distance']['text']
	return [nt_time, nt_dist]
	
sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import timer_class as tc
	
basestring = 'https://maps.googleapis.com/maps/api/distancematrix/json?language=en&origins={0}&destinations={1}&key={2}'


sc = arcpy.SearchCursor(inputfile)	
f = open(outputfile, 'w')
f.write('{0}, {1}, TimeCost, Distance\n'.format(org_id, dest_id))

totaln = int(str(arcpy.GetCount_management(inputfile)))
i = 0
watch = tc.timer()
row = sc.next()
while row:
	org_add = row.getValue(org_name)
	dest_add = row.getValue(dest_name)
	if type(dest_add) == type('a'):
		dest_add = dest_add.replace(' ', '%20')
	orgid_text = row.getValue(org_id)
	destid_text = row.getValue(dest_id)
	
	arcpy.AddMessage('Fetching Traveling time for {0} {1} to {2} {3}...'.format(org_id, orgid_text, dest_id, destid_text))
	download_link = basestring.format(org_add, dest_add, apikey)
	ggl_cost = fetch_google_OD(download_link)
	f.write('{0}, {1}, {2}, {3}\n'.format(orgid_text, destid_text, ggl_cost[0], ggl_cost[1]))
	
	i += 1
	if i % 100 == 0:
		watch.lap()
		togo = watch.format_time(watch.avg_sec*(totaln-i)/100)
		arcpy.AddMessage('Each batch take about {0}secs. {1} hours  {2} mins {3} secs to go...'.format(str(watch.avg_sec)[0:5], togo[0], togo[1], togo[2]))
	
	row = sc.next()
	

f.close()