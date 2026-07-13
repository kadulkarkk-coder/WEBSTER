from aura.core.launcher import Launcher


def main():

    try:

        launcher = Launcher()

        launcher.start()

    except Exception as e:

        print("\nAURA FAILED TO START\n")

        print(type(e).__name__)

        print(e)


if __name__ == "__main__":

    main()