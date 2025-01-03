# controllers/api_controller.py
from flask import Blueprint, jsonify, request
from helpers.cleaning import load_and_clean_data
from helpers.model import prompt_creator, db2
import project_environment as env
import openai
import json

api = Blueprint('api', __name__)

# Load the cleaned data once
df = load_and_clean_data()

@api.route('/classification', methods=['POST'])
def classification():
    data = request.get_json()
    content = data["content"]
    openai.api_key = env.API_KEY

    # all client options can be configured just like the `OpenAI` instantiation counterpart
    openai.base_url = env.API_URL + "/v1/"
    openai.default_headers = {"x-foo": "true"}

    prompt = prompt_creator(env.INITIAL_PROMPT, env.db_configs[env.db_mode])

    messages = [
        { "role": "system", "content": prompt},
        { "role": "assistant", "content": "我係京都念慈庵嘅產品推介大使 請問身體有咩不適症狀需要幫手?" },
        { "role": "user", "content": content}
    ]

    initial_model = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    classification = initial_model.choices[0].message.content
    try:
        classification = json.loads(classification)
    except:
        classification = [-5] # Internal Issue

    if classification[0] < 0:
        return jsonify({"error": env.REJECTION[classification[0]]})
    else:
        return jsonify({"list": classification})
    
@api.route('/questionaire', methods=['POST'])
def questionaire():
    data = request.get_json()
    classification = data["list"]
    questionaire_response = data["questionaire_response"]

    filtered_df = df.loc[classification]
    print("before", filtered_df)

    if questionaire_response["phlegm_color"] == 2:
        return {"error": env.REJECTION[-2]}

    else:
        for column in questionaire_response:
            filtered_df = filtered_df[filtered_df[column] >= questionaire_response[column]]
    print("after", filtered_df)

    filtered_list = filtered_df.index.tolist()

    if 9 in filtered_list:
        return {
            "message": f'Ready for new questionnaire',
            "list": filtered_list
        }

    elif filtered_list == []:
        return jsonify({"error": env.REJECTION[-1]})

    else:
        return jsonify({"success": filtered_list})

@api.route('/questionaire2', methods=['POST'])
def questionaire2():
    data = request.get_json()
    existing_list = data["list"]
    answer = data["answer"]

    index = existing_list.index(9)
    existing_list[index] = existing_list[index]+answer

    return jsonify({"success": existing_list})

@api.route('/final_result', methods=['POST'])
def final_result():
    data = request.get_json()
    result = data["success"]
    
    response = db2(env.db_configs[env.db_mode], result)
    print(response)
    return jsonify({"success": response})