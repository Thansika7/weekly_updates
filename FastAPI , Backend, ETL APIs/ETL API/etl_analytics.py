import pandas as pd
import logging
import os

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Header

from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
import models
import schemas

from dotenv import load_dotenv


load_dotenv()

Base.metadata.create_all(bind=engine)


# logging
logging.basicConfig(

    filename="app.log",

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)


API_KEY = os.getenv("API_KEY")


app = FastAPI()


# db connection
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# API KEY AUTH FUNCTION

def verify_api_key(x_api_key: str = Header(...)):

    if x_api_key != API_KEY:

        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/")
def home():
    return {"message": "Laptop ETL API is running"}

@app.post("/upload")
def upload_csv(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    api_key: str = Depends(verify_api_key)

):

    try:

        logging.info("Upload started")

        df = pd.read_csv(file.file)

        logging.info(f"File received: {file.filename}")

        logging.info(f"Before cleaning: {len(df)}")


        df.replace("?", pd.NA, inplace=True)


        df.dropna(inplace=True)


        logging.info(f"After cleaning: {len(df)}")


        df["Ram"] = df["Ram"].str.replace("GB", "", regex=False)
        df["Ram"] = pd.to_numeric(df["Ram"], errors="coerce")


        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")


        df["Inches"] = pd.to_numeric(df["Inches"], errors="coerce")


        df.dropna(inplace=True)


        logging.info("Transformation complete")


        total = len(df)

        avg_price = df["Price"].mean()

        max_price = df["Price"].max()

        min_price = df["Price"].min()

        avg_ram = df["Ram"].mean()


        company_distribution = df["Company"].value_counts().to_dict()


        count = 0

        for i, row in df.iterrows():

            laptop = models.Laptop(

                company=row["Company"],

                ram=int(row["Ram"]),

                inches=float(row["Inches"]),

                price=float(row["Price"])

            )

            db.add(laptop)

            count += 1

        db.commit()


        logging.info(f"{count} records inserted")


        return {

            "Total": total,

            "Average Price": avg_price,

            "Max Price": max_price,

            "Min Price": min_price,

            "Average RAM": avg_ram,

            "Company Distribution": company_distribution

        }


    except Exception as e:

        logging.error(str(e))

        raise HTTPException(status_code=500, detail=str(e))



# view laptops

@app.get("/laptops", response_model=list[schemas.LaptopResponse])

def view_laptops(

    db: Session = Depends(get_db),

    api_key: str = Depends(verify_api_key)

):

    data = db.query(models.Laptop).all()

    return data