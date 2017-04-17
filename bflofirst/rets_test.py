#!/usr/bin/env python
import sys

import librets
from config import RETS_USERNAME, RETS_PASSWORD
#from dump import *

session = librets.RetsSession("http://rets.nys.mlsmatrix.com/rets/login.ashx")
session.Login(RETS_USERNAME,RETS_PASSWORD)

metadata = session.GetMetadata()

system = metadata.GetSystem()


def dump_all_tables(metadata, aClass):
    for table in metadata.GetAllTables(aClass):
        print "Table name: " + table.GetSystemName() + " [" + \
              table.GetStandardName() + "]"

def dump_all_classes(metadata, resource):
    resource_name = resource.GetResourceID()
    for aClass in metadata.GetAllClasses(resource_name):
        print "Resource name: " + resource_name + " [" + \
              resource.GetStandardName() + "]"
        print "Class name: " + aClass.GetClassName() + " [" + \
              aClass.GetStandardName() + "]"
        dump_all_tables(metadata, aClass)
        print

for resource in metadata.GetAllResources():
    break
    dump_all_classes(metadata, resource)

request = session.CreateSearchRequest("Property",
                                      "Listing",
                                      "(PostalCode=14225)")

try:
    request.SetStandardNames(True)
    #request.SetSelect("YearBuiltDescription")
    #request.SetLimit(librets.SearchRequest.LIMIT_DEFAULT)
    #request.SetOffset(librets.SearchRequest.OFFSET_NONE)
    #request.SetCountType(librets.SearchRequest.RECORD_COUNT_AND_RESULTS)
    #request.SetFormatType(librets.SearchRequest.COMPACT)
    results = session.Search(request)
except librets.RetsException as e:
    print("Caught:", e.GetMessage())

print "Record count: {!r}".format(results.GetCount())
print
columns = results.GetColumns()
while results.HasNext():
    for column in columns:
        print "{}: {}".format(column, results.GetString(column))

        # ~ logout = session.Logout()
        # ~ print("Billing info:", logout.GetBillingInfo())
        # ~ print("Logout message:", logout.GetLogoutMessage())
        # ~ print("Connect time:", logout.GetConnectTime())
