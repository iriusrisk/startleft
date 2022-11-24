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
will need to clone the `dev branch:

```shell
git clone -b dev https://github.com/iriusrisk/startleft.git
```

And then deploy the documentation using the provided `docker-compose` file inside the `deployment` folder:
```shell
cd deployment

docker-compose up -d docs
```

Now you can access the docs for the dev branch in [http://localhost:8000](http://localhost:8000).

