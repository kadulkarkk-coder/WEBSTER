from aura.app.application import Application


def main():

    try:

        app = Application()

        app.run()

    except Exception as e:

        print("\nAURA FAILED TO START\n")

        print(type(e).__name__)

        print(e)


if __name__ == "__main__":

    main()