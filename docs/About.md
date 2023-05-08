# About this documentation

---

## Maintenance

---
This documentation is maintained by the IriusRisk engineering team. If you find an error, or need any 
clarification, please raise an issue in the 
[StartLeft GitHub repository](https://github.com/iriusrisk/startleft/issues).

## Documentation per branch

---
The documentation shown here applies to the 
[latest stable version of StartLeft](https://github.com/iriusrisk/startleft/releases). If you want to check the 
documentation of a previous version or for an ongoing development, you can do it by checking out the desired branch and 
deploying its documentation. To do that, first we need to select the right branch:

* `main` is the branch for the latest stable version.
* `release/{release-number}` (i.e: `release/1.7.0`) are the branches for each version.
* `dev` is the branch that contains the developments that will be delivered in the next version.
* `feature/{feature-number}` (i.e: `feature/600`) are the branches for specific developments.

So, suppose for example you want to check the documentation for the developments delivered in the next version. You 
will need to clone the `dev` branch:

```shell
git clone -b dev https://github.com/iriusrisk/startleft.git
```

And then launch the StartLeft documentation


## Launch StartLeft documentation by Dockerfile

Deploy the documentation using the provided `docker-compose.yml` file inside the `deployment` folder:

- With docker installed from debian/ubuntu packages (docker.io) and the docker-compose plugin
```shell
cd deployment
docker-compose up -d startleft-docs
```
- With docker installed from docker.com packages
```shell
cd deployment
docker compose up -d startleft-docs
```


Now you can access the docs in [http://localhost:8000](http://localhost:8000).

> :information_source: **_Launch by Dockerfile is recommended in case none modification will be done to the docs_**


## Launch StartLeft documentation by mkdocs serve
Run into StartLeft root folder
```shell
pip install -r docs/requirements.txt
mkdocs serve
```

Browse to [http://localhost:8000](http://localhost:8000) to access the documentation.

> :information_source: **_Launch by mkdocs serve is recommended if the docs will be modified, as the changes are 
> reloaded automatically_**