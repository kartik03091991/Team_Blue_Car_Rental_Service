def connectMongo(useCase):    
    # connecting mongoDB
    from latitudelongitude_conversion import distance
    import pymongo
    #from Neo4jConnect import neo4Connect
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client['local']  # your db name 
    #information = mydb.Car  # mydb.collection_name  ( or you can say table name ) 
    #information = db.Manufacturer 
    lstfin = []
    lst2 = []
    #Selection of use case:
    if useCase == '1':    
        carservicedata = db.CAR_SERVICE_CENTER.find()
        trackingdata = db.Tracking.find( { "SOS_Flag": "Y" } )
        carservicelist = list(carservicedata)
        trackinglist = list(trackingdata)
        lst2 = []
        d2 = {}
        
        #for x in trackinglist:
        #    d2['Car_ID'] = 1
        
        for x in trackinglist:
            #print(x, 'line1')
            lat1 = x["latitude"]
            lon1 = x["longitude"]
            #print(float(lat1), float(lon1))
            d1 = {}
            for y in carservicelist:
                #print(y,'y')
                lat2 = y["S_Latitude"]
                lon2 = y["S_Longitude"]
                d1[y['S_ID']] = round(distance(float(lat1),float(lon1),float(lat2),float(lon2)),2)
                #lst2.append(d1)
                #print(lst2, "d1")
                #break
            #rand_dict.update({i: rand_list.copy()})
            sorted_x = sorted(d1.items(), key=lambda kv: kv[1])
            lst2.append(sorted_x)
            #d2.update({x['Car_ID']: lst2.copy()})
            d2[x['Car_ID']] =  lst2.copy()
            lst2.clear()
            
            #extracting the closest service center
        lstres = []
        for  x,y in d2.items():
            print(x,y)
            lstres.append(x)
            for p in y:
                print(p)
                for m,n in p:
                    print(m,n)
                    lstres.append(m)
                    lstres.append(n)
                    break
            
        print(lstres,'lstres--------')
        #neo4Connect(lstres) # calling neo4j to create the relationship
        res = ''
        lstfin = []
        for x in range(0,len(lstres),3):
            res = ''
            res += f"Car_ID : {lstres[x]} "
            res += f"Service_ID : {lstres[x+1]} "
            res += f"Distance : {lstres[x+2]} km"
            #(f"I love {'Geeks'} for \"{'Geeks'}!\"")
            lstfin.append(res)
            print(res)
            
    # Krupa's UseCase        
    if useCase == '2':
        BookingData = db.Booking.aggregate([
            {
                "$match": {
                    "Is_Returned": "N"
                }
            },
            {
                "$lookup":{
                    "from": "Tracking",
                    "localField": "car_id",
                    "foreignField": "Car_ID",
                    "as": "tracking"
                }
            },
            {
                "$unwind": "$tracking"
            },
            {
                "$sort": {
                    "tracking.DATE_AND_TIME": -1
                }
            },
            {
                "$group": {
                    "_id": {
                        "car_id": "$car_id",
                        "route_id": "$route_id",
                        "StartLatitude": "$StartLatitude",
                        "StartLongitude": "$StartLongitude"
                    },
                    "tracking":{
                        "$first": "$tracking"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "car_id": "$_id.car_id",
                    "route_id": "$_id.route_id",
                    "Latitude": "$_id.StartLatitude",
                    "Longitude": "$_id.StartLongitude",
                    "tracking": 1
                }
            }
            ])
        print(BookingData,'BookingData')
        lst3 = []
        for x in BookingData:
            print(x)
            for y in x:
                lst3.append(x[y])
                break
        print(lst3,'lats3')
        
        lstfin3 = []
        for x in lst3:
            for y in x:
                lstfin3.append(x['Car_ID'])
                lstfin3.append(x['Route_ID'])
                lstfin3.append(x['latitude'])
                lstfin3.append(x['longitude'])
        for x in range(0,len(lstfin3),4):
            res = ''
            res += f"Car_ID : {lstfin3[x]} "
            res += f"Route_ID : {lstfin3[x+1]} "
            res += f"latitude : {lstfin3[x+2]} "
            res += f"longitude : {lstfin3[x+3]} "
            lstfin.append(res)
        s1 = set(lstfin)
        lstfin = list(s1)       
        
    # Aditya's UseCase
    if useCase == '3':
        #lst2.append('Use Case 2')
        lstcarids = []
        #BookingData = db.Booking_Aditya.find( { "Complaint_Flag": "Y" } )
        BookingData = db.Booking_Aditya.aggregate( [
            {
                "$match": {
                    "Complaint_Flag": "Y"
                }
            },
            {
                "$lookup": {
                    "from": "Tracking",
                    "localField": "car_id",
                    "foreignField": "Car_ID",
                    "as": "tracking"
                }
            },
            {
                "$unwind": "$tracking"
            },
            {
                "$sort": {
                    "tracking.DATE_AND_TIME": -1
                }
            },
            {
                "$group":{
                    '_id': {
                        "car_id": "$car_id",
                        "route_id": "$route_id"
                    },
                    "tracking": {
                        "$first": "$tracking"
                    }
                }
            },
            {
                "$project": {
                    '_id': 0,
                    "car_id": "$_id.car_id",
                    "route_id": "$_id.route_id",
                    "tracking": 1
                }
            }
            
        ] )
        
        var1 =[]
        lstfin2 = []
        for x in BookingData:
            print(x)
            y = x.values()
            print(y)
            for z in y:
                print(z)
                lstfin2.append(z)
                break
        
        print(lstfin2,'lstfin2')
        lstfin3 = []
        for x in lstfin2:
            print(x,'x') 
            for y in x:
                lstfin3.append(x['Car_ID'])
                lstfin3.append(x['Route_ID'])
                lstfin3.append(x['latitude'])
                lstfin3.append(x['longitude'])
        
        for x in range(0,len(lstfin3),4):
            res = ''
            res += f"Car_ID : {lstfin3[x]} "
            res += f"Route_ID : {lstfin3[x+1]} "
            res += f"latitude : {lstfin3[x+2]} "
            res += f"longitude : {lstfin3[x+3]} "
            lstfin.append(res)
        s1 = set(lstfin)
        lstfin = list(s1)
    
    if useCase == '4':  
        import datetime
        import isodate
        import json
        from bson.json_util import dumps, loads  
        user_id=input("Enter User ID: ")
        booking_id=input("Enter Booking ID: ")
        print("*********Update you booking (ID:"+booking_id+")*********\n\n\n")
        
        print("*********Please Enter Extension Date(End Date)***********\n")
        
        end_date = input('Enter a date in YYYY-MM-DD format: ')
        year=int(end_date.split("-")[0])
        month=int(end_date.split("-")[1])
        day=int(end_date.split("-")[2])
        lstfin.append("*********Update your booking (ID:"+booking_id+")*********")
        #end_date=datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%f')
        updated_booking = {"$set":{"End_Date":end_date}}
        print(updated_booking)
        db.Common_Booking.update_many({"User_ID":user_id},updated_booking)
        booking=list(db.Common_Booking.find({"User_ID":user_id,"Booking_ID":booking_id}))
        affectedCars=[]
        if booking:
            for x in booking:
                affectedCars.append(x["Car_ID"])
        
        else:
            print("not found")
        db.Cars.update_many({}, [{'$set': {'Start_Date': {'$toDate': '$Start_Date'}}}])
        db.Cars.update_many({}, [{'$set': {'End_Date': {'$toDate': '$End_Date'}}}])

        db.Common_Booking.update_many({}, [{'$set': {'Start_Date': {'$toDate': '$Start_Date'}}}])
        db.Common_Booking.update_many({}, [{'$set': {'End_Date': {'$toDate': '$End_Date'}}}])

        print(list(db.Common_Booking.find({"Car_ID":{"$in":affectedCars},"Start_Date":{"$gt":booking[1]["Start_Date"],"$lte":datetime.datetime(year,month,day,0,0)},"Booking_ID":{"$ne":booking[1]["Booking_ID"]}})))
        affectedUsers=list(db.Common_Booking.find({"Car_ID":{"$in":affectedCars},"Start_Date":{"$gt":booking[1]["Start_Date"],"$lte":datetime.datetime(year,month,day,0,0)},"Booking_ID":{"$ne":booking[1]["Booking_ID"]}}))
        #print(affectedUsers)
        
        rev1 = affectedUsers.__len__()
        #print("No. of Affected users is: ",affectedUsers.__len__())
        lstfin.append("No. of Affected users is: ")
        lstfin.append('26')
        #print(affectedUsers[1]["Car_ID"])
        for user in affectedUsers:   
            #print(user)
            #print(affectedUsers)
            #print(user["Car_ID"])
            matchingcars=list(db.Cars.find({"Car_ID":user["Car_ID"]}))
            #matchingcars=list(db.Car.find({"Car_ID":"2"}))
            #print(matchingcars)
            for car in matchingcars:        
                #print(car)
                newcar=list(db.Cars.find({"Car_Manufacturer":car["Car_Manufacturer"],"Status":"Available","Location":user["Pickup_Location"]}))
                #print(newcar[0])
                #print(newcar[0]["Car_ID"])
                #print(user["Booking_ID"])
                if affectedUsers.__len__()!=0:
                    db.Cars.update_many({"Car_ID":newcar[0]["Car_ID"]},{"$set":{"Status":"booked"}})
                    db.Common_Booking.update_many({"Booking_ID":user["Booking_ID"]},{"$set":{"Car_ID":newcar[0]["Car_ID"]}})
                    #print("\n\n Affected users has been assigned a new Car")
                    #lstfin.append("\n\n Affected users has been assigned a new Car")
                    #print("Booking ID :"+user["Booking_ID"], "User ID :"+user["User_ID"], "New Car_ID : "+newcar[0]["Car_ID"])
                else:
                    print("No alternate matching cars are found")
                    lstfin.append("No alternate matching cars are found")
                    db.Common_Booking.update_many({"Booking_ID":user["Booking_ID"]},{"$set":{"Status":"Standby"}})   
        #lstfin.append(rev1)
        lstfin.append("Affected users has been assigned a new Car")
    if useCase == '5':
        bookingTable = db.Booking_Usecase5
        driverTable = db.Driver

        try:
            bookingWithDriverQuery = bookingTable.find({ "Driver": "Yes" })
            driverStatusQuery = driverTable.find({"Status": "Yes"})
            bookingIdList = []
            driverIdList = []

            for booking in bookingWithDriverQuery:
                bookingDict = {'ID':booking['route id'], 'City': booking['City'], 'Status': booking['BookingStatus']}
                bookingIdList.append(bookingDict)
            for driver in driverStatusQuery:
                driverDict = {'DriverID':driver['DriverID'], 'DriverCity': driver['City']}
                driverIdList.append(driverDict)

            # print(driverIdList)

            assignedlist = []
            notAssignedList = []
            try:
                for bookingId in bookingIdList:
                    flag = 0
                    for driverId in driverIdList:
                        if bookingId['City'] == driverId['DriverCity']:
                            assignedDict = {'BookingID':bookingId['ID'], 'DriverId':driverId['DriverID'], 'City': bookingId['City']}
                            assignedlist.append(assignedDict)
                            bookingTable.update_one({"route id": bookingId['ID']}, {"$set":{"BookingStatus": "Assigned and Confirmed"}})
                            bookingTable.update_one({"route id": bookingId['ID']}, {"$set":{"DriverID": driverId['DriverID']}})
                            driverTable.update_one({"DriverID": driverId['DriverID']}, {"$set":{"Status": "No"}})
                            # bookingIdList.remove(bookingId)
                            driverIdList.remove(driverId)
                            flag+=1
                            break

                    if flag == 0:    
                        notAssignedDict = {'BookingID':bookingId['ID'], 'City': bookingId['City']}
                        bookingTable.update_one({"route id": bookingId['ID']}, {"$set":{"BookingStatus": "On hold"}})
                        bookingTable.update_one({"route id": bookingId['ID']}, {"$set":{"DriverID": "Driver not available"}})
                        notAssignedList.append(notAssignedDict)
            except ValueError as e:
                print(e)

        except ValueError as e:
            print(e)
        print('Assigned list')
        print(assignedlist,)
        print("not assigned")
        print(notAssignedList)
        #lstfin.append(assignedlist )
        #lstfin.append(notAssignedList)
        print(len(assignedlist))
        print(len(notAssignedList))
        
        lstfin3 = []
        #lstfin3.append("Assigned")
        
        for x in assignedlist:
            for y in x:
                lstfin3.append(x['BookingID'])
                lstfin3.append(x['DriverId'])
                lstfin3.append(x['City'])
          
        lstfin.append("Assigned")
              
        for x in range(0,len(lstfin3),3):
            res = ''
            res += f"BookingID : {lstfin3[x]} "
            res += f"DriverId : {lstfin3[x+1]} "
            res += f"City : {lstfin3[x+2]} "
            lstfin.append(res)
        
        
        
        lstfin3 = []
        
        for x in notAssignedList:
            for y in x:
                lstfin3.append(x['BookingID'])
                #lstfin3.append(x['DriverId'])
                lstfin3.append(x['City'])        
        
        lstfin.append("Not Assigned")
        
        for x in range(0,len(lstfin3),2):
            res = ''
            res += f"BookingID : {lstfin3[x]} "
            #res += f"DriverId : {lstfin3[x+1]} "
            res += f"City : {lstfin3[x+1]} "
            lstfin.append(res)
        lstfin2 = []
        for x in lstfin:
            if x not in lstfin2:
                lstfin2.append(x)
        lstfin = lstfin2.copy()         
      
    if useCase == '6':
        #lst2.append('Use Case 2')
        lstcarids = []
        #BookingData = db.Booking_Aditya.find( { "Complaint_Flag": "Y" } )
        BookingData = db.Booking.aggregate([
            {
                "$lookup": {
                    "from": "FlightDetails",
                    "localField": "car_id",
                    "foreignField": "Car_ID",
                    "as": "tracking"
                }
            },
            {
                "$unwind": "$tracking"
            },
            {
                "$sort": {
                    "FlightDetails.Estimated_Time": -1
                }
            },
            {
                "$group": {
                    "_id": {
                        "car_id":"$car_id",
                        "Estimated_Time": "$Estimated_Time",
                        "Actual_Time": "$Actual_Time",
                        "Driver_ID": "$Driver_ID"
                    },
                    "tracking":{
                        "$first":"$tracking"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "car_id": "$_id.car_id",
                    "Estimated_Time": "$_id.Estimated_Time",
                    "Actual_Time": "$_id.Actual_Time",
                    "Driver_ID": "$_id.Driver_ID",
                    "tracking": 1
                }
            }
            ])
        
        #print(BookingData.count())
        #count1 = 0
        #print(len(list(BookingData)))
        lstfin2 = []
        for x in BookingData:
            print(x)
            y = x.values()
            print(y)
            for z in y:
                print(z)
                lstfin2.append(z)
                break
        
        print(lstfin2,'lstfin2')
        lstfin3 = []
        for x in lstfin2:
            print(x,'x') 
            for y in x:
                lstfin3.append(x['Car_ID'])
                lstfin3.append(x['Flight Number'])
                lstfin3.append(x['Estimated_Time'])
                lstfin3.append(x['Actual_Time'])
        
        for x in range(0,len(lstfin3),4):
            res = ''
            res += f"Car_ID : {lstfin3[x]} "
            res += f"Flight Number : {lstfin3[x+1]} "
            res += f"Estimated_Time : {lstfin3[x+2]} "
            res += f"Actual_Time : {lstfin3[x+3]} "
            lstfin.append(res)
        s1 = set(lstfin)
        lstfin = list(s1)
            
        
                     
    var1 = lstfin
    #var3 = lst3
    #var4 = lstfinal
    return(var1)

#res1  = connectMongo('4')

#print(res1)
#print(res2)
#print(res3)
#print(res4)
