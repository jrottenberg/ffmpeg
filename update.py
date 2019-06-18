#! /usr/bin/env python

from string import Template
import sys
<<<<<<< HEAD
import re
import urllib
from distutils.version import StrictVersion

MIN_VERSION = '2.8'
VARIANTS = ['ubuntu', 'alpine', 'centos', 'scratch', 'vaapi', 'nvidia']
FFMPEG_RELEASES = 'https://ffmpeg.org/releases/'

travis = []
azure = []
response = urllib2.urlopen(FFMPEG_RELEASES)
ffmpeg_releases = response.read()

parse_re = re.compile('ffmpeg-([.0-9]+).tar.bz2.asc<\/a>\s+')
all_versions = parse_re.findall(ffmpeg_releases)
all_versions.sort(key=StrictVersion, reverse=True)

version, all_versions = all_versions[0], all_versions[1:]

last = version.split('.')
keep_version = ['snapshot']

keep_version.append(version)

for cur in all_versions:
    if cur < MIN_VERSION:
        break

    tmp = cur.split('.')
    # Check Minor
    if len(tmp) >= 2 and tmp[1].isdigit() and tmp[1] < last[1]:
        keep_version.append(cur)
        last = tmp
    # Check Major
    elif len(tmp) > 1 and tmp[0].isdigit() and tmp[0] < last[0]:
        keep_version.append(cur)
        last = tmp

for version in keep_version:
    for variant in VARIANTS:
        if version == 'snapshot':
            dockerfile = 'docker-images/%s/%s/Dockerfile' % (
                version, variant)
            travis.append(' - VERSION=%s VARIANT=%s' % (version, variant))
            azure.append('      %s_%s:\n        VERSION: %s\n        VARIANT: %s' % (version.replace('.', '_'), variant, version, variant))
=======
import getopt
import argparse
import configparser
from os import listdir, path

variants = ['alpine', 'centos', 'ubuntu', 'nvidia', 'armv7']
versions = ['snapshot', '4.1', '4.0', '3.4', '3.3', '3.2', '2.8']
builddir = '/tmp/build'
makeflags = '-j6'

templates = "./templates"

fragments = path.join(templates, "fragments")
common = path.join(templates, "common")
configfile_template = path.join(templates, 'config', "config_${version}.ini")

class ActionEnableDisable(argparse.Action):
    def __init__(self, option_strings, dest, default=None, required=False, help=None):
        if len(option_strings) != 1:
            raise ValueError('Only a single argument is allowed with enable/disable action')
        if not option_strings[0].startswith('--'):
            raise ValueError('Enable/Disable arguments must be prefixed with "--"')

        opt_name = option_strings[0][2:]
        opts = ['--enable-' + opt_name, '--disable-' + opt_name]
        super(ActionEnableDisable, self).__init__(opts, dest, nargs=0, const=None, default=default, required=required, help=help)

    def __call__(self, parser, namespace, values, option_strings=None):
        if option_strings.startswith('--disable-'):
            setattr(namespace, self.dest, False)
>>>>>>> fix extra comma
        else:
            setattr(namespace, self.dest, True)

def parser_gen():
    parser = argparse.ArgumentParser(description='Dockerfile generator.')
    for f in listdir(fragments):
        if f != 'ffmpeg' and path.isfile(path.join(fragments, f)):
            parser.add_argument('--' + f, action=ActionEnableDisable, default=None, help='enable/disable ' + f)

    parser.add_argument('--enable-all', help='set all external libraries to true', action='store_true', default=False)
    parser.add_argument('variant', default='alpine', choices=variants)
    parser.add_argument('version', default='4.1', choices=versions)
    parser.add_argument('--with-bins', action='store_true', default=False )
    parser.add_argument('--no-strip', action='store_true', default=False)

    outsize = parser.add_mutually_exclusive_group(required=False)
    outsize.add_argument('--fat', help='keep everything', action='store_true', default=True)
    outsize.add_argument('--slim', help='only keep libraries', action='store_true', default=False)
    outsize.add_argument('--scratch', help='build from scratch', action='store_true', default=False)

    return parser

def kebab_arg(name):
    return name.replace('_', '-')

def snake_arg(name):
    return name.replace('-', '_')

