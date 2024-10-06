import warnings
import json

from src.engine.base_engine import Engine
from src.utils.arg_parser import parse_args
from src.utils.logger import Logger


warnings.filterwarnings('ignore')


if __name__ == "__main__":
    args = parse_args()
    with open(args.config, "r") as file:
        config = json.loads(file.read())

    logger = Logger(config["experiment_path"], config["experiment_name"])
    engine = Engine(args, logger, config)

    engine.start()
