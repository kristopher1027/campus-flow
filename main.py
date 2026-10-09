from campusflow.storage import StorageError, load_tickets, save_tickets


def main():
    try:
        tickets = load_tickets()
    except StorageError as error:
        print(f"Error: {error}")
        return          # stop; do not continue with an empty list

    # ... menu loop. After every successful change:
    # save_tickets(tickets)


if __name__ == "__main__":
    main()