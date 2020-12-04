# -*- coding: utf-8 -*-
import logging
import sys


def main():
    # Logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info("Hello world!")


if __name__ == "__main__":
    main()
