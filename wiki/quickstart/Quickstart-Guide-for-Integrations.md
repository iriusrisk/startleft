# Quickstart Guide for Integrations

The final goal of StartLeft is being integrated within processes that requires the generation of a Threat Model. Examples
of this are:
* A CI/CD pipeline for modifications in IaC files.
* A process for creating standardized Threat Models from infrastructure diagrams.
* A process for migrating Threat Models from one threat modelling tool to another.

The more common scenario for these use cases is that they are automatized. For that, it is necessary that Startleft can
be used by another services or applications in a smoothy way. The different ways of doing this are explained along this page.

## As a service
This type of integration fits specially well when we need to integrate StartLeft with some application that requires 
OTM conversion features. For instance, [IriusRisk](https://www.iriusrisk.com/) provides importing endpoints for different
sources that internally rely on a StartLeft service for generating an OTM as a common intermediate state:

![iriusrisk-integration](images/iriusrisk-integration.png)

Notice that StartLeft is a stateless service. Neither does it require authentication nor authorization since it does not
access or stores personal information nor access other services. For this reason, the service is quite simple to deploy and
operate.

### Deploy locally
If you only want to experiment with the API, this is probably the simplest way. For that, you need to have
StartLeft installed in your machine like explained in the [Quickstart Guide for Beginners](Quickstart-Guide-for-Beginners.md)
and execute the command:
```shell
startleft server
```
**The server is started by default in the port 5000**, but you can configure it with the `--port`/`-p` modifier.
```shell
startleft server --port 8080
```
Once you have your service started, you can check the API documentation in [http://localhost:5000/docs](http://localhost:5000/docs).

### Deploy dockerized
This is the more logical option for integration purposes, since it enables the service to be portable to any infrastructure.
In the same StartLeft repository a ready-to-use Dockerfile is provided, so you already have what you need to set up your 
dockerized service.

For trying it, let's first create a folder for the docker resources:
```shell
mkdir startleft-docker
cd startleft-docker
```

And download the Dockerfile:
```shell
wget https://raw.githubusercontent.com/iriusrisk/startleft/main/Dockerfile
```

Now, we can create the startleft image:
```shell
docker build . -t startleft
```

And, finally, we can run the docker container for the image we have just generated. Notice that you can select the
port where the service is exposed in a standard Docker way.
```shell
docker run -p 5000:5000 startleft
```

If everything works, you should see a log like this:
```shell
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```

As in the local deployment, we can check that the service documentation is successfully in 
[http://localhost:5000/docs](http://localhost:5000/docs).

Another way to verify the availability of the service is performing a request to the health endpoint, what can be done
through a curl command like:
```shell
curl localhost:5000/health
```
This command should return:
```json
{
  "status": "OK",
  "version": "development-version",
  "components": {
    "StartLeft": "OK"
  }
}
```
For more details about how to use the StartLeft API, you can check the [REST API page](../REST-API.md).

#### Custom Dockerfile
The Dockerfile provided should be enough for the most common integration scenarios, but, of course, it is possible to
create a custom docker image for StartLeft. For that, you can take the existent 
[Dockerfile](https://raw.githubusercontent.com/iriusrisk/startleft/main/Dockerfile) available in the root of the StartLeft
repository as a base. However, you must bear in mind the following considerations:
* Every [official python image from the Docker Hub](https://hub.docker.com/_/python) for versions over 3.6 should work, but
  you should know:
  * Depending on the base image, you may need to install additional libraries.
  * Alpine-based images may be significantly slower than others at building time.
  * Some official python images may be detected as vulnerable by container analyzing tools.
* Despite you could set as the entrypoint the `startleft server` command, it is more recommendable to just use the uvicorn 
  command, that also allows you to select the default deployment port:
```
ENTRYPOINT ["uvicorn", "startleft.startleft.api.fastapi_server:webapp", "--host", "0.0.0.0", "--port", "5000"]
```

## In batch processes
The [Command Line Interface](../Command-Line-Interface.md) enables the users to easily create scripts for converting from different sources to OTM in batch, but
also to perform other operations like validating files. For doing that, you simply need to install startleft on your machine or 
creating a StartLeft docker image able to read the scripts you want to process.

Regarding the different functionalities available through the CLI and the REST API, it is important to consider that they does
not have necessarily to match. For example, OTM or mappings validations are available through the `validate` command, but 
there are no REST endpoint for them. On the other hand, not all the formats can be converted into OTM through the `parse` CLI
command, but all of them are supported in the REST API. These inconsistencies are expected to be solved in a short/medium
term with a small impact, since the transformation logic and the access interfaces are already decoupled. Thus, if you have
special interest in having some feature available through some interface, please raise an issue or create a fork following the
[Quickstart guide for developers](Quickstart-Guide-for-Developers.md).


## As a library (Future)
This is an interesting feature that is on the roadmap of StartLeft, but **that is not still available**.Even though an 
advanced user could manage to install and use startleft as a library, it is not recommendable because probably some related
changes (like modules' visibility) will be done that could break retro compatibility.

In addition, as you can see in the [Architecture section](../Architecture.md), StartLeft is a modularized application. Some
of the StartLeft's modules are likely to be extracted as a libraries. Specially remarkable is the case of the `otm` module, that is 
expected to become in the "official" python library for the [OTM](Open-Threat-Model-(OTM).md) standard, providing generic 
functionalities related to OTM.
