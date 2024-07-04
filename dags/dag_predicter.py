import datetime as dt


from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from stock_predictor import get_predict_data
from funs import delete_from_table, add_row_predict

from settings import db_names


def start_pred():
    # for symbol in db_names:
    for symbol in ["ibm_stock"]:
        df = get_predict_data(symbol)
        print(f"predict for {symbol} was got")

        delete_from_table(f"{symbol}_predict")
        df.apply(lambda x: add_row_predict(x, symbol), axis=1)
        print(f"Data for {symbol} was add to table")


args = {
    "owner": "airflow",
    "start_date": dt.datetime(2024, 6, 25),
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=1),
    "depends_on_past": False,
}


with DAG(
    dag_id="dag_predicter",
    schedule_interval="@daily",
    default_args=args,
) as dag:

    first_task = BashOperator(
        task_id="first_task",
        bash_command='echo "Start predictions"',
        dag=dag,
    )

    start = PythonOperator(task_id="pasrecompaire", python_callable=start_pred, dag=dag)

    first_task >> start
