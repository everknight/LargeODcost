import arcpy
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""
  
  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo() 
    
  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
    
    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""
    if self.params[0].altered and not self.params[0].hasBeenValidated:
	  sliced_gdb = self.params[0].value
	  arcpy.env.workspace = sliced_gdb
	  file = arcpy.ListFeatureClasses()[0]
	  fields = arcpy.ListFields(file)
	  self.field_name = []
	  for each_field in fields:
	    self.field_name.append(each_field.name)
	  self.params[1].filter.list = self.field_name
	  

    if self.params[5].altered and not self.params[5].hasBeenValidated:
      self.roadnetwork = self.params[5].value
      roadprop= arcpy.Describe(self.roadnetwork).attributes
      cost = []
      restrict = []
      for field in roadprop:
        if field.usageType == 'Cost':
	      cost.append(field.name)
        elif field.usageType == 'Restriction':
	      restrict.append(field.name)
      self.params[6].filter.list = cost
      self.params[7].filter.list = cost
      self.params[8].filter.list = restrict
     


    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return
