import warnings


from src.engine.base_engine import Engine
from src.utils.arg_parser import parse_args
from src.utils.logger import Logger



warnings.filterwarnings('ignore')


if __name__ == "__main__":

    args = parse_args()
    engine = Engine()

    engine.start()
