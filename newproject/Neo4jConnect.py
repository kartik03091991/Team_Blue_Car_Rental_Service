#neo123
#connection to neo4j
def neo4Connect(lstres):
    from py2neo import Graph, Node, Relationship 
    import neo4j
    #uri = "bolt://localhost:7687"
    #driver = neo4j.GraphDatabase.driver(uri, auth = ('neo4j','neo123'))
    graph = Graph("bolt://localhost:7687", user="neo4j", password="neo123")
    #session = driver.session()
    #graph = Graph()
    for x in range(0,len(lstres),3):
        car_id = Node("Car_ID", name = lstres[x])
        graph.create(car_id)
        service_center = Node("Service_Center", name = lstres[x+1])
        graph.create(service_center)
        graph.create(Relationship(car_id , 'distance',service_center))


    #graph.close()
    return('a')
    


lstres = ['2439', '8', 11.12, '2204', '3', 11.12, '2102', '1', 11.12, '2225', '5', 33.36, '2297', '10', 33.36, '2179', '2', 22.24, '2338', '7', 22.24, '2505', '9', 11.12, '2213', '4', 22.24]

res = neo4Connect(lstres)

print(res)

"""
    for x in range(0,len(lstres),3):
        b = lstres[x]
        tx.run("CREATE (a {name: $b})")
        #f"Car_ID : {lstres[x]} "
        #create (p:person {name:'Amber'})
        #CREATE (a {name: 'Andy'})
        #f"CREATE (n:Car_ID {lstres[x]})"
        nodes = session.run(q1)
"""