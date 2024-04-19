import pandas as pd
import folium
from sklearn.svm import SVR
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from pymongo import MongoClient


print("[x] Starting forecast script")

df = pd.read_csv("./testdata.csv")
df["DateTime"] = pd.to_datetime(df["DateTime"])
df.head()

filtered_df = df.copy()
filtered_df = filtered_df[filtered_df["Magnitude"] >= 5]
filtered_df.head()


aftershock_data = filtered_df.copy()
for i in range(0, 30):
    aftershock_data["day" + str(i)] = pd.Series([None] * len(aftershock_data))
aftershock_data["overallAftershocks"] = pd.Series([None] * len(aftershock_data))
aftershock_data.head()

for event_id in filtered_df["EventID"].unique():
    event_data = filtered_df[filtered_df["EventID"] == event_id]

    earthquake_datetime = event_data["DateTime"].iloc[0]

    # Iterate through days after the earthquake and count aftershocks
    aftershock_counts = []
    overall_count = 0
    for i in range(0, 30):
        day = earthquake_datetime + pd.Timedelta(days=i)
        day_after = day + pd.Timedelta(days=1)
        aftershocks_after_day = df[(df["DateTime"] > day)]
        aftershocks_on_day = aftershocks_after_day[
            (aftershocks_after_day["DateTime"] < day_after)
        ]
        aftershock_count = len(aftershocks_on_day)
        overall_count += aftershock_count
        daystring = "day" + str(i)
        aftershock_data.loc[
            aftershock_data["EventID"] == event_id, daystring
        ] = aftershock_count
    aftershock_data.loc[
        aftershock_data["EventID"] == event_id, "overallAftershocks"
    ] = overall_count

aftershock_data.head()

aftershock_data.to_csv("./result.csv")

daylist = []
for i in range(0, 30):
    daylist.append("day" + str(i))

df_durchschnitt = aftershock_data[daylist].mean()


m = folium.Map(
    location=[aftershock_data["Latitude"].mean(), aftershock_data["Longitude"].mean()],
    zoom_start=6,
    zoom_control=False,
    scrollWheelZoom=False,
    dragging=True,
)
for i in range(len(aftershock_data)):
    row = aftershock_data.iloc[i]
    folium.Marker([row["Latitude"], row["Longitude"]], popup=row["Magnitude"]).add_to(m)

days = {f"y_{i}": None for i in range(30)}
for i in range(30):
    days["y_" + str(i)] = aftershock_data["day" + str(i)].copy()

features = ["Latitude", "Longitude", "Depth", "Magnitude", "Gap"]
X = aftershock_data[features].copy()


preprocessor = ColumnTransformer(
    transformers=[("num", SimpleImputer(strategy="mean"), features)]
)

X = preprocessor.fit_transform(X)

models = {}
for i in range(30):
    models["model_" + str(i)] = SVR()
    models["model_" + str(i)].fit(X, days["y_" + str(i)])

gps = [[-125.046387, 40.522151], [-117.751465, 37.709899]]
Depth = [6.74, 1.34]
Magnitude = [9.6, 5.1]
Gap = [10, 360]

data_to_predict = pd.DataFrame(
    {"Longitude": [], "Latitude": [], "Depth": [], "Magnitude": [], "Gap": []}
)

for cor in gps:
    for dep in Depth:
        for mag in Magnitude:
            for gap in Gap:
                new_line = [cor[0], cor[1], dep, mag, gap]
                data_to_predict.loc[len(data_to_predict)] = new_line


predictions = {}
for i in range(30):
    predictions["day" + str(i)] = models["model_" + str(i)].predict(
        data_to_predict[features].values
    )

for i in range(30):
    data_to_predict["day" + str(i)] = predictions["day" + str(i)]


MONGO_DATABASE_URI: str = "mongodb://root:example@mongo:27017"
MONGO_DATABASE: str = "disaster_information"

client = MongoClient(MONGO_DATABASE_URI)
db = client.get_database(MONGO_DATABASE)
collection = db["predictions"]
data = data_to_predict.to_dict(orient="records")
collection.delete_many({})
result = collection.insert_many(data)

print(result.inserted_ids)
print("[x] Finished forecast script")
