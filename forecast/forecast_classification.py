import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from pymongo import MongoClient

print("[x] Starting forecast_classification script")

df = pd.read_csv("testdata.csv")
df["DateTime"] = pd.to_datetime(df["DateTime"])


filtered_df = df.copy()
filtered_df = filtered_df[filtered_df["Magnitude"] >= 5]


aftershock_data = filtered_df.copy()
for i in range(0, 10):
    aftershock_data["day" + str(i)] = pd.Series([None] * len(aftershock_data))


for event_id in filtered_df["EventID"].unique():
    event_data = filtered_df[filtered_df["EventID"] == event_id]

    earthquake_datetime = event_data["DateTime"].iloc[0]

    # Is there an aftershock > 4?
    for i in range(0, 10):
        aftershock_bigger_four = 0
        day = earthquake_datetime + pd.Timedelta(days=i)
        day_after = day + pd.Timedelta(days=1)
        aftershocks_after_day = df[(df["DateTime"] > day)]
        aftershocks_on_day = aftershocks_after_day[
            (aftershocks_after_day["DateTime"] < day_after)
        ]
        for index, row in aftershocks_on_day.iterrows():
            if row["Magnitude"] >= 4:
                aftershock_bigger_four = 1
                break
        daystring = "day" + str(i)
        aftershock_data.loc[
            aftershock_data["EventID"] == event_id, daystring
        ] = aftershock_bigger_four


days = {}
for i in range(10):
    days["y_" + str(i)] = aftershock_data["day" + str(i)].copy()
    days["y_" + str(i)] = days["y_" + str(i)].astype(int)
features = ["Latitude", "Longitude", "Depth", "Magnitude", "Gap"]
X = aftershock_data[features].copy()


models = {}
for i in range(10):
    models["model_" + str(i)] = DecisionTreeClassifier()
    models["model_" + str(i)].fit(X, days["y_" + str(i)])

scores = {}
for i in range(10):
    scores["score_" + str(i)] = cross_val_score(
        models["model_" + str(i)], X, days["y_" + str(i)], scoring="f1"
    )
    print(f'F1-Score: {scores["score_"+str(i)].mean()}')


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
for i in range(10):
    predictions["day" + str(i)] = models["model_" + str(i)].predict(
        data_to_predict[features]
    )

for i in range(10):
    data_to_predict["day" + str(i)] = predictions["day" + str(i)]
data_to_predict

MONGO_DATABASE_URI: str = "mongodb://root:example@mongo:27017"
MONGO_DATABASE: str = "disaster_information"

client = MongoClient(MONGO_DATABASE_URI)
db = client.get_database(MONGO_DATABASE)
collection = db["predictions_2"]
data = data_to_predict.to_dict(orient="records")
collection.delete_many({})
result = collection.insert_many(data)
print(result.inserted_ids)


print("[x] End forecast_classification script")
