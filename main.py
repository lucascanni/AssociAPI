# Import du framework
from fastapi import FastAPI

# Import des routers
from routers import router_members
from routers import router_auth
from routers import router_stripe

# Import de la description de l'API
from documentation.description import api_description

# Création de l'application
app = FastAPI(
    title='AssociAPI',
    description=api_description,
    docs_url='/',
)

# Ajout des routers
app.include_router(router_members.router)
app.include_router(router_auth.router)
app.include_router(router_stripe.router)