def dockerfile_gen(args, config, packages):
    variant = open(path.join(templates, 'variants', "Dockerfile.%s" % (getattr(args, 'variant'))))
    src = Template(variant.read())

    d={
        'prefix': builddir,
        'makeflags': makeflags,
        'packages': '',
        'dev_packages': ''
      }

   

    deps = []
    flags = []
    default = False
    if getattr(args, 'enable_all'):
        delattr(args, 'enable_all')
        default = True
        
    for section in config.sections():
        dep = snake_arg(section)
        if hasattr(args, dep) and getattr(args, dep) is None:
            setattr(args, dep, default)

    for arg in vars(args):
        library = kebab_arg(arg)
        if getattr(args, arg) and library in config:
            if 'Variants' in config[library] and variant in config[library]['Variants'].split(','):
                continue
            if 'DependsOn' in config[library]:
                if not config[library]['DependsOn'] in deps:
                    for dependency in config[library]['DependsOn'].split(','):
                        deps.append(dependency.strip())
            if 'Flags' in config[library]:
                if not config[library]['Flags'] in flags:
                    for flag in config[library]['Flags'].split(','):
                        flags.append(flag.strip())
            if not library in deps:
                deps.append(library)

    for dep in deps + ['ffmpeg']:
        if 'Install' in config[dep]:
            for package in config[dep]['Install'].split(','):
                d['packages'] = "%s %s" % (packages[getattr(args, 'variant')][package].strip(), d['packages'])
        if 'InstallDev' in config[dep]:
            for package in config[dep]['InstallDev'].split(','):
                d['dev_packages'] = "%s %s" % (packages[getattr(args, 'variant')][package].strip(), d['dev_packages'])

    result = src.safe_substitute(d)
    print(result)

    print ("")
    print ("ARG\tFFMPEG_VERSION=%s" % (config.get('ffmpeg', 'Version')))
    for dependency in deps:
            if "Version" in config[dependency]:
                print ("ARG\t%s_VERSION=%s" % (snake_arg(dependency.upper()), config.get(dependency, "Version")))

    print ("")
    for dependency in deps:
        if "SHA256sum" in config[dependency]:
            print ("ARG\t%s_SHA256SUM=%s" % (dependency.upper(), config.get(dependency, "SHA256sum")))

    print("")
    for dependency in deps:
            with open(path.join(fragments, dependency)) as fragment:
                print (fragment.read())

    with open(path.join(fragments, 'ffmpeg')) as ffmpeg_fragment:
        ffmpeg_template = Template(ffmpeg_fragment.read())
        ffmpeg_flags = ' \\\n\t'.join(flags)

        result = ffmpeg_template.safe_substitute({'lib_flags': ffmpeg_flags})
        print(result)

    if getattr(args, 'slim'):
        assembly_type = 'slim'
        release_pattern = {'source': 'base', 'entrypoint': 'ffmpeg', 'install_dir': '/usr/local'}
        assembly_pattern = {
            'bins': 'true' if getattr(args, 'with_bins') else 'false',
            'strip': 'false' if getattr(args, 'no_strip') else 'true'
            }
    elif getattr(args, 'scratch'):
        assembly_type = 'scratch'
        release_pattern = {'source': 'scratch', 'entrypoint': '/bin/ffmpeg', 'install_dir': '/'}
        assembly_pattern = {
            'bins': 'true' if getattr(args, 'with_bins') else 'false',
            'strip': 'false' if getattr(args, 'no_strip') else 'true'
            }
    else :
        assembly_type = 'fat'
        release_pattern = {'source': 'base', 'entrypoint': 'ffmpeg', 'install_dir': '/usr/local'}
        assembly_pattern = {}

    with open(path.join(common, assembly_type)) as assembly:
        assembly_template = Template(assembly.read())            
        print (assembly_template.safe_substitute(assembly_pattern))

    with open(path.join(common, 'release')) as release:
        release_template = Template(release.read())
        print (release_template.safe_substitute(release_pattern))



def main(argv):
    args_parser = parser_gen()
    config_parser = configparser.ConfigParser()
    package_parser = configparser.ConfigParser()

    args = args_parser.parse_args()
    configfile = Template(configfile_template)

    config_parser.read(configfile.safe_substitute({'version': getattr(args, 'version')}))
    package_parser.read(path.join(templates, 'variants', 'packages.ini'))
    dockerfile_gen(args, config_parser, package_parser)

if __name__ == '__main__':
    main(sys.argv)