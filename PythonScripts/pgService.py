import psycopg2


def insertAverageData():
	try:
		conn = getConnection()
		cursor = conn.cursor()
		cursor.execute("""INSERT INTO averagedata(camera_id, weekday, hour, averageleft, averageright) SELECT camera_id, extract(isodow from datetime), extract(hour from datetime), SUM(leftvehicles)/ COUNT(leftvehicles) As Average, SUM(rightvehicles)/COUNT(rightvehicles) FROM cameradata GROUP BY camera_id, extract(isodow from datetime), extract(hour from datetime)""")
		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
	    print(e)
	    
	    
def deleteAverageData():
	try:
		conn = getConnection()
		cursor = conn.cursor()
		cursor.execute("""DELETE FROM averagedata""")
		conn.commit()		
		cursor.close()
		conn.close()
	except Exception as e:
	    print(e)
	    	    	    
def selectAverageData():
	try:
		conn = getConnection()
		cursor = conn.cursor()
		cursor.execute("""SELECT * FROM averagedata""")
		conn.commit()
		rows = cursor.fetchall()
		print(rows)	
		cursor.close()
		conn.close()
	except Exception as e:
	    print("Uh oh, can't connect. Invalid dbname, user or password?1")
	    print(e)

def getAverageInfo(camId,date):
	try:
		conn = getConnection()
		cursor = conn.cursor()
		cursor.execute("""SELECT averageleft,averageright FROM averagedata WHERE weekday = extract(isodow from %s) AND hour = extract(hour from %s) and camera_id = %s""",(date,date,camId))
		conn.commit()
		row = cursor.fetchone()
		print(row)	
		return row
		cursor.close()
		conn.close()
	except Exception as e:
	    print("Uh oh, can't connect. Invalid dbname, user or password?1")
	    print(e)
	
	    
	
def selectTable():
	try:
		conn = getConnection()
		cursor = conn.cursor()
		cursor.execute("""SELECT * FROM cameradata""")
		conn.commit()
		rows = cursor.fetchall()
		print(rows)	
		cursor.close()
		conn.close()
	except Exception as e:
	    print("Uh oh, can't connect. Invalid dbname, user or password?2")
	    print(e)
	    
def existsImageInTable(camId,ts):
	try:
		conn = getConnection()
		cursor = conn.cursor()
		cursor.execute("""SELECT 1  FROM cameradata WHERE camera_id = %s AND datetime = %s """,(camId,ts))
		conn.commit()
		row = cursor.fetchone()
		
		
		
		if row is None:
			return 0
		
		return row[0]	
		
		cursor.close()
		conn.close()
	except Exception as e:
	    print("exists not working")
	    print(e)
	    
	   	    
	    
def countTableInfo():
	try:
		conn = getConnection()
		cursor = conn.cursor()
		cursor.execute("""SELECT COUNT(*) FROM cameradata""")
		conn.commit()
		rows = cursor.fetchall()
		print(rows)	
		cursor.close()
		conn.close()
	except Exception as e:
	    print("Uh oh, can't connect. Invalid dbname, user or password?10")
	    print(e)

def dropTables():
	try:
		conn = getConnection()
		cursor = conn.cursor()
		cursor.execute("""DROP TABLE cameradata; DROP TABLE averagedata""")
		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
	    print("Uh oh, can't connect. Invalid dbname, user or password?3")
	    print(e)

def createTableInfo():
	try:
	    conn = getConnection()
	    
	    # create a psycopg2 cursor that can execute queries
	    cursor = conn.cursor()
	    # create a new table with a single column called "name"
	    cursor.execute("""
		CREATE TABLE cameradata (
			id SERIAL PRIMARY KEY,
			camera_id INTEGER NOT NULL,
			leftvehicles REAL NOT NULL,
			rightvehicles REAL NOT NULL,
			datetime TIMESTAMP NOT NULL
			)
		""")
	    #cursor.execute("""SELECT * from cameradata""")
	    conn.commit()
	    #rows = cursor.fetchall()
	    #print(rows)	
	    cursor.close()
	    conn.close()
	except Exception as e:
	    print("Uh oh, can't connect. Invalid dbname, user or password?4")
	    print(e)
	   

def createTableAverage():
	try:
	    conn = getConnection()
	    
	    # create a psycopg2 cursor that can execute queries
	    cursor = conn.cursor()
	    # create a new table with a single column called "name"
	    cursor.execute("""
		CREATE TABLE averagedata (
			id SERIAL PRIMARY KEY,
			camera_id INTEGER NOT NULL,
			weekday INTEGER NOT NULL,
			hour INTEGER NOT NULL,
			averageleft REAL NOT NULL,
			averageright REAL NOT NULL
			)
		""")
	    #cursor.execute("""SELECT * from cameradata""")
	    conn.commit()
	    #rows = cursor.fetchall()
	    #print(rows)	
	    cursor.close()
	    conn.close()
	except Exception as e:
	    print("Uh oh, can't connect. Invalid dbname, user or password?5")
	    print(e)

def insertCameraData(infoPerImage):
	try:
	    conn = getConnection()
	    
	    # create a psycopg2 cursor that can execute queries
	    cursor = conn.cursor()
	    # create a new table with a single column called "name"
	    cursor.execute("""
		INSERT INTO cameradata (
			camera_id,
			leftvehicles,
			rightvehicles,
			datetime
			) SELECT %s,%s,%s,%s
		""", (infoPerImage["camera"], infoPerImage["leftvehicles"], infoPerImage["rightvehicles"], infoPerImage["timestamp"] ))
	    #cursor.execute("""SELECT * from cameradata""")
	    conn.commit()
	    #rows = cursor.fetchall()
	    #print(rows)	
	    cursor.close()
	    #conn.close()
	except Exception as e:
	    print("Uh oh, can't connect. Invalid dbname, user or password?3")
	    print(e) 
	    
	 
	 
def insertCameraDatafromList(infoImages):
	try:
	    conn = getConnection()
	    
	    # create a psycopg2 cursor that can execute queries
	    cursor = conn.cursor()
	    # create a new table with a single column called "name"
	    for infoPerImage in infoImages:
	    	cursor.execute("""
		INSERT INTO cameradata (
			camera_id,
			leftvehicles,
			rightvehicles,
			datetime
			) SELECT %s,%s,%s,%s
		""", (infoPerImage["camera"], infoPerImage["leftvehicles"], infoPerImage["rightvehicles"], infoPerImage["timestamp"] ))
	    #cursor.execute("""SELECT * from cameradata""")
	    conn.commit()
	    #rows = cursor.fetchall()
	    #print(rows)	
	    cursor.close()
	    conn.close()
	except Exception as e:
	    print("Uh oh, can't connect. Invalid dbname, user or password?3")
	    print(e)


def getConnection():
	try:
	    connect_str = "dbname='trafficdatadb' user='andi' host='localhost' " + \
		          "password='de'"
	    # use our connection values to establish a connection
	    conn = psycopg2.connect(connect_str)
	    return conn
	except Exception as e:
#	    print("Uh oh, can't connect. Invalid dbname, user or password?")
	    print(e)



