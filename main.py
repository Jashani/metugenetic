import metugenetic.simulation.evolution
import metugenetic.config
from metugenetic.config import config


def wait_for_exit():
    while True:
        import time
        time.sleep(1000)


if __name__ == '__main__':
    metugenetic.config.initialise()
    e = metugenetic.simulation.evolution.Evolution(config.population, config.board_size)
    try:
        e.run(config.generations)
        wait_for_exit()
    except KeyboardInterrupt:
        print("Exiting")
        import sys
        sys.exit()
