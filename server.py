from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'ALL 4 one, 1 for all!'

import random

game_conditions = {
        'card1': ['Farm', '(earn 10 - 20 gold)', 10, 20],
        'card2': ['Cave', '(earn 5 - 10 gold)', 5, 10],
        'card3': ['House', '(earn 2- 5 gold)', 2, 5],
        'card4': ['Casino', '(win/lose 0 - 50 gold)', 0, 50],
        'gold': 50
}

@app.route('/')
def index():
    if 'isPlaying' in session:
        if session['isPlaying'] == True:
            pass
        else:
            gold = session['gold']
            turns = session['count']
            status = session['isWinner']
            session.clear()
            return render_template('index.html', gold = gold, turns = turns, status = status)

    else:
        session['isPlaying'] = True
        session['count'] = 0
        for key in game_conditions:
            session[key] = game_conditions[key]
        print(session['gold'])
    return render_template('index.html')

@app.route('/process_money', methods=['POST'])
def process_money():
    session['count'] += 1
    card = request.form['card-played']
    print(f"{card}")

    temp = make_money(card)
    print(f"{temp}")

    if session['gold'] >= 350 and session['count'] < 21:
        session['isWinner'] = True
        session['isPlaying'] = False
        print(f"\033[1;32m Ninja has earned {session['gold']} gold, winning this round of NINJA GOLD! \n")
    elif session['gold'] < 350 and session['count'] > 20:
        session['isWinner'] = False
        session['isPlaying'] = False
        print(f"\033[1;31m Ninja has failed to earn 500 gold or more in less than 20 turns, losing this round of NINJA GOLD! \n")

    return redirect('/')

def make_money(card):
    if session[card][0] == 'Casino':
        x = random.randint(0, 1)
        if x == 0:
            win = random.randint(session[card][2], session[card][3])
            print(f"\033[1;32m You've won {win} gold to add to your stash, Ninja! \n")
            session['gold'] += win
        else:
            loss = random.randint(session[card][2], session[card][3])
            print(f"\033[1;31m You've lost {loss} gold. Your stash has shrunk, Ninja! \n")
            session['gold'] -= random.randint(session[card][2], session[card][3])
    else:
        make = random.randint(session[card][2], session[card][3])
        print(f"\033[1;32m You made {make} gold working in the {session[card][0]}. \n")
        session['gold'] += make
    return card

if __name__ == '__main__':
    app.run(debug=True)
