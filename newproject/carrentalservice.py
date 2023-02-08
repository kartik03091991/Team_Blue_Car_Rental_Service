def connectMongo(useCase):    
    # connecting mongoDB
    from latitudelongitude_conversion import distance
    import pymongo
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client['local']  # your db name 
    #information = mydb.Car  # mydb.collection_name  ( or you can say table name ) 
    information = db.Manufacturer 
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
            
    if useCase == '2':
        #lst2.append('Use Case 2')
        lstcarids = []
        BookingData = db.Booking_Aditya.find( { "Complaint_Flag": "Y" } )
        #data2 = data.find()
        
        for x in BookingData:
            lst2.append(x)
            print(x)
            lstcarids.append(x['car_id'])
        var2 = lstcarids
        # looping through lstcarids in tracking and extracting from it
        lst3 = []
        
        for x in lstcarids:
            TraickingData = db.Tracking.find( { "Car_ID": x } )
            for y in TraickingData:
                lst3.append(y)
            lstlat = []
            lstlong = []
            lstdatetime = []
            lstfinal = []          
            for z in lst3:
                lstlat.append(z['latitude'])
                lstlong.append(z['longitude'])
                lstdatetime.append(z['Date_and_Time'])
            lstfinal.append(x)    
            lstfinal.append(lstlat[-1])
            lstfinal.append(lstlong[-1])
            lstfinal.append(lstdatetime[-1])
            break    
        lstfin.append('Use Case 2 Inprogress') 
            
    if useCase == '3':
        lstfin.append('Use Case 3 Inprogress')

    var1 = lstfin
    #var3 = lst3
    #var4 = lstfinal
    
    return(var1)

res1  = connectMongo('1')

print(res1)
#print(res2)
#print(res3)
#print(res4)
