#****************************************************************************
# (C) Cloudera, Inc. 2020-2022
#  All rights reserved.
#
#  Applicable Open Source License: GNU Affero General Public License v3.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# #  Author(s): Paul de Fusco
#***************************************************************************/

# Airflow DAG
from cloudera.cdp.airflow.operators.cde_operator import CDEJobRunOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from dateutil import parser
from airflow.decorators import task
from airflow import DAG
import pendulum

username = "pdefusco_052923"

print("Running as Username: ", username)

cde_spark_job_name = 'spark-sql'

default_args = {
        'owner': username,
        'retry_delay': timedelta(seconds=5),
        'depends_on_past': False,
        'start_date': pendulum.datetime(2020, 1, 1, tz="Europe/Amsterdam"), #Start Date must be in the past
        'end_date': datetime(2023,9,30,8) #End Date must be in the future
        }

dag_name = '{}-airflow-dag'.format(username)

with DAG(
        dag_name,
        default_args=default_args,
        schedule_interval='@daily',
        catchup=False,
        is_paused_upon_creation=False
        ) as dag:

    start = DummyOperator(
                    task_id="start")

    spark_sql = CDEJobRunOperator(
            task_id='sparksql-task',
            job_name=cde_spark_job_name
            )

    read_conf = BashOperator(
        	task_id="read-resource-file-task",
        	bash_command="cat /app/mount/my_airflow_file_resource/my_file.conf",
            do_xcom_push=True
    	)

    def _print_confs(**context):
        return context['ti'].xcom_pull(task_ids='read-resource-file-task')

    pythonstep = PythonOperator(
        task_id="print_file_resource_confs",
        python_callable=_print_confs,
    )

    @task.branch(task_id="branch_task")
    def branch_func(**context):
        airflow_file_resource_value = int(context['ti'].xcom_pull(task_ids="read-resource-file-task"))
        if airflow_file_resource_value >= 5:
            return "continue_task"
        elif airflow_file_resource_value >= 2 and airflow_file_resource_value < 5:
            return "stop_task"
        else:
            return None

    branch_op = branch_func()

    continue_op = EmptyOperator(task_id="continue_task")
    stop_op = EmptyOperator(task_id="stop_task")


start >> spark_sql >> read_conf >> pythonstep >> branch_op >> [continue_op, stop_op]
