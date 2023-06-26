class Users(Resource):
    # methods go here, including top
    pass

class Quotes(Resource):
    # methods go here
    pass

class Scenes(Resource):
    # methods go here
    pass

class Movies(Resource):
    # methods go here
    pass

api.add_resource(Users, "/users")
api.add_resource(Locations, "/quotes")
api.add_resource(Scenes, "/scenes")
api.add_resource(Scenes, "/movies")
