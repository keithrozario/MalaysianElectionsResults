# <author>Pieter Muller</author>
# <date>2012-11-14</date>

import sys
import sqlite3 as sqlite

tablesToIgnore = ["sqlite_sequence"]

outputFilename = None

def Print(msg):
    
    if (outputFilename != None):
        outputFile = open(outputFilename,'a')
        print >> outputFile, msg
        outputFile.close()
    else:
        print (msg)
        

def Describe(dbFile):
    connection = sqlite.connect(dbFile)
    cursor = connection.cursor()
    
    Print("TableName,Max(id),RowCount")

    totalTables = 0
    totalColumns = 0
    totalRows = 0
    totalCells = 0
    
    # Get List of Tables:      
    tableListQuery = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
    cursor.execute(tableListQuery)
    tables = map(lambda t: t[0], cursor.fetchall())
    
    for table in tables:
    
        if (table in tablesToIgnore):
            continue            
            
       
        rowsQuery = "SELECT Count() FROM %s" % table
        cursor.execute(rowsQuery)
        numberOfRows = cursor.fetchone()[0]
        
        maxidQuery = "SELECT max(id) FROM %s" % table
        cursor.execute(maxidQuery)
        maxid = cursor.fetchone()[0]
        
        Print("%s,%d,%s" % (table, numberOfRows, maxid))
        
       
    cursor.close()
    connection.close()   

            
if __name__ == "__main__":
    if (len(sys.argv) == 2):
        dbFile = sys.argv[1]
        Describe(dbFile)
    elif (len(sys.argv) == 3):
        dbFile = sys.argv[1]
        outputFilename = sys.argv[2]
        Describe(dbFile)
    else:        
        print ("\n\tUsage:")
        print ("\n\t\tDBDescribe.py {dbFile}")
        print ("\t\t\tPrints summary of {dbFile} to standard output.")
        print ("\n\t\tDBDescribe.py {dbFile} {outputFile}")
print ("\t\t\tAppends summary of {dbFile} to {outputFile}.")