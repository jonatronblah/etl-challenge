from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

import user_etl.user_sync as user_sync
from datetime import timedelta, datetime

stage_db = "stage_db"
home_dir = "/opt/airflow/dags/user_etl"

dag_email_recipient = "jonatron@gmail.com"


args = {
    "owner": "jonathan",
    "start_date": datetime(2024, 6, 26),
    "email": dag_email_recipient,
    "email_on_failure": False,
}


@dag(
    dag_id="user_etl",
    default_args=args,
    dagrun_timeout=timedelta(minutes=300),
    tags=["user", "etl", "stage"],
    schedule_interval=None,
    catchup=False,
)
def taskflow():
    @task(task_id="pull_push_user")
    def pull_push_user():
        # query api
        response_list = user_sync.call_api(size=100)
        # flatten and transform to pandas dataframe
        response_df = user_sync.flatten_df(response_list=response_list)
        # get db conn
        pg_hook_stage = PostgresHook(postgres_conn_id=stage_db)
        pg_engine_stage = pg_hook_stage.get_sqlalchemy_engine()
        # push to db
        response_df.to_sql(
            name="stage_user",
            con=pg_engine_stage,
            if_exists="append",
            index=False,
        )

    user_stage_task = pull_push_user()

    user_stage_task


dag = taskflow()
