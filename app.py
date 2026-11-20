import json
from difflib import get_close_matches

def load_training_data(file_path : str) -> dict:
    with open(file_path,'r') as file:
        data: dict = json.load(file)
    return data

def save_training_data(file_path : str, data: dict):
    with open(file_path,'w') as file:
        json.dump(data, file,indent=2)

def find_accurate(user_question : str, questions : list[str]) -> str|None:
    matches: list = get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None

def get_answer(request: str, training:dict) -> str|None:
    for q in training["requests"]:
        if q["request"] == request:
            return q["reply"]

def chatBot():
    training: dict =  load_training_data("train.json")
    while True:
        user_input: str = input("You : ")
        best_match: str|None = find_accurate(user_input,[q["request"] for q in training["requests"]])
        if best_match:
            reply : str = get_answer(best_match,training)
            print(f'Bot : {reply}')
        else:
            print("Sorry, but I don't know the answer, can you please give the correct answer ?")
            new_req : str = input("Type the answer or \"skip\" to skip : ")

            if new_req.lower() != "skip":
                training["requests"].append({"request":user_input,"reply":new_req})
                save_training_data('train.json',training)
                print("Answer Saved!")

chatBot()
