### RTS Labs - ETL Challenge

#### Description

This repository contains code to set up and run an airflow instance using docker on a single host. The environment is close to the offical docker compose configuration.

There is a single DAG contained within the project to pull data from the 'user' API, normalize it and convert it to a python dataframe and push it to a database on the postgres container specified in the compose file.

On first run, the postgres container will initialize a staging database called 'grover'. To run the DAG, this connection must be added to airflow with the postgres connection id 'stage_db'.

#### Details

Functions provided for API queries are contained within the user_etl dag, which is set up as a python module. user_etl.user_sync provides synchronous functions for API access:

- `call_api` queries the API, allowing one to pass the API size parameter as a function argument. The api will accept up to size 100, returning data as a json array. If only a single user is queried, the resulting python dictionary will be appended to an empty list, so as to maintain type integrity.

- `call_api_single` queries the api without the size parameter; instead the function argument defines the size of a range value, used in a for loop to query the api one user at a time however many times is necessary. This function provides an optional `wait` parameter, that uses the python time.sleep() method to overcome issues with request speed if necessary.

- `flatten_df` uses the pandas json_normalize method to flatten and convert the nested json/dict response to a tabular dataframe. This functional also labels the data with a pulled datetime for future reference or deduplication.

user_etl.user_async provides an asynchronous function to make single api calls to the users endpoint in parallel; however, this is not implemented in the DAG as rate limiting makes it nonfunctional.

The DAG imports the relevant above functions, pulling the api data and converting the response to a pandas dataframe. Finally, a connection is established to the stage database using an airflow postgres hook, and the resulting dataframe is pushed to the database.

#### Future Considerations and Limitations

- Error and exception handling would be necessary for a real world use case. For this project, handling and alerting the user about the rate limiting enforced by the API would be useful in particular.

- With data this simple, a complex data model is unnecessary; all the required data can be simply stored in a single table. In the real world, this data would likely be pulled in combination with other sources, facts and dimensions. Handling this in a robust manner would require modeling all aspects of the data in a way that is maintainable, performant and reflective of the business needs.

- Finally, pulling data into our airflow instance, holding it in memory as a dataframe and pushing it to a database is far from an ideal situation. In the real world, one would leverage connections to cloud or on prem storage/db solutions, leaving airflow to do what it does best - orchestrate.
