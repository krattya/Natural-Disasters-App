# %% [markdown]
# Import Libaries

# %%
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from pymongo import MongoClient

print("[x] Starting forecast_classification script")

# %% [markdown]
# Reading and format data from the csv file

# %%
df = pd.read_csv("testdata.csv")
df['DateTime'] = pd.to_datetime(df['DateTime'])
df.head()

# %% [markdown]
# Filtering data for magnitude >= 5

# %%
filtered_df = df.copy()
filtered_df = filtered_df[filtered_df['Magnitude'] >= 5]
filtered_df.head()

# %% [markdown]
# Add empty Column for Aftershock Counter, will be filled later

# %%
aftershock_data = filtered_df.copy()
for i in range(0,10):
    aftershock_data['day'+str(i)] = pd.Series([None] * len(aftershock_data))
aftershock_data.head()

# %% [markdown]
# is there an aftershock > 4 after an major earthquake?

# %%
for event_id in filtered_df['EventID'].unique():
    event_data = filtered_df[filtered_df['EventID'] == event_id]
    
    earthquake_datetime = event_data['DateTime'].iloc[0]

    # Is there an aftershock > 4?
    for i in range(0, 10):
      aftershock_bigger_four = 0
      day = earthquake_datetime + pd.Timedelta(days=i)
      day_after = day + pd.Timedelta(days=1)
      aftershocks_after_day = df[(df['DateTime'] > day)]
      aftershocks_on_day = aftershocks_after_day[(aftershocks_after_day['DateTime'] < day_after)]
      for index,row in aftershocks_on_day.iterrows():
        if row["Magnitude"] >= 4:
           aftershock_bigger_four = 1
           break
      daystring = "day"+str(i)
      aftershock_data.loc[aftershock_data["EventID"]== event_id,daystring] = aftershock_bigger_four

# %% [markdown]
# 1 -> major earthquake had an aftershock > 4 <br>
# 0 -> no aftershock > 4

# %%
aftershock_data

# %% [markdown]
# Select features

# %%
days = {}
for i in range(10):
    days["y_"+str(i)] = aftershock_data["day"+str(i)].copy()
    days["y_"+str(i)]= days["y_"+str(i)].astype(int)
features = ["Latitude","Longitude","Depth","Magnitude","Gap"]
X = aftershock_data[features].copy()

# %% [markdown]
# Train model for the first 10 days

# %%
models = {}
for i in range(10):
    models["model_"+str(i)] = DecisionTreeClassifier()
    models["model_"+str(i)].fit(X,days["y_"+str(i)])

# %% [markdown]
# Cross validation

# %%
cross_val_score(models["model_0"], X, days["y_0"], scoring="f1")

# %% [markdown]
# Add data to predict

# %%
gps = [[-125.046387,40.522151],[-117.751465,37.709899]]
Depth = [6.74,1.34]
Magnitude = [9.6,5.1]
Gap = [10,360]

data_to_predict = pd.DataFrame({"Longitude":[],"Latitude":[],"Depth":[],"Magnitude":[],"Gap":[]})

for cor in gps:
        for dep in Depth:
            for mag in Magnitude:
                for gap in Gap:
                    new_line = [cor[0],cor[1],dep,mag,gap]
                    data_to_predict.loc[len(data_to_predict)] = new_line

# %%
data_to_predict.head()

# %% [markdown]
# Predict data

# %%
predictions = {}
for i in range(10):
    predictions["day"+str(i)] = models["model_"+str(i)].predict(data_to_predict[features])

# %% [markdown]
# Store data in dataframe

# %%
for i in range(10):
    data_to_predict["day"+str(i)] = predictions["day"+str(i)]
data_to_predict

# %% [markdown]
# Save data to database

# %%
MONGO_DATABASE_URI: str = "mongodb://root:example@localhost:27018"
MONGO_DATABASE: str = "disaster_information"

client = MongoClient(MONGO_DATABASE_URI)
db = client.get_database(MONGO_DATABASE)
collection = db["predictions_2"]
data = data_to_predict.to_dict(orient="records")
collection.delete_many({})
collection.insert_many(data)

print("[x] End forecast_classification script")