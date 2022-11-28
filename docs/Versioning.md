# Versioning

---
> **Note**: All StartLeft versions and their release notes can be found [here](https://github.com/iriusrisk/startleft/releases).

StartLeft uses [Semantic Versioning](https://semver.org/) as versioning strategy. To summarize, the version is 
composed by three parts following this format:

`{major}.{minor}.{patch}` (i.e.: `1.5.0`)

Where:

* The `{major}` part changes when there is a retro-compatibility breaking change.
* The `{minor}` part changes with each new release of the application.
* The `{patch}` part changes when a hotfix is delivered over the current release of the application.

## Versions management

---
StartLeft versions are managed through git tags. For each release, [a new tag for that version is created along with 
its release notes](https://github.com/iriusrisk/startleft/releases). During the installation, the latest version tag from 
the current branch is retrieved. Thus, if you query the version through the CLI command or the REST API endpoint, 
you will know what is the version of the StartLeft's code that is being executing.

???+ "Versions table"

    There are different types of branches in the StartLeft repository that correspond to different stages of the 
    software life cycle. If we suppose that the current version is `1.5.0`, that is, the last tag in the 
    [release page](https://github.com/iriusrisk/startleft/releases) is `1.5.0`, we should expect to get the following 
    version for each branch type:
    
    | branch          | description                                     | expected version example |
    |-----------------|-------------------------------------------------|--------------------------|
    | `main`          | Latest stable version                           | `1.5.0`                  |
    | `hotfix/*`      | Urgent fixes over main version                  | `1.5.1.dev1+ge7812ca`    |
    | `release/1.6.0` | Specific version                                | `1.6.0rc1`               |
    | `bugfix/*`      | Fixes during a release process                  | `1.6.0rc1.dev1+g6cda015` |
    | `dev`           | Features under development for the next version | `1.7.0.dev19+g17d9f68`   |
    | `feature/*`     | Specific developmnet ongoing                    | `1.7.0.dev3+g52d796a`    |

## Getting the installed version

---
Once you have [StartLeft installed](Quickstart-Guide-for-Beginners.md), there are two ways of getting the version of 
StartLeft you are executing.

Through the CLI it is as simple as executing the command:

```shell
startleft --version
```

The REST API also exposes an endpoint for retrieving the version that can be invoked with this cURL command:
```shell
curl http://localhost:5000/health
```