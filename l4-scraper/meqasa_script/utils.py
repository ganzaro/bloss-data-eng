import datetime


def save_data(df):
    file_time = datetime.datetime.now()
    file_time = file_time.strftime("%Y-%m-%d")
    fine_name = "meqasa_" + file_time + ".csv"
    df.to_csv("data/" + fine_name, index=False)

