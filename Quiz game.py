print("Welcome to the quiz")

play = input("Do you want to play my IT quiz game? ")
score = 0

if play != "yes":
    quit()

print("Okay! Let's play :)")

answer = input("What does CPU stand for? ")
if answer.lower() == "central processing unit":
    print('Correct!')
    score += 1
else:
    print("Incorrect")

answer = input("What does RAM stand for? ")
if answer.lower() == "random access memory":
    print('Correct!')
    score += 1
else:
    print("Incorrect")

answer = input("What does PSU stand for? ")
if answer.lower() == "power supply":
    print('Correct!')
    score += 1
else:
    print("Incorrect")

answer = input("What does GPU stand for? ")
if answer.lower() == "graphical processing unit":
    print('Correct!')
    score += 1
else:
    print("Incorrect")

print("You got " + str(score) + "Questions correct!")
print("You got " + str((score/4 * 100) + float("%")))
