from math import cos, asin, sqrt, pi

def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    m = 12742 * asin(sqrt(a)) #2*R*asin...
    return m

#lat1 = 53.32055555555556
#lat2 = 53.31861111111111
#lon1 = -1.7297222222222221
#lon2 = -1.6997222222222223

#lat1 = 41.0008
#lat2 = 42.0008
#lon1 = -101.99918
#lon2 = -102.99918


#41.0008	-101.99918

#xvar = distance(float(lat1),float(lon1),float(lat2),float(lon2))
#print(xvar)
#print(distance(53.32055555555556,-1.7297222222222221 ,53.31861111111111 ,-1.6997222222222223 ))