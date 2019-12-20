from src.app import WordenApp
import src.const as const
import argparse
import logging

def main():
    App = WordenApp()
    App.run()
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="worden",
            description='TUI Space operations center',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=const.MSG_CONTROLS_HELP )
    
    parser.add_argument('--debug', '-d', action='store_true', help="Debug messages will be written in worden.log")
    parser.add_argument('--version', '-v',action='store_true', help='Print version and exit')
    parser.add_argument('--refresh','-r', metavar='S', type=int,
        help='Time in 10ths of second to refresh API data; {} by default'.format(const.KEYPRESS_TIMEOUT))

    args = parser.parse_args()
    if args.version:
        print("worden version: {}".format(const.VERSION))
        exit(0)
    if args.debug:
        logging.basicConfig(filename="worden.log", level=logging.DEBUG)
    if args.refresh:
        const.KEYPRESS_TIMEOUT = args.refresh
    main()
