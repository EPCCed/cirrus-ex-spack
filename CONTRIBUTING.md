# Contributing to the centrally installed software

This is a guide for contributing to the centrally installed spack installation, including configuration changes and changes to the cse environment.
In order to make any change you will need to create a pull request and the pull request will have to be reviewed by a member of the cse team.

## Making a change

- Clone the `develop` branch of this repository, as described in the main Readme file.
- Make sure to use the included spack installation. This repository contains a script to generate the required modules. See the main Readme file for instructions.

### Adding a spec to the cse environment

- Activate the `environments/cirrus-ex-cse` environment with `spack env activate environments/cirrus-ex-cse`.
- Add specs to the environment in `environments/cirrus-ex-cse/spack.yaml` file. Alternatively, you can use the command `spack add <my_spec>`.
- Always specify the compiler or use one of the available toolchains (`gcc_all`,`cce_all`,`intel_all`) .
- Concretize the new spec with `spack concretize`. This command should output a concretized spec. Try to avoid mixing different compilers, as they can cause issues when generating modules for the spec. Adding the `-U` flag to the concretize command can help avoiding mixing compiler dependencies. Do not force re-concretization ( i.e. using the `-f` flag ), as this will change specs that are already installed in the environment.
- Install the spec using `spack install <spec>` and check that the build works.
- Generate the modules. By default apps and libraries will only be visible when the programming environment matches the LMod compiler for the spec. This is usually the correct behavior for libraries. For apps you might want the application to always be available. If that is the case, add the spec to `core_specs`. You can generate the modules using `spack module lmod refresh`.
- Test the application/library works when using the generated modules. Ideally, add a test in Reframe.
- Commit all changes and submit a pull request to this repo. Make sure to include the `spack.lock` file. This is to ensure the same exact concretized specs will be installed by the reviewer or when deploying the main system.


## Licensed packages

- When adding packages with a license, follow the same process as for any specs
- Additionally , make sure the permissions for packages are set correctly ( see the main README file ). Also make sure that the `cse-cirrus-ex` user is added to the package group.
- Make sure the only copy for the source code is in the `licensed_packages` mirror and the permission of the mirror folder only allow the `cse-cirrus-ex` user to read and write to the mirror. ( see the main README file for more detailed instructions )

## Reviewing

Each pull request should be reviewed by a member of the cse team.

- Pull the changes locally .
- Activate the `cirrus-ex-cse` environment and run `spack concretize`. Spack should return a message specifying that no specs needed to be concretized. If not, the `spack.lock` file in the pull request was probably out of date. 
- Test that the above procedure was followed. In particular you should be able to generate modules and test the change ( including any new software installed as part of the stack ).

## Deploying

When deploying new software, this should be made through the central installation.

- Pull from the repository the relevant branch and activate the environment.
- Run `spack concretize` to check that no new specs will be concretized
- Run `spack install` to build the new software
- Generate the modules usng `spack module lmod refresh`. This command will generate new modules, but will not overwrite/delete existing modules. If a module needs to be deleted or overwritten, this should be removed manually first and then the modules be refreshed. The `--delete-tree -y` flag should be avoided, as it will attempt to remove all the modules and re-create them. This could cause running jobs to fail and intermittent issues for users.
 
## A user cannot install a specific package.

The repository `repos/cirrus-ex-cse` contains custom packages, which can override the default ones. This is useful to fix packages which do not build with spack out of the box on `cirrus-ex`.
If a user cannot build a package, the cse team can create or modify a package. This should be contributed to this repo through a pull request. As the deployment might not happen immediately, the cse team can share the custom repo with the user. The user can then use the new package by

```bash
spack repo add <my_custom_repo>
spack install <my_spec>
```

## Release cycles

We aim to deploy changes at regular intervals ( i.e. every 6 months ), but not continuously unless an emergency occurs.
At regular intervals, we would:

- Generate a release on the github repo. The verson of the `cse_env` and spack config would then be bumped and deployed in a new folder.
- The `cirrus-ex` environment is generated from scratch , software installed and modules generated. This could also be a good time for re-concretizing the environment.
- Generate modules for both `spack` and `cse_env` and test them as described in the sections above.
- Additionally run reframe tests against the new modules and check that all tests pass.