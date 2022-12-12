# Welcome to the StartLeft contributing guide
First off, thanks for taking the time to contribute!!

StartLeft is an Open Source project that welcomes collaborators to extend or improve its functionality. Despite
the fact that it was born as an internal [IriusRisk](https://iriusrisk.com) project, there are some characteristics
that make it especially suitable to grow through the contributions of the community:

* The nature of the project, whose functional scaling is based on the **support of new, independent, source
  formats**.
* The **conversion into the [Open Threat Model (OTM)](https://github.com/iriusrisk/OpenThreatModel) format is based on
  configuration files** that can also be created independently depending on the expected OTM use.
* The **modularized architecture** enables collaborators to contribute to each format's processor without conflicts.

## New contributor guide
The contributing strategy for StartLeft is based on standardized procedures for collaborating in GitHub Open Source
projects, so these resources may be helpful for you:

* [Finding ways to contribute to open source on GitHub](https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github).
* [Set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git).
* [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow).
* [Collaborating with pull requests](https://docs.github.com/en/github/collaborating-with-pull-requests).

## Getting started

All you need to know about StartLeft is on its [documentation page](http://iriusrisk.github.io/startleft). Once you
get familiarized with the project, you can check out the
[Quickstart Guide for Developers](http://iriusrisk.github.io/startleft/development/Quickstart-Guide-for-Developers/),
which will guide you through the process of setting up the development environment as well as providing you with all
the basics to start coding.

### Issues
If you spot a problem with StartLeft, [search if an issue already exists](https://github.com/iriusrisk/startleft/issues).
If a related issue does not exist, you can open a new issue.

### Enhancements
To propose improvements or changes that are not properly bugs or problems you can also use the
[issues section](https://github.com/iriusrisk/startleft/issues). In this case, please try to be as clear as you can
and include in your issue:
* The **context** of the issue. Does it apply to the CLI? To the API? Is it an improvement for a specific SLP?
* The **motivation** of the proposal. How will the proposed change improve StartLeft?
* The **goal** of the issue. What is exactly the change that should be implemented?

### Make changes
In order to use the best approach for integration with external developers (also applicable to any contributor), the
[GitHub guide for contributing to projects](https://docs.github.com/en/get-started/quickstart/contributing-to-projects)
will be used. Summarizing, the steps that an external developer must follow to contribute are:

1. [Fork the StartLeft repository](https://github.com/iriusrisk/startleft/fork).
2. Implement your changes in your forked repository.
3. Create a Pull Request (PR) from the forked branch to the StartLeft `dev` branch in the main
   repository describing the changes done and their motivations.
4. The PR will be reviewed by the owners' team using the
   [GitHub strategy](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request).
   for async communication.
5. Once approved, the PR will be merged in the `dev` branch of the StartLeft repository and delivered in the next
   release.

## Code conventions
There are no specific code conventions for the StartLeft project. At this point, the generic
[Style Guide for Python Code](https://peps.python.org/pep-0008/) is followed. So, please take a look at it before
starting coding, paying special attention to the
[naming conventions](https://peps.python.org/pep-0008/#naming-conventions). Anyway, if some doubt arises in a PR, it
can be discussed to get aligned.


## Useful links
* <a href="http://iriusrisk.github.io/startleft" target="_blank">StartLeft documentation</a>.
* <a href="https://github.com/iriusrisk/startleft/issues" target="_blank">Open issues</a>.
* <a href="https://github.com/iriusrisk/startleft/releases" target="_blank">Releases</a>.
* <a href="https://github.com/iriusrisk/OpenThreatModel" target="_blank">Open Threat Model (OTM) standard definition</a>.
* <a href="https://www.threatmodelingconnect.com/" target="_blank">Threat Modeling connect forum</a>.
