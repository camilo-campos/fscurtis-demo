from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse ,  JSONResponse
from fastapi.templating import Jinja2Templates
from chatbot import process_user_message
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# Montar la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hola gente, vamos a usar HTML con FastAPI"})


# Ruta para enviar mensajes
@app.post("/send-message")
async def send_message(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        id_sesion = data.get("id_sesion")
        
        
        print(f"User Input: {user_input}, Session ID: {id_sesion}")
        
        if not user_input or not id_sesion :
            raise HTTPException(status_code=400, detail="Message, id_sesion fields are required")
        
        # Procesa el mensaje del usuario usando la lógica del chatbot
        response = process_user_message(user_input, id_sesion)
        return JSONResponse(content={"response": response})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")