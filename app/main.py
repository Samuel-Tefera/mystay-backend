from fastapi import FastAPI

app = FastAPI(title='MyStay API')

@app.get('/')
def welcome():
  return {'message': 'Welome to MyStay'}