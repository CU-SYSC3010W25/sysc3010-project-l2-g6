import pyrebase
import time

# Firebase Config
config = {
  "apiKey": "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCz3Oj8vMYmmY76\nYp83px7AMDoEirhDro3MZHJJeiVdDuTWxogKWdqUMs4jTs8Kj1H4DTF2RdzBtJYu\n0ThGQYufg+p9+1saWeUxfGTiNEWbb9tWt/tEt9oq6ChbcVzjlr65huZ1N0/ZU/5l\nfUOz2TwCZp1LVT4bZ25lBqTtLurmHYFImiOlx93gitr6vaICfdNALWHbwaseYL+e\nFZYPW/v7cZAwP+JvbX+VIYGInnMTcw4T3hE3KRVsba37gRtSqE4dDEiI5ulooLzL\nISYgGyjQPCxYMhzUYcdL56qmgcEz9GL75uLx6OxYvuau4IqjDnmZWElSUPRwalg5\nFgh0XIcnAgMBAAECggEAEY2TxU/iTKkReDkWDcHcW+g4+UbVIHHRZSrrsQ+1GXBX\nKpNkemd2JUlnWbBwFI6TyCVNeEaYJTqrqh+r93Cfy4OoZ6lspNU0wLrBmQZ96+NO\nNhfYHfGNXpZFPgCsY9+gdw2wbFcSDq/GSimf6QDgfOF+efgfNWByOHTItVxYpff9\nnB1AL9rkFLU933MJ3qSVn0UN+MLG5G2XhRVMaEvEdRjoLft7OyM+/5Cu+A6o93Vt\n5DvKm4SlA10ow6G+JY3enRnWQqL7Yi6Hd+NRfQDEK2ZNsv7hGk6/xy5RBmwdYn9H\nPRyALn1/hIw1N1eYTf19WEfLdhZ+JjeRrlsihRVEDQKBgQDcw6ZPZ22Zljg8q7uJ\n/lVGernTmaO1v/rieAkPyII+xVVb94BosWJuVqFKPGO5a7JDeistlNhND6HgfbET\n/5mGvoc+alWhVFLZ7e/Dbo8Fj7KHPIOod5xJBxYsyMH8Cu8Pp7heCM4VYo8qHR9t\nOdb38QoTnfOePhnRIh4Ux7zq3QKBgQDQkgvrXG3XkaSWqaThX5fU7JHdoygsHb48\nn7BPwDWP5NlvpRC7tsCzPmuRX5p//H/EtcUN1fc8h/bHZVYeO/Eo0gzafwHcV7Ys\nvEX6Kn1C2JWb2aKklhg+YiPqxjOWK/1S/jdXAflN4JOjQ6NBmQr4grxHR9sVGV6d\nQPoC8TQP0wKBgFI9WFEwOHYErgJ7/ysS4fWVdnBLRd9JG08OZGHK0ipMHNZbxyw5\nGG/+OauL/6JtakUU18ztK/7ZGfalHDhU+X5mr78ioa+t2AdzSeRF5WWu+FTEyE8T\n79aMm0gnqYwZDqGIW3g8U3lH9Ak+PBzWdSx8UMKqDr0eaUOtMAORvODJAoGAPgyE\n4UNBJlWc2nmjpKzUtbKffolwhRdgJhb30/IBvUo+6bj4rm+jCnAyfjAr/ZF3zWSq\nOACEqgxk/VMHeL0qdJNw4XvRaOTrPInSY6dKVp2qfJAVk9NXaQ+3UbwfUrjJh2w7\nuHXM3j9GjNatdfF60w3Jx4b4BWHjxPK0rjVl4KMCgYEAry9nYQ5EIfUBwngTRuVK\nJEl+QvzvzV7CnTywiZxw+gBDVYTeJoImx56q/d+m7BMys2CPzNWzocQayI579lCz\nIYPgTa6zwTzwMOOBDy7XvrAR3YGMJm44VNkKD+Lgnw/Up617zheS+MgDGvhLb+1j\nzsxeW/PwRvvQDj2MAoLULQ4=",
  "authDomain": "sysc-3010-project-l2-g6.firebaseapp.com",
  "databaseURL": "https://sysc-3010-project-l2-g6-default-rtdb.firebaseio.com",
  "storageBucket": "sysc-3010-project-l2-g6.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
dataset = "Gestures"
labels = ["currentGesture", "prevGesture"]
gestureList = ["a", "b", "x", "y"]

def setGesture(gesture: str):
    db.child(dataset).child(labels[0]).set(gesture)

def updateGestures(gestures: list):
    for g in gestures:
        prevGesture = db.child(dataset).child(labels[0]).get().val()
        db.child(dataset).child(labels[1]).set(prevGesture)
        db.child(dataset).child(labels[0]).set(g)
        print(f"wrote '{g}' to database at currentGesture")
        time.sleep(10)

def main():
    setGesture("lol")
    updateGestures(gestureList)

main()