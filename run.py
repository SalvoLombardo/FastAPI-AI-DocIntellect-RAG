from fastapi import FastAPI
from app.routes.upload import upload_router
from app.routes.query import query_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(query_router)




"""
(venv) salvatorelombardo@Mini-di-Salvo FastAPI_Project_AI_RAG % alembic ini alembic
usage: alembic [-h] [--version] [-c CONFIG] [-n NAME] [-x X] [--raiseerr] [-q]
               {branches,check,current,downgrade,edit,ensure_version,heads,history,init,list_templates,merge,revision,show,stamp,upgrade} ...
alembic: error: argument {branches,check,current,downgrade,edit,ensure_version,heads,history,init,list_templates,merge,revision,show,stamp,upgrade}: invalid choice: 'ini' (choose from branches, check, current, downgrade, edit, ensure_version, heads, history, init, list_templates, merge, revision, show, stamp, upgrade)
(venv) salvatorelombardo@Mini-di-Salvo FastAPI_Project_AI_RAG % 



"""