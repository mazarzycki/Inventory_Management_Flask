friends = ['Rolf', 'Tom', 'Cinthia']

def add_friend():
    new_friend = input('Add friend: ')
    friends.append(new_friend)

add_friend()

print(friends)