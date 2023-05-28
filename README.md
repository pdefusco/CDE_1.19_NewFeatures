# CDE 1.19 New Features

## Objective

CDE 1.19 has been introduced in May 2023 with the following enhancements and new features:

* Two Tiers of Virtual Clusters: Core and All-Purpose. Core clusters are dedicated to batch jobs. All-Purpose clusters include Interactive Sessions.
* Interactive sessions: introducing Spark Shell capabilities directly within the CDE Virtual Cluster.
* Spark 3.3 Support.  Now CDE supports 3 versions of Spark -- 2.4, 3.2, and 3.3. 3.2 will also serve as the LTS so customer can depend on it like they do on-premise.
* Support for Hong Kong & Jakarta workload regions.
* Airflow performance is now 2x faster from a combination of upgrade & continued optimizations.
* Support for File Resources with Airflow CDE Jobs: you can now mount extra files to Airflow jobs. This will be extended in the next release to support python packages.
* CDE CLI profiles: ability to set up multiple virtual clusters and keys and easily switch between them using the CLI.
* Spark-submit migration tooling: use the tool to migrate Datahub Spark jobs to CDE.

To learn more please visit the release notes at [this URL](https://docs.cloudera.com/data-engineering/cloud/release-notes/topics/cde-whats-new-1.19.html)

This repository showcases the following 1.19 capabilities:

* Interactive Sessions [link](https://github.com/pdefusco/CDE_1.19_NewFeatures#interactive-sessions)
* Using CDE Airflow Jobs with File Resources [link](https://github.com/pdefusco/CDE_1.19_NewFeatures#using-cde-airflow-jobs-with-file-resources)
* Spark Submit Migration Tool [link](https://github.com/pdefusco/CDE_1.19_NewFeatures#spark-submit-migration-tool)

## Requirements

You can reproduce these use cases in your CDE Virtual Cluster:

* CDE Version 1.19 in Private or Public Cloud (AWS, Azure, OCP and Cloudera ECS ok).
* Basic familiarity with Python, PySpark, Airflow and Docker.

## Project Setup

Clone this git repository to a local folder on your machine. All files and dependencies are included in this project.

## Interactive Sessions

## Using CDE Airflow Jobs with File Resources

## Spark Submit Migration Tool

## Conclusions & Next Steps

CDE is the Cloudera Data Engineering Service, a containerized managed service for Spark and Airflow. Each CDE virtual cluster includes an embedded instance of Apache Airflow.

With Airflow based pipelines users can now specify their data pipeline using a simple python configuration file.

A basic CDE Airflow DAG can be composed of a mix of hive and spark operators that automatically run jobs on CDP Data Warehouse (CDW) and CDE, respectively; with the underlying security and governance provided by SDX.

However, thanks to the flexibility of Airflow, CDE can also empower users with the ability to integrate with other CDP Data Services and 3rd party systems.
For example, you can combine the operators we have seen above to create complex pipeleines across multiple domains such as Datawarehousing, Machine Learning, and much more.

![alt text](img/airflow_guide_11.png)

If you are exploring CDE you may find the following tutorials relevant:

* [Using CDE Airflow](https://github.com/pdefusco/Using_CDE_Airflow): an deep dive into CDE Airflow Capabilities along with answers to FAQ's and Cloudera-recommended best practices.

* [Spark 3 & Iceberg](https://github.com/pdefusco/Spark3_Iceberg_CML): a quick intro of Time Travel Capabilities with Spark 3

* [Simple Intro to the CDE CLI](https://github.com/pdefusco/CDE_CLI_Simple): A simple introduction to the CDE CLI for the

* [CDE CLI Demo](https://github.com/pdefusco/CDE_CLI_demo): A more advanced CDE CLI reference with additional details for the CDE user who wants to move beyond the basics shown here.

* [GitLab2CDE](https://github.com/pdefusco/Gitlab2CDE): a CI/CD pipeline to orchestrate Cross Cluster Workflows - Hybrid/Multicloud Data Engineering

* [CML2CDE](https://github.com/pdefusco/CML2CDE): a CI/CD Pipeline to deploy Spark ETL at Scale with Python and the CDE API

* [Postman2CDE](https://github.com/pdefusco/Oozie2CDE_Migration): using the Postman API to bootstrap CDE Services

For more information on the Cloudera Data Platform and its form factors please visit [this site](https://docs.cloudera.com/).

For more information on migrating Spark jobs to CDE, please reference [this guide](https://docs.cloudera.com/cdp-private-cloud-upgrade/latest/cdppvc-data-migration-spark/topics/cdp-migration-spark-cdp-cde.html).

If you have any questions about CML or would like to see a demo, please reach out to your Cloudera Account Team or send a message [through this portal](https://www.cloudera.com/contact-sales.html) and we will be in contact with you soon.
