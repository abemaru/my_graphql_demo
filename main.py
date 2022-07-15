import graphene
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self,info,name):
        return "Hello " + name

app = FastAPI(title='ContactQL', description='GraphQL Contact APIs', version='0.1')
@app.get("/")
async def root():
    return {"message": "Contact Applications!"}

app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))