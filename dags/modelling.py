import pickle

import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression

from creds import db_path

import warnings

warnings.filterwarnings("ignore")

DB_URL = db_path


def convert(df):
    df = df.dropna()
    print("\nStart convert\n")
    df = df.sort_values("date", ascending=True)
    columns = ["open", "high", "low", "close"]
    new_columns = ["date"]
    time_before_for_predict = 100  # Time periods fo train
    for i in range(time_before_for_predict, 0, -1):
        for col in columns:
            new_columns.append(col + "_" + str(i) + "b")

    new_columns.extend(columns)
    # print(new_columns)

    new_df = pd.DataFrame(columns=new_columns[1:])
    date = np.array(df.iloc[time_before_for_predict:, 0].tolist()).reshape(
        -1, 1
    )  # slide wich == 100 dates
    df_lst = np.array(df.drop("date", axis=1))
    for i in range(time_before_for_predict, df.shape[0]):

        new_df.loc[new_df.shape[0]] = (
            df_lst[i - time_before_for_predict : i + 1]
            .reshape((1, -1))
            .astype(float)[0]
        )

    return new_df


def get_data_from_db(name_db):
    engine = create_engine(DB_URL)
    df = pd.read_sql_table(name_db, engine)
    print(f"data from {name_db} was got")
    return df


def make_model1(df: pd.DataFrame, columns_to_drop: list, column_pred, name_table):
    X, y = df.drop(columns_to_drop, axis=1), df[column_pred]
    print(f"X_col for {column_pred} : {X.columns}")
    range_for_test = 500
    X_train, X_test, y_train, y_test = (
        X[:-range_for_test],
        X[-range_for_test:],
        y[:-range_for_test],
        y[-range_for_test:],
    )

    print(f"\nStart train model_{name_table}_{column_pred}")

    grid = LinearRegression()

    grid.fit(X_train, y_train)

    y_pred_train = grid.predict(X_train)
    print(
        "for",
        column_pred,
        "train",
        r2_score(y_train, y_pred_train),
        mean_squared_error(y_train, y_pred_train),
    )

    y_pred = grid.predict(X_test)
    print("test", r2_score(y_test, y_pred), mean_squared_error(y_test, y_pred))
    # print(y_pred)

    print(f"gb importances {pd.Series(grid.coef_, X.columns)}")
    # print(f"feature {pd.Series(gb.coefs_, X.columns)}")
    model_path = f"models/model_{name_table}_{column_pred}.pkl"
    with open(model_path, "wb") as file:
        pickle.dump(grid, file)


def start_train(tables: list):
    for table in tables:
        df = get_data_from_db(table)
        # df = pd.read_csv("IBM_data.csv", index_col=0)
        df = convert(df)

        df = df.dropna()
        print(f"conerted df {table} was completed")
        col = ["open", "high", "low", "close", "date"]
        for i in range(len(col) - 1):
            make_model1(df, col[i:-1], col[i], table)


def main():
    tables_for_train = ["IBM_stock", "GOOGL_stock", "MSFT_stock"]
    start_train(tables_for_train)


main()
