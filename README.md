# Machine Learning Operations (MLOps) project
## About the project
The project implements a simple CI/CD pipeline for machine learning projects. 
The machine learning task is numerical integration on [-2, 2] using 5 equally 
spaced nodes: -2, -1, 0, 1, 2. The task can be solved using Boole's rule 
(5-Point Closed Newton-Cotes formula), which shows that the solution is a sum 
of the values of the function at the nodes scaled by certain coefficients. 
Thus even simple linear regression can solve this problem by finding the coefficients. 
This model is wrapped in a simple Flask app, without any styling.
## Frameworks and services used:
* GitHub
* AWS
* Jenkins
* Docker
* Flask
* sklearn
* pandas
* MLFlow
## Pipeline
There are 2 pipelines: (Jenkinsfile and Jenkinsfile_train). The first one is a classical
CI/CD pipeline which builds a Docker image, tests if the Flask application runs 
successfully, pushes the image to the registry(private Docker registry or DockerHub), 
and runs the Docker container with port 5000 exposed for Flask. <br><br>
The second pipeline is the machine learning pipeline. It pulls the image pushed 
in the first pipeline, then it trains several models on the new data(already provided 
in /app/model/data/), and using MLFlow, it saves the hyperparameters and metrics, and 
automatically takes the best model by performance. Afterward, using pytest the performance
of this model is checked. If it is above a certain threshold, the new Docker image, 
containing the new model is pushed to the registry, and the whole application is run
with port 5000 exposed for the Flask application, and port 8000 exposed for the MLFlow
user interface.

