# Copyright (C) 2019 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Provides path expansion to components needed for the rustc build."""

import os.path
import build_platform

THIS_DIR = os.path.realpath(os.path.dirname(__file__))

STAGE0_RUST_VERSION = '1.51.0'
CLANG_REVISION = 'r416183b1'

def workspace_path(*args):
    """Generates a path relative to the root of the workspace."""
    return os.path.realpath(os.path.join(THIS_DIR, '..', '..', *args))


def rustc_path(*args):
    """Generates a path relative to the rustc source directory."""
    return os.path.realpath(os.path.join(THIS_DIR, '..', 'rustc', *args))


def patches_path(*args):
    """Generates a path relative to the patches directory."""
    return os.path.realpath(os.path.join(THIS_DIR, 'patches', *args))


def this_path(*args):
    """Generates a path relative to this directory."""
    return os.path.realpath(os.path.join(THIS_DIR, *args))


def out_path(*args):
    """Generates a path relative to the output directory of the build."""
    return workspace_path('out', *args)

def stdlib_srcs(*args):
    """Generates a path relative to the directory to install stdlib sources."""
    return out_path('src', 'stdlibs', *args)

def rust_prebuilt(*args):
    """Generates a path relative to the rust prebuilt directory."""
    return workspace_path('prebuilts', 'rust', build_platform.prebuilt(),
                          STAGE0_RUST_VERSION, *args)

def clang_name():
    """Returns the versioned clang directory name."""
    return 'clang-{0}'.format(CLANG_REVISION)

def llvm_prebuilt(*args):
    """Generates a path relative to the LLVM prebuilt directory."""
    return workspace_path('prebuilts', 'clang', 'host',
                          build_platform.prebuilt(), clang_name(), *args)

def cxx_linker_path(*args):
    """Generates an absolute path relative to the LLVM C++ runtime"""
    return llvm_prebuilt('lib64', *args)

def android_cxx_linker_path(*args):
    """Generates a relative path to the LLVM C++ in the Android tree"""
    # We live at      prebuilts/rust/${BUILD_PLATFORM}/${VERSION}/bin
    # libc++ lives at prebuilts/clang/host/${BUILD_PLATFORM}
    #                 /clang-${CLANG_REVISION}/lib64
    return os.path.join('..', '..', '..', '..', 'clang', 'host',
                        build_platform.prebuilt(), clang_name(), 'lib64',
                        *args)

def cmake_prebuilt(*args):
    """Generates a path relative to the Cmake prebuilt directory."""
    return workspace_path('prebuilts', 'cmake', build_platform.prebuilt(),
                          *args)


def ninja_prebuilt(*args):
    """Generates a path relative to the Ninja prebuilt directory."""
    return workspace_path('prebuilts', 'ninja', build_platform.prebuilt(),
                          *args)



def build_tools_prebuilt(*args):
    """Generates a path relative to the build-tools prebuilt directory."""
    return workspace_path('prebuilts', 'build-tools', 'path',
                          build_platform.prebuilt(), *args)


def curl_prebuilt(*args):
    """Generates a path relative to the curl prebuilt directory."""
    return workspace_path('prebuilts', 'android-emulator-build', 'curl',
                          build_platform.prebuilt_full(), *args)


def ndk(*args):
    """Generates a path relative to the prebuilt NDK.

    Use of the NDK should eventually be removed so as to make this a Platform
    target, but is used for now as a transition stage.
    """
    return workspace_path('toolchain', 'prebuilts', 'ndk', 'r20', *args)


def extract_arch(target):
    """Extracts from a target the android-style arch"""
    canon_arch = target.split('-')[0]
    if canon_arch == 'aarch64':
        return 'arm64'
    if canon_arch == 'armv7':
        return 'arm'
    if canon_arch == 'i686':
        return 'x86'
    if canon_arch == 'riscv64':
        return 'riscv64'
    return canon_arch


def normalize_target(target):
    """Translates triples into their general form."""
    if target == 'armv7-linux-androideabi':
        return 'arm-linux-androideabi'
    return target


def ndk_sysroot(*args):
    """Generates a path relative to the NDK sysroot."""
    return ndk('sysroot', *args)


def sys_includes(*args):
    """Generates a path relative to the NDK sysroot include dir."""
    return ndk_sysroot('usr', 'include', *args)


def target_includes(target, *args):
    """Generates a path relative to the target-specific NDK include dir."""
    return sys_includes(normalize_target(target), *args)


def ndk_llvm(*args):
    """Generates a path relative to the NDK prebuilt for LLVM objects"""
    return ndk('toolchains', 'llvm', 'prebuilt', 'linux-x86_64', *args)


def plat_ndk_llvm_libs(target, *args):
    """Generates a path relative to the target's LLVM NDK sysroot libs"""
    return ndk_llvm('sysroot', 'usr', 'lib', normalize_target(target), *args)


def plat_ndk_sysroot(target, *args):
    """Generates a path relative to the NDK platform-specific sysroot.

    This sysroot is incomplete, and contains only the object files, not the
    headers. However, the primary sysroot has the object files behind an
    additional level of indirection for the API level which platform clang
    does not look through.
    """
    return ndk('platforms', 'android-29', 'arch-' + extract_arch(target),
               *args)


def gcc_libdir(target, *args):
    """Locates the directory with the gcc library target prebuilts."""
    return ndk_llvm('lib', 'gcc', normalize_target(target), '4.9.x', *args)
