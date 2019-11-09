#!/usr/bin/env python3
'''Host side actions for building clang-format wheels'''
import argparse
import collections
import contextlib
import os
import shutil
import subprocess


CORES = os.environ.get('CORES', 2)  # number of cores in container
DOCKER_IMAGE = 'quay.io/pypa/manylinux1_x86_64'
MOUNT_POINT = '/io'

# different llvm/clang versions are distributed from different locations:
BASE_URLS = {'github': 'https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/',
             'llvm': 'http://releases.llvm.org/{version}/',
             }

# using the 9.x version of clang-format-diff.py as it's python3 compatible
CLANG_FORMAT_DIFF_URL = ('https://raw.githubusercontent.com/llvm/llvm-project/'
                         'release/9.x/clang/tools/clang-format/clang-format-diff.py')

V = collections.namedtuple('V', 'version, source, cmake_flags')
VERSIONS = (V('6.0.1', 'llvm', ''),
            V('7.1.0', 'github', '-DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=true'),
            V('8.0.1', 'github', '-DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=true'),
            V('9.0.0', 'llvm', '-DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=true'),
            )

VERSIONS = {v.version: v for v in VERSIONS}


@contextlib.contextmanager
def cd(path):
    '''change to `path`'''
    curdir = os.path.abspath(os.curdir)
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(curdir)


def create_llvm_build_script(version, src_dir, script_dir):
    '''create the build script in `script_dir` for clang-format `version`

    Note:
        not using a template engine to reduce dependencies
    '''
    with open('build_clang.template') as fd:
        build_clang = fd.read()

    path = os.path.join(script_dir,
                        'build_{version}.sh'.format(version=version.version))
    with open(path, 'w') as fd:
        fd.write(build_clang.format(version=version.version,
                                    cmake_flags=version.cmake_flags,
                                    cores=CORES,
                                    src_dir=src_dir))


def download(url):
    '''download `url`

    Note:
        shelling out and using wget instead of using requests to reduce dependencies
    '''
    if not os.path.exists(os.path.basename(url)):
        subprocess.check_call(['wget', url, ])


def extract(path):
    '''decompress `path`'''
    if path.endswith('.xz'):
        flags = 'xfJ'
    elif path.endswith('.gz'):
        flags = 'xfz'
    else:
        raise Exception('Could not decompress %s' % path)

    subprocess.check_call(['tar', flags, path])


def download_and_extract(version, src_dir, script_dir):
    '''download `version` of source for llvm & clang, extract to correct directory'''
    assert version.source in BASE_URLS, 'Only known sources are %s' % list(BASE_URLS)
    base_url = BASE_URLS[version.source]

    with cd(src_dir):
        url = os.path.join(base_url, 'llvm-{version}.src.tar.xz').format(version=version.version)
        download(url)
        extract(os.path.basename(url))

        url = os.path.join(base_url, 'cfe-{version}.src.tar.xz').format(version=version.version)
        download(url)
        extract(os.path.basename(url))

        shutil.move('cfe-{version}.src'.format(version=version.version),
                    'llvm-{version}.src/tools/clang'.format(version=version.version))

        clang_format_diff_path = os.path.basename(CLANG_FORMAT_DIFF_URL)
        if not os.path.exists(clang_format_diff_path):
            download(CLANG_FORMAT_DIFF_URL)

        shutil.copy(clang_format_diff_path,
                    'llvm-{version}.src/tools/clang'.format(version=version.version))

    create_llvm_build_script(version, src_dir, script_dir)


def download_and_extract_cmake(src_dir, script_dir):
    url = 'https://cmake.org/files/v3.12/cmake-3.12.0.tar.gz'
    with cd(src_dir):
        download(url)
        extract(os.path.basename(url))

    build_script = '''
(cd {mount_point}/{src_dir}/cmake-3.12.0 \\
    && ./configure --parallel={cores} \\
    && gmake -j{cores} install \\
    )
    '''.format(src_dir=src_dir, cores=CORES, mount_point=MOUNT_POINT)
    with open(os.path.join(script_dir, '0-build_cmake.sh'), 'w') as fd:
        fd.write(build_script)


def run_docker(script_dir):
    '''launches docker, which then runs all the scripts in the `script_dir`, alphabetically'''
    subprocess.check_call(['docker', 'pull', DOCKER_IMAGE, ])
    subprocess.check_call(['docker', 'images', ])

    subprocess.check_call(
        ['docker', 'run', '--rm',
         '-v', '{pwd}:{mount_point}'.format(pwd=os.path.abspath(os.curdir),
                                            mount_point=MOUNT_POINT),
         DOCKER_IMAGE,
         'sh', '-c',
         'for i in $(ls -1 {mount_point}/{script_dir}/*.sh); do sh $i; done'.format(
             mount_point=MOUNT_POINT,
             script_dir=script_dir),
         ])

def get_parser():
    '''return the argument parser'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--script-dir', default='scripts',
                        help='location of script dir')
    parser.add_argument('--src-dir', default='src',
                        help='location of source directory')
    parser.add_argument('versions', nargs='+',
                        help='versions to build: %s' % list(VERSIONS))
    return parser


def main(args):
    '''main'''
    script_dir, src_dir = args.script_dir, args.src_dir

    os.makedirs(script_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)

    download_and_extract_cmake(src_dir, script_dir)

    versions = args.versions
    if args.versions[0] == 'all':
        versions = VERSIONS

    for version in versions:
        version = VERSIONS[version]
        download_and_extract(version, src_dir, script_dir)
        create_llvm_build_script(version, src_dir, script_dir)
    run_docker(script_dir)


if __name__ == '__main__':
    PARSER = get_parser()
    main(PARSER.parse_args())
