from cli.cli import CliTool
from config import config

def main():
    foo = CliTool()
    print(foo.parser.parse_args())
    print(config())

if __name__ == '__main__':
    main()
