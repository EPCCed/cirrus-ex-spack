# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import datetime as dt
import os

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonExtension, PythonPipBuilder
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack_repo.builtin.packages.lammps.package import Lammps as BuiltinLammps
from spack.package import *

class Lammps(BuiltinLammps):
    
    patch('timer.patch', when='@20250612')