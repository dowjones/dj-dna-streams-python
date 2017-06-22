import time


def wait_while_processing(threads):
    while True:
        try:
            time.sleep(2)
            if are_all_threads_dead(threads):
                break
        except (KeyboardInterrupt):
            print('\nReceived keyboard interrupt.')
            break
        except:
            raise


def are_all_threads_dead(threads):
    all_dead = True
    for thread in threads:
        if thread.isAlive():
            all_dead = False
            break
    return all_dead
