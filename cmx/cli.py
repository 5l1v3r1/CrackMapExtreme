#!/usr/bin/env python3

####################################################################
#   cli.py   -   CMX command line interface 
#   
#   Displays CMX Banner
#   Generates command line arguments for a given protocol 
#
#
# Classes:
#   - 
#
# Non-Class Functions:
#   gen_cli_args
#
####################################################################

import argparse
import sys
import pkg_resources
from argparse import RawTextHelpFormatter
#import argcomplete
#from argcomplete.completers import ChoicesCompleter

from cmx.loaders.protocol_loader import protocol_loader
from cmx.helpers.logger import highlight
from cmx import config as cfg


def gen_cli_args():

    VERSION = (pkg_resources.get_distribution('cmx').version).split('+')
    #VERSION = cfg.VERSION
    RELEASED = cfg.RELEASED

    p_loader =  protocol_loader()
    protocols = p_loader.get_protocols()
    title = """____ ____ ____ ____ _  _   _  _ ____ ___    ____ _  _ ___ ____ ____ _  _ ____ 
|    |__/ |__| |    |_/    |\/| |__| |__]   |___  \/   |  |__/ |___ |\/| |___ 
|___ |  \ |  | |___ | \_   |  | |  | |      |___ _/\_  |  |  \ |___ |  | |___ 
"""

    parser = argparse.ArgumentParser(description="""
{}
      {}
                     {}{}
                    {}{}
                           {}: {}
              {} 
""".format(highlight(title, 'yellow'),
           highlight('Pentesting tool for on-prem, cloud, and hybrid AD environments', 'green'),
           highlight('Forged by the O.P. ', 'white'),
           highlight('@byt3bl33d3r', 'blue'),
           highlight('R3born from the ashes by ', 'red'),
           highlight('@awsmhacks', 'blue'),
           highlight('Version', 'green'),
           highlight(VERSION[0], 'cyan'),
           highlight('(/.__.)/ The python3 EXTREME edition \(.__.\)', 'yellow')),
           formatter_class=RawTextHelpFormatter,
           epilog="""Usage: 
       cmx [-D] PROTOCOL [-h] TARGET [target options] [-M MODULE [module options]]  

       cmx smb -M mimikatz --options    (List a particular module's options)
       cmx smb 10.10.10.10 -u Administrator -p Password --recon
       cmx -D smb 192.168.1.1 -u username -p password -M mimikatz

  Azure!
       cmx az --config   (get an azure session up, follow prompts)
       cmx az --user <useremail>   (gets all info about a single user)
       cmx az --users      (gets all users)
       cmx az -h  (for all current azure stuffs)

 *Check https://awsmhacks.github.io/cmxdocs/index for detailed usage* 

""",
           add_help=False, usage=argparse.SUPPRESS)

    parser.add_argument("--threads", type=int, dest="threads", default=100, help=argparse.SUPPRESS)
    parser.add_argument("--timeout", default=0, type=int, help=argparse.SUPPRESS) # use --timeout 0 for no timeout
    parser.add_argument("-D","--debug", action='store_true', help=argparse.SUPPRESS)
    parser.add_argument("--darrell", action='store_true', help=argparse.SUPPRESS)
    parser.add_argument("--rekt", action='store_true', help=argparse.SUPPRESS)

    subparsers = parser.add_subparsers(title='protocols', dest='protocol', help=argparse.SUPPRESS) #suppressing cause it looks cleaner. gonna have to hit the wiki for helps.

    std_parser = argparse.ArgumentParser(add_help=False)
    std_parser.add_argument("target", nargs='*', type=str, help="the target IP(s), range(s), CIDR(s), hostname(s), FQDN(s), file(s) containing a list of targets, NMap XML or .Nessus file(s)")
    std_parser.add_argument("-id", metavar="CRED_ID", nargs='+', default=[], type=str, dest='cred_id', help="database credential ID(s) to use for authentication")
    std_parser.add_argument("-u", metavar="USERNAME", dest='username', nargs='+', default=[], help="username(s) or file(s) containing usernames")
    std_parser.add_argument("-p", metavar="PASSWORD", dest='password', nargs='+', default=[], help="password(s) or file(s) containing passwords")
    fail_group = std_parser.add_mutually_exclusive_group()
    fail_group.add_argument("--gfail-limit", metavar='LIMIT', type=int, help='max number of global failed login attempts')
    fail_group.add_argument("--ufail-limit", metavar='LIMIT', type=int, help='max number of failed login attempts per username')
    fail_group.add_argument("--hfail-limit", metavar='LIMIT', type=int, help='max number of failed login attempts per host')

    module_parser = argparse.ArgumentParser(add_help=False)
    mgroup = module_parser.add_mutually_exclusive_group()
    mgroup.add_argument("-M", "-m", "--module", metavar='MODULE', help='module to use')

    module_parser.add_argument('-mo', metavar='MODULE_OPTION', nargs='+', default=[], dest='module_options', help='module options')
    module_parser.add_argument('-L', '--list-modules', action='store_true', help='list available modules')
    module_parser.add_argument('--options', dest='show_module_options', action='store_true', help='display module options')
    module_parser.add_argument("--server", choices={'http', 'https'}, default='https', help='use the selected server (default: https)')
    module_parser.add_argument("--server-host", type=str, default='0.0.0.0', metavar='HOST', help='IP to bind the server to (default: 0.0.0.0)')
    module_parser.add_argument("--server-port", metavar='PORT', type=int, help='start the server on the specified port')


    for protocol in list(protocols.keys()):
        protocol_object = p_loader.load_protocol(protocols[protocol]['path'])
        subparsers = getattr(protocol_object, protocol).proto_args(subparsers, std_parser, module_parser)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    return args
