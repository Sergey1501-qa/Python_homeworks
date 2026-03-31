from user import User

def main():
    my_user = User("Анна", "Сидорова")

    my_user.print_first_name()

    my_user.print_last_name()

    my_user.print_full_name()

if __name__ == "__main__":
    main()