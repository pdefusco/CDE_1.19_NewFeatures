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
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from dateutil import parser
from airflow import DAG
import pendulum

username = "pdefusco_020723"

print("Running as Username: ", username)

cde_spark_job_name = 'spark-sql'

"""cde_job_name_07_B = '07_B_pyspark_RIGHT'
cde_job_name_07_C = '07_C_pyspark_JOIN'"""

default_args = {
        'owner': username,
        'retry_delay': timedelta(seconds=5),
        'depends_on_past': False,
        'start_date': pendulum.datetime(2020, 1, 1, tz="Europe/Amsterdam"), #Start Date must be in the past
        'end_date': datetime(2023,9,30,8) #End Date must be in the future
        }

dag_name = '{}-airflow-dag'.format(username)

dag = DAG(
        dag_name,
        default_args=default_args,
        schedule_interval='@daily',
        catchup=False,
        is_paused_upon_creation=False
        )

start = DummyOperator(
                task_id="start",
                dag=dag)

spark_sql = CDEJobRunOperator(
        task_id='create-left-table',
        dag=dag,
        job_name=cde_spark_job_name
        )

read_conf = BashOperator(
    	task_id="read_conf",
        dag=dag,
    	bash_command="cat /app/mount/my_file_resource/my_file.conf"
	)

"""read_conf = BashOperator(
    	task_id="read_conf",
        dag=dag,
    	bash_command="cat /app/mount/my_file_resource/my_file.conf",
        xcom_push=True
	)

def _print_confs(**context):
    return context['ti'].xcom_pull(task_ids='read_conf')

apiresponse_step5 = PythonOperator(
    task_id="print_file_resource_confs",
    python_callable=_print_confs,
    dag=dag
)"""

start >> spark_sql >> read_conf #>> apiresponse_step5
