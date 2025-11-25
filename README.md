# Spack

These repo contains configurations for the centrally installed version of spack.
The configuration is set using environment variables. The user can easily override these configurations to a custom directory.

The cirrus repo folder contains patches for broken or non-existent packages on cirrus.

## Using spack

### Loading spack

```bash
module load spack/1.0.2
```

### Useful commands

- `spack find`:  view installed packages. See `spack find -h` for options.
- `spack install ${SPEC}` : to install a specifick package name.
- `spack compilers` : show availabe compilers
- `spack list ` : shows all packages available in the repository

## Installing Spack

Navigate to the folder where you wish to install spack and clone this folder, including submodules.

```bash
git clone --recursive -b develop https://github.com/lucaparisi91/cirrus-ex-spack.git
```
You can generate module files to load spack using

```bash
module load cray-python
python scripts/generate_modules.py $SPACK_VERSION --output $MODULES_ROOT/spack
```

## Installing the CSE environment

This is an environment we can use to provide centrlly installed packages.
You can install the environment wih

```bash
spack -d -e environments/cirrus-ex-cse install -vvvv
```
If installing from fresh, this might take a long time.

Finally generate environment modules with

```bash
spack -e environments/cirrus-ex-cse module lmod refresh --delete-tree -y
```

To unlock the modules created, you can generate a module that activates the environment modules.

```bash
python scripts/generate_modules.py $VERSION_CSE_ENV --module=cse_env --output $MODULES_ROOT/cse_env
```

To use the spack generated modules load the `cse_env` module

```bash
module load cse_env
```

You will be able to see all the packages compatible with your current programming environment. To view packages supported only for a certain compiler, load the corresponding cray programming environment or use the `module spider <package_name>` command. 


## Licensed packages

Source code of licenced packages can be set in a mirror in `cirrus-ex-cse/licensed_packages` . This directory should only accessible for the cse user.

```bash
spack -e environments/cirrus-ex-cse/ mirror  create -d  ../../cirrus-ex-cse/licensed_packages <my-package-name>
spack -e environments/cirrus-ex-cse/ install -vvv <my-package-name>
```

The first time you install a package, the source code needs to be present in your current folder. For subsequent installations, the source will be fetched from the mirror.
Once the package has been added to the mirror, it needs to be added to the environment, as described in the section above.
However, make sure to set the permissions in the `packages` section of the `spack.yaml` environment are set appropriatly.

## Build cache

Spack defaults to installing all packages from source. As this requires re-compiling, this can take a long time and/or require a large amount of memory.
This can be sped up by setting a re-usable build cache of commonly used packages.
An environment containg specs we want to cache is contained in the `cirrus-ex-cse-cache` environment.
In order to add packages to the cache run

```bash
spack -e environments/cirrus-ex-cse-cache/ install # install specs defined in the environment
spack -e environments/cirrus-ex-cse-cache/ buildcache push --only=package cache # Save defined specs in the build cache
spack -e environments/cirrus-ex-cse-cache/ buildcache push --only=dependencies cache # Save dependencies in the build cache
spack -e environments/cirrus-ex-cse-cache/ buildcache update-index cache # Update the cache index, so that the cached build can be found when a cirrus-ex user installs the same package in their own environment
```

