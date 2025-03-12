

## Ollama - Build a ChatBot with Langchain, Ollama & Deploy on Docker

### get ollama image and run the container for further usage

1. pull ollama docker image
command = docker pull ollama/ollama  

2. Run ollama container in docker (useful for microservice applications)
command = docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
------This command starts a container based on the Ollama image and maps port 11434 on your local machine to port 11434 inside the container. The -it flag attaches an interactive terminal to the container.


The command you provided is a Docker command to run a container based on the ollama/ollama image. Let's break down the command:

docker run: This command is used to run a Docker container.
-d: This flag runs the container in detached mode, meaning it runs in the background.
-v ollama:/root/.ollama: This flag mounts a Docker volume named ollama to the container's /root/.ollama directory. This allows persistent storage for the container.
-p 11434:11434: This flag maps port 11434 on the host to port 11434 in the container. This allows accessing the service running inside the container via port 11434 on the host machine.
--name ollama: This flag assigns the name ollama to the container.
ollama/ollama: This is the name of the Docker image used to create the container.
So, when you run this command, Docker will start a container named ollama based on the ollama/ollama image, with persistent storage mounted at /root/.ollama, and accessible on port 11434 of the host machine.

3. Run llama2 model locally
command = docker exec -it ollama ollama run llama2
------This Docker command executes a command inside a running container named "ollama" with the options -it. 
The command being executed inside the container is "ollama run llama2". It interacts with the container's standard input/output and runs a program or script called "llama2" within the "ollama" container.

command = docker exec -it ollama
------- Repeating : This Docker command executes a command inside a running container named "ollama" with the options -it. 

4. We should be able to check, if ollama is running by calling http://localhost:11434


### Basic Ollama Comamnds:

ollama pull — This command is used to pull a model from the Ollama model hub.
ollama rm — This command is used to remove the already downloaded model from the local computer.
ollama cp — This command is used to make a copy of the model.
ollama list — This command is used to see the list of downloaded models.
ollama run — This command is used to run a model, If the model is not already downloaded, it will pull the model and serve it.
ollama serve — This command is used to start the server, to serve the downloaded models.


------------------------------------------------------------------------------------




FROM python: 3.10

# Create app directory
WORKDIR /app

# Copy the files
COPY requirements.txt ./
COPY app.py ./

#install the dependecies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

---------------------------------------------------------------------------------------

------ We are using the python docker image, as the base image, and creating a working directory called /app. 
We are then copying our application files there, and running the pip installs to install all the dependencies.
We are then exposing the port 8501 and starting the streamlit application.



-------------------
use docker commands

docker images: list all images
docker container ls: list all containers
docker container ps: list all running containers
docker image rm image_name: removes image_name image
docker stop container_name: stops a container, but does not removed its orphaned volumes
docker rm container_name : remove a stopped container_name
docker container prune: This will remove all stopped containers and should work on all platforms the same way.
docker system prune: clean up all unused containers, networks, images (both dangling and unreferenced), and optionally, volumes, in one command.



DOCKERIZE AN APP
1. Docker requires the project folder name to be completely in lowercase letters and underscores. It is important to ensure the name is in lowercase before building the app in the next step.
2.  Build a Docker image for the NER app with the command:

command: docker build -f Dockerfile -t appname .

The -f flag is used to specify the name of the Dockerfile to be used for building the image
The -t flag is used to name and/or tag the image. In this case, we are tagging the Docker image with the ‘latest’ tag 
The dot at the end is necessary. It indicates that Docker should use files from the current directory to build the image.

3. Run the application from the Docker container by entering the following command into the CLI:

command: docker run -p 8501:8501 appname

The -p flag is used to map the container’s port to the host port i.e. port 8501. 
Streamlit works best on port 8501 specifically.
