# Machine Learning Operations (MLOps) project
## About the project
The project implements a simple CI/CD pipeline for machine learning project. The machine learning task
is numerical integration on [-2, 2] using 5 equally spaced nodes: -2, -1, 0, 1, 2. Obviously,
the task can be solved using Boole's rule (5-Point Closed Newton-Cotes formula), which shows that
the solution is a sum of the values of the function at the nodes scaled by certain coefficients. t
Thus even simple linear regression can solve this problem finding the coefficients. This model is wrapped in
a simple Flask app, without any styling.
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
There are 2 pipeline: (Jenkinsfile and Jenkinsfile_train). The first one is a classical
CI/CD pipeline which builds a Docker image, tests if the Flask application runs successfully,
pushing the image to registry(private Docker registry or DockerHub) and runs the docker container 
with port 5000 exposed for Flask. <br><br>
The second pipeline is machine learning pipeline. It pulls the image pushed in the first pipeline,
then it trains several models on the new data(already provided in /app/model/data/) and using MLFlow,
it saves the hyperparameters and metrics, and the automatically takes the best model by performance. Afterward,
using pytest the performance of this model is checked. If it is above a certain threshold, the new Docker image ,
containing the new model is pushed to the registry and the whole application is run with port 5000 exposed for the
Flask application, port 8000 exposed for the MLFlow user interface.

