import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import RedirectResponse
from beanie import init_beanie

from config import settings
from openapi import initialise_openapi
# from routers import router
from model import __beanie_models__

# app object
app = FastAPI()


origins = ['http://localhost:3000',
           'http://localhost:5173'
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

import routers

@app.on_event('startup')
async def startup_event():
    try:
        app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
        app.mongodb = app.mongodb_client[settings.MONGODB_NAME]

        await init_beanie(
                database=app.mongodb_client[settings.MONGODB_NAME],
                document_models=__beanie_models__,
            )

    except Exception as e:
        logger.error(f"Failed to connect with MongoDB: {e}.")
    else:
        logger.info('Connect to MongoDB ✅')
        
    
    
@app.on_event("shutdown")
async def shutdown_db_client():
  
  logger.info('DB connection Shutdown')

  try:
    app.mongodb_client.close()
  except Exception as e:
    logger.error(f"Failed to close connection w/ MongoDB: {e}.")
  else:
    logger.info('Close connection w/ MongoDB')


@app.get('/', include_in_schema=False)
async def get_root():
  if (root_url := os.environ.get('ROOT_URL')) is None:
    return {
      'api_docs': {
        'openapi': f'{root_url}/docs',
        'redoc': f'{root_url}/redoc'
      }
    }
    
  response = RedirectResponse(url=f"{root_url}/docs")
  return response


initialise_openapi(app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )