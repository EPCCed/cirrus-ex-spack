# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import re
import sys

from spack_repo.builtin.packages.cmake.package import Cmake as BuiltinCmake

from spack.package import *


class Cmake(BuiltinCmake):
    """A cross-platform, open-source build system. CMake is a family of
    tools designed to build, test and package software.
    """
    
    version(
        "4.1.2",
        sha256="643f04182b7ba323ab31f526f785134fb79cba3188a852206ef0473fee282a15")
    