import os
import json
import pandas as pd
from typing import List, Dict, Any
from fastapi import FastAPI, Query, File, UploadFile, HTTPException
from pymongo import MongoClient
from bson import json_util
import plotly.graph_objects as go
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base
import os.path


app = FastAPI()


def merge_json_files(filepaths: List[str]) -> List[Dict[str, Any]]:
    merged_data = []
    for filepath in filepaths:
        with open(filepath, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            merged_data.extend(data)
    return merged_data


@app.get("/datalist1")
async def get_merged_data():
    filepaths = ["2018.json", "2020.json", "2022.json"]
    merged_data = merge_json_files(filepaths)
    return {"ok": True, "list": merged_data}


@app.get("/datalist2")
async def get_data():
    try:
        data = pd.read_csv("dataset.csv")
        data_json = data.to_json(orient="records", force_ascii=False)
        return {"ok": True, "data": json.loads(data_json)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, "../secret.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg


HOSTNAME = get_secret("ATLAS_HOSTNAME")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
print("Connected to MongoDB....")

db = client["testdb"]


@app.get("/all_data")
def get_all_data():
    combined_data = {}
    db.drop_collection("alldata_collection")
    collection_name = "alldata_collection"
    collection = db[collection_name]

    for year in [2018, 2020, 2022]:
        file_name = f"{year}.json"
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        df1 = pd.DataFrame(data)
        df1 = df1.iloc[2:]  # 2행 부터
        df1.columns = ["노선", "상대공항", "운항(편)", "여객(명)", "화물(톤)"]
        df1 = df1.reset_index(drop=True)
        df1["상대공항코드"] = df1["상대공항"].apply(lambda x: x.split("(")[1].replace(")", ""))

        df2 = pd.read_csv("dataset.csv")

        merged_df = pd.merge(
            df1,
            df2[["공항코드1(IATA)", "도시명", "한글국가명"]],
            left_on="상대공항코드",
            right_on="공항코드1(IATA)",
            how="left",
        )
        merged_df.drop("공항코드1(IATA)", axis=1, inplace=True)  # 작업이 컬럼에 대해 수행
        json_data = merged_df.to_json(orient="records", force_ascii=False)
        data_dict = json.loads(json_data)

        combined_data[str(year)] = data_dict

    collection.insert_one(json_util.loads(json.dumps(combined_data)))

    return {"ok": True, "list": combined_data}


@app.get("/all_yeardata")
def get_year_data(year: int):
    data_dict = {}
    collection_name = f"collection_{year}"
    collection = db[collection_name]
    collection.drop()

    file_name = f"{year}.json"
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
    df1 = pd.DataFrame(data)
    df1 = df1.iloc[2:]
    df1.columns = ["노선", "상대공항", "운항(편)", "여객(명)", "화물(톤)"]
    df1 = df1.reset_index(drop=True)
    df1["상대공항코드"] = df1["상대공항"].apply(lambda x: x.split("(")[1].replace(")", ""))

    df2 = pd.read_csv("dataset.csv")

    merged_df = pd.merge(
        df1,
        df2[["공항코드1(IATA)", "도시명", "한글국가명"]],
        left_on="상대공항코드",
        right_on="공항코드1(IATA)",
        how="left",
    )
    merged_df.drop("공항코드1(IATA)", axis=1, inplace=True)

    json_data = merged_df.to_json(orient="records", force_ascii=False)
    data_dict[str(year)] = json.loads(json_data)

    collection.insert_one(json_util.loads(json.dumps(data_dict)))

    return {"ok": True, "list": data_dict}


def serialize_document(document):
    document.pop("_id", None)
    return json_util.dumps(document)


@app.get("/all_yeardatatop10")
def get_year_data(year: int):
    # Loading the JSON data and preprocessing with pandas
    file_name = f"{year}.json"
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
    df1 = pd.DataFrame(data)
    df1 = df1.iloc[2:]
    df1.columns = ["노선", "상대공항", "운항(편)", "여객(명)", "화물(톤)"]
    df1 = df1.reset_index(drop=True)
    df1["상대공항코드"] = df1["상대공항"].apply(lambda x: x.split("(")[1].replace(")", ""))

    df2 = pd.read_csv("dataset.csv")

    merged_df = pd.merge(
        df1,
        df2[["공항코드1(IATA)", "도시명", "한글국가명"]],
        left_on="상대공항코드",
        right_on="공항코드1(IATA)",
        how="left",
    )
    merged_df.drop("공항코드1(IATA)", axis=1, inplace=True)

    json_data = merged_df.to_json(orient="records", force_ascii=False)
    data_dict = json.loads(json_data)

    collection_name = f"collection_{year}"
    collection = db[collection_name]
    collection.drop()
    collection.insert_many(json_util.loads(json.dumps(data_dict)))

    merged_df["여객(명)"] = pd.to_numeric(merged_df["여객(명)"], errors="coerce")
    top_10_df = merged_df.nlargest(10, "여객(명)")

    json_data_top_10 = top_10_df.to_json(orient="records", force_ascii=False)
    top_10_data_dict = json.loads(json_data_top_10)

    top_10_collection_name = f"top_10_collection_{year}"
    top_10_collection = db[top_10_collection_name]
    top_10_collection.drop()
    top_10_collection.insert_many(json_util.loads(json.dumps(top_10_data_dict)))

    top_10_data_dict = json_util.dumps(top_10_data_dict)

    return {"ok": True, str(year): json.loads(top_10_data_dict)}


@app.get("/all_japan_rankings10")
def print_japan_rankings(year: int = Query(..., description="연도")):
    collection_name = f"top_10_collection_{year}"
    collection = db[collection_name]

    documents = list(collection.find({}))

    for i, doc in enumerate(documents):
        doc["_id"] = str(doc["_id"])
        doc["rank"] = i + 1

    japan_rankings = [doc for doc in documents if doc["한글국가명"] == "일본"]

    if japan_rankings:
        return {"ok": True, "list": {"year": year, "rankings": japan_rankings}}
    else:
        return {"ok": False, "error": "해당 연도의 일본 도시 데이터를 찾을 수 없습니다."}


@app.get("/save1")
async def save_figures():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
    secret_file = os.path.join(BASE_DIR, "../secret.json")

    with open(secret_file) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        try:
            return secrets[setting]
        except KeyError:
            errorMsg = "Set the {} environment variable.".format(setting)
            return errorMsg

    HOSTNAME = get_secret("ATLAS_HOSTNAME")
    USERNAME = get_secret("ATLAS_Username")
    PASSWORD = get_secret("ATLAS_Password")

    client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
    print("Connected to MongoDB....")

    db = client["testdb"]

    fig_combined = go.Figure()

    colors = ["rgb(158,202,225)", "rgb(242,177,172)", "rgb(188,189,34)"]

    for i, collection_name in enumerate(
        [
            "top_10_collection_2018",
            "top_10_collection_2020",
            "top_10_collection_2022",
        ]
    ):
        collection = db[collection_name]
        cursor = collection.find()

        df = pd.DataFrame(list(cursor))
        df["Year"] = collection_name.replace("top_10_collection_", "")
        df["여객(명)"] = pd.to_numeric(df["여객(명)"])

        df_combined = df.groupby("도시명")["여객(명)"].sum().reset_index()
        df_combined = df_combined.sort_values("여객(명)", ascending=False)
        df_combined["rank"] = range(1, len(df_combined) + 1)
        df_combined["rank"] = df_combined["rank"].astype(str) + "위"

        fig = go.Figure(
            data=[
                go.Bar(
                    x=df_combined["도시명"],
                    y=df_combined["여객(명)"],
                    text=df_combined["rank"],
                    textposition="auto",
                )
            ]
        )
        fig.update_layout(
            title=f"Year: {collection_name.replace('top_10_collection_', '')}",
            xaxis_title="도시명",
            yaxis_title="여객(명)",
            plot_bgcolor="rgb(255,255,255)",
            paper_bgcolor="rgb(255,255,255)",
            font_color="#333",
        )
        fig.update_traces(
            marker_color=colors[i],
            marker_line_color="rgb(8,48,107)",
            marker_line_width=1.5,
        )
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)

        fig.write_image(
            os.path.join(
                BASE_DIR,
                f"figure_{collection_name.replace('top_10_collection_', '')}.png",
            )
        )

        fig_combined.add_trace(
            go.Bar(
                x=df_combined["도시명"],
                y=df_combined["여객(명)"],
                name=f"Year: {collection_name.replace('top_10_collection_', '')}",
                marker_color=colors[i],
                marker_line_color="rgb(8,48,107)",
                marker_line_width=1.5,
                text=df_combined["rank"],
                textposition="auto",
            )
        )
    fig_combined.update_layout(
        title="Total 2018, 2020, 2022",
        xaxis_title="도시명",
        yaxis_title="여객(명)",
        plot_bgcolor="rgb(255,255,255)",
        paper_bgcolor="rgb(255,255,255)",
        font_color="#333",
    )
    fig_combined.update_xaxes(showgrid=False, zeroline=False)
    fig_combined.update_yaxes(showgrid=False, zeroline=False)

    fig_combined.write_image(os.path.join(BASE_DIR, "combined_figure.png"))

    return {"message": "ok save"}


@app.get("/save2")
async def save_figures():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
    secret_file = os.path.join(BASE_DIR, "../secret.json")

    with open(secret_file) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        try:
            return secrets[setting]
        except KeyError:
            errorMsg = "Set the {} environment variable.".format(setting)
            return errorMsg

    HOSTNAME = get_secret("ATLAS_HOSTNAME")
    USERNAME = get_secret("ATLAS_Username")
    PASSWORD = get_secret("ATLAS_Password")

    client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
    print("Connected to MongoDB....")

    db = client["testdb"]

    df_all_years = pd.DataFrame()

    fig_combined = go.Figure()

    df_all_combined = pd.DataFrame()

    for collection_name in [
        "top_10_collection_2018",
        "top_10_collection_2020",
        "top_10_collection_2022",
    ]:
        collection = db[collection_name]
        cursor = collection.find()

        df = pd.DataFrame(list(cursor))
        df["Year"] = collection_name.replace("top_10_collection_", "")
        df["여객(명)"] = pd.to_numeric(df["여객(명)"])

        df_combined = df.groupby("한글국가명")["여객(명)"].sum().reset_index()
        df_all_combined = pd.concat([df_all_combined, df_combined])

        fig = go.Figure(
            data=[go.Pie(labels=df_combined["한글국가명"], values=df_combined["여객(명)"])]
        )
        fig.update_layout(
            title=f"Year: {collection_name.replace('top_10_collection_', '')}",
            plot_bgcolor="rgb(255,255,255)",
            paper_bgcolor="rgb(255,255,255)",
            font_color="#333",
        )
        fig.write_image(
            os.path.join(
                BASE_DIR,
                f"pie_chart_{collection_name.replace('top_10_collection_', '')}.png",
            )
        )

        fig_combined.add_trace(
            go.Pie(
                labels=df_combined["한글국가명"],
                values=df_combined["여객(명)"],
                name=f"Year: {collection_name.replace('top_10_collection_', '')}",
            )
        )

    fig_combined.update_layout(
        title="Total 2018, 2020, 2022",
        plot_bgcolor="rgb(255,255,255)",
        paper_bgcolor="rgb(255,255,255)",
        font_color="#333",
    )
    fig_combined.update_yaxes(showgrid=False, zeroline=False)

    fig_combined.write_image(os.path.join(BASE_DIR, "combined_pie_chart.png"))

    return {"message": "ok: save"}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, "../secret.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg


HOSTNAME = get_secret("Mysql_Hostname")
PORT = get_secret("Mysql_Port")
USERNAME = get_secret("Mysql_Username")
PASSWORD = get_secret("Mysql_Password")
DBNAME = get_secret("Mysql_DBname")

DB_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}"

Base = declarative_base()


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    data = Column(LargeBinary)


def db_conn():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


@app.get("/upload_image_all")
def upload_images():
    inspector = inspect(create_engine(DB_URL))

    table_names = inspector.get_table_names()

    if "images" not in table_names:
        Base.metadata.create_all(create_engine(DB_URL))

    session = db_conn()

    image_names = [
        "combined_figure",
        "combined_pie_chart",
        "figure_2018",
        "figure_2020",
        "figure_2022",
        "pie_chart_2018",
        "pie_chart_2020",
        "pie_chart_2022",
    ]

    for image_name in image_names:
        with open(f"{image_name}.png", "rb") as file:
            binary_data = file.read()
        image = Image(name=image_name, data=binary_data)
        session.add(image)

    session.commit()
    return {"detail": "ok: Images uploaded to MySQL"}
