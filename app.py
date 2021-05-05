from flask import Flask, render_template, request, jsonify
# from assistant import check
from chat import fxn 
import sys
sys.path.append('/.../EcommerceChatbot/Combined_scraper_and_sentiment_analysis/combined_scraper_and_model')
from Combined_scraper_and_sentiment_analysis.combined_scraper_and_model import get_reviews

global flag 
flag = False

app = Flask(__name__)

# def get_flag():
#     return flag

# def set_flag(x):
#     flag = x
#     return flag

@app.route("/", methods=['GET', 'POST'])
def home():
    # if request.method == 'POST':
    #     user_query = request.form['user_query']
    #     print(user_query)
    #     user_query = user_query.strip()
    #     result = check(user_query)
    #     return render_template('index.html', response=result, user_query=user_query)
    return render_template('index.html')

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    user_query = request.json 
    print("user query",user_query)
    user_query = user_query['name']    
    print("final user query",user_query)
    global flag 
    if flag==False:
        result,iflag = fxn(user_query)
        if iflag == True:
            # result = "Please write only product name below : "
            flag = True
            return jsonify(result)
        else:
            return jsonify(result)
    else:
        print("Running Queery",user_query)
        result1,result2 = get_reviews(user_query)
        # result1 = "12"
        print("Done")
        flag = False
        return jsonify(result1)

if __name__ == "__main__":
    app.run(debug=True)
