from makima.core.agent import run_agent
import sys
from makima.ui.app import run_ui
from makima.setup import setup_api_key, setup_model


def main():
    # run_agent()
    setup_model()
    setup_api_key()
    run_ui()

if __name__ == "__main__":
    main()