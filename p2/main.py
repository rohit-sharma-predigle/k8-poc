from time import sleep


def run():
    for i in range(10):
        print("Iteration ", i)
        sleep(1)

    raise Exception


if __name__ == "__main__":
    run()
