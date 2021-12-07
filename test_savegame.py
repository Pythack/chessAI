board = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
user_input = None


if user_input == '/commands':
    print('/save : Save the state of the game \n/continue : Continue the last saved game')

if user_input == '/save':
    with open('Record.txt', 'w') as file:
        'Record.txt'.write(board)

if user_input == '/continue':
    with open('Record.txt', 'r+') as file:
        pass

user_input = str(input('Entrez : '))
