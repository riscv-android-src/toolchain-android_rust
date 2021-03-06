#
# Copyright (C) 2021 The Android Open Source Project
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
#
"""Constants and helper functions for hosts."""
import enum
import sys

@enum.unique
class Host(enum.Enum):
    """Enumeration of supported hosts."""
    Darwin = 'darwin'
    Linux = 'linux'
    Windows = 'windows'
    Android = 'android'

    @property
    def is_windows(self) -> bool:
        """Returns True if the given host is Windows."""
        return self == Host.Windows

    @property
    def is_darwin(self) -> bool:
        """Returns True if the given host is Darwin."""
        return self == Host.Darwin

    @property
    def is_linux(self) -> bool:
        """Returns True if the given host is Linux."""
        return self == Host.Linux

    @property
    def os_tag(self) -> str:
        """Returns the os tag of current Host."""
        return {
            Host.Darwin: 'darwin-x86',
            Host.Linux: 'linux-x86',
            Host.Windows: 'windows-x86',
        }[self]


@enum.unique
class Arch(enum.Enum):
    """Enumeration of supported arches."""
    ARM = 'arm'
    AARCH64 = 'aarch64'
    I386 = 'i386'
    X86_64 = 'x86_64'

    @property
    def llvm_arch(self) -> str:
        """Converts to llvm arch."""
        return {
            Arch.ARM: 'arm',
            Arch.AARCH64: 'aarch64',
            Arch.I386: 'i686',
            Arch.X86_64: 'x86_64',
        }[self]

    @property
    def llvm_triple(self) -> str:
        """Converts to llvm triple."""
        return f'{self.llvm_arch}-linux-android'

    @property
    def ndk_arch(self) -> str:
        """Converts to ndk arch."""
        return {
            Arch.ARM: 'arm',
            Arch.AARCH64: 'arm64',
            Arch.I386: 'x86',
            Arch.X86_64: 'x86_64',
        }[self]

    @property
    def ndk_triple(self) -> str:
        if self == Arch.ARM:
            return 'arm-linux-androideabi'
        return self.llvm_triple

def _get_default_host() -> Host:
    """Returns the Host matching the current machine."""
    if sys.platform.startswith('linux'):
        return Host.Linux
    if sys.platform.startswith('darwin'):
        return Host.Darwin
    if sys.platform.startswith('win'):
        return Host.Windows
    raise RuntimeError('Unsupported host: {}'.format(sys.platform))


_BUILD_OS_TYPE: Host = _get_default_host()


def build_host() -> Host:
    """Returns the cached Host matching the current machine."""
    global _BUILD_OS_TYPE  # pylint: disable=global-statement
    return _BUILD_OS_TYPE
