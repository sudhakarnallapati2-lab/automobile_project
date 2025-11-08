from fastapi import FastAPI, UploadFile, File
from fastapi_server.model_helper import predict

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Car Damage Detection API Running ✅"}


@app.post("/predict")
async def get_prediction(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        temp_path = "temp.jpg"

        with open(temp_path, "wb") as f:
            f.write(image_bytes)

        result = predict(temp_path)
        return result

    except Exception as e:
        return {"error": str(e)}
