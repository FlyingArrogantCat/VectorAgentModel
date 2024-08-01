from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()


    parser.add_argument("-c", 
                        "--config", 
                        default="./cfg/init.json")
    

    return parser.parse_args()
