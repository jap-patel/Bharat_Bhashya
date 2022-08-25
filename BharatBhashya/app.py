from flask import Flask, flash, redirect, render_template, request, session, abort, Response, url_for
import re
import yagmail
import os
import helper
import otherTextToText
import otherTextToSpeech
import otherSpeechToText

app = Flask(__name__)

@app.route('/')
def index():  
    session['logged_in'] = False
    return home()

@app.route('/home')
def home():
    if not session.get('logged_in'):        
        return render_template('index.html')
    else:
        return user()

@app.route("/converter")
def converter():    
    return render_template('converter.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:                
        password = request.form['password'] 
        username = request.form['username'] 
        user_conn = helper.connect_to_db('users')                
        user_coll = user_conn[2]                
        check_user = user_coll.find({"username": username, "password": password})                  
        user_result = list(check_user)                
        if(len(user_result) != 0):
            security_agency_name = user_result[0]['security_agency_name']            
            email = user_result[0]['email']
            session['logged_in'] = True    
            session['username'] = username
            session['email'] = email
            session['security_agency_name'] = security_agency_name
            cases_conn = helper.connect_to_db('cases')
            cases_coll = cases_conn[2]        
            open_case_detail = cases_coll.find({"username": username, "case_status": "open"}).sort('timestamp', -1).limit(5)
            close_case_detail = cases_coll.find({"username": username, "case_status": "close"}).sort('timestamp', -1).limit(5)
            open_case_result = list(open_case_detail)
            close_case_result = list(close_case_detail)            
            print("You have successfully Logged In")  
            user_conn[1].close()  
            cases_conn[1].close()  
            return render_template('user.html', username = username, email = email, security_agency_name = security_agency_name, \
                open_case_result = open_case_result, close_case_result = close_case_result)
        else:
            print('user not present')
            msg = 'user not present'
            user_conn[1].close()  
            return render_template('login.html', msg = msg)    
    return render_template('login.html')  

@app.route('/close_case', methods = ['GET', 'POST'])
def close_case():    
    cases_conn = helper.connect_to_db('cases')
    cases_coll = cases_conn[2]            
    close_case_detail = cases_coll.find({"username": session['username'], "case_status": "close"}).sort('timestamp', -1)
    close_case_result = list(close_case_detail)     
    cases_conn[1].close()  
    return render_template('close_case.html', close_case_result = close_case_result)    

@app.route('/open_case', methods = ['GET', 'POST'])
def open_case():
    cases_conn = helper.connect_to_db('cases')
    cases_coll = cases_conn[2]        
    open_case_detail = cases_coll.find({"username": session['username'], "case_status": "open"}).sort('timestamp', -1)
    open_case_result = list(open_case_detail)        
    cases_conn[1].close()  
    return render_template('open_case.html', open_case_result = open_case_result)

@app.route('/user', methods = ['GET', 'POST'])
def user():
    open_case_result = ""
    close_case_result = ""
    cases_conn = helper.connect_to_db('cases')
    cases_coll = cases_conn[2]        
    open_case_detail = cases_coll.find({"username": session['username'], "case_status": "open"}).sort('timestamp', -1).limit(5)
    close_case_detail = cases_coll.find({"username": session['username'], "case_status": "close"}).sort('timestamp', -1).limit(5)
    open_case_result = list(open_case_detail)
    close_case_result = list(close_case_detail)
    cases_conn[1].close()  
    return render_template('user.html', open_case_result = open_case_result, close_case_result = close_case_result, \
        username = session['username'], email = session['email'], security_agency_name = session['security_agency_name'])

@app.route('/case_detail/<fir_number>', methods = ['GET', 'POST'])
def case_detail(fir_number):    
    cases_conn = helper.connect_to_db('cases')
    cases_coll = cases_conn[2]        
    case_detail = cases_coll.find({"fir_number": fir_number})
    case_result = list(case_detail)    
    cases_conn[1].close()  
    return render_template('case_detail.html', case_result = case_result)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        msg=""
        if request.method == 'POST' and 'name' in request.form and 'password' in request.form and \
            'email' in request.form and 'repeat_password' in request.form and 'agree_on_all_terms' in request.form \
            and 'security_agency_name' in request.form and 'admin_token' in request.form:
            admin_token = "abimanyu_26417"
            form_admin_token = request.form['admin_token']
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            repeat_password = request.form['repeat_password']  
            security_agency_name = request.form['security_agency_name'].strip()              
            conn = helper.connect_to_db('users')
            coll = conn[2]                     
            check_username = coll.find({"username": name})
            check_username = list(check_username)
            check_email = coll.find({"email": email})
            check_email = list(check_email)    
            check_security_agency_name = coll.find({"check_security_agency_name": security_agency_name})
            check_security_agency_name = list(check_security_agency_name)    
            alphanum_re = "^[A-Za-z][A-Za-z0-9_]{7,29}$";            
            email_re = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            pass_re = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"                            
            #pass_re = re.compile(pass_re)
            if(admin_token!=form_admin_token):
                print('invalid admin_token')                
                msg = 'Invalid admin_token !'
            elif len(security_agency_name)<2 or len(security_agency_name)>40:
                print('invalid security_agency_name')                
                msg = 'Security Agency Name must be having (2-40) characters !'
            elif not re.fullmatch(email_re, email):
                print('invalid email')                
                msg = 'Invalid email address !'
            elif not re.match(alphanum_re, name):                                
                print('invalid name')
                if(len(name)<8 or len(name)>29):
                    msg = 'User ID must be having (8-29) characters !'
                else:
                    msg = 'User ID must contain only characters and numbers !'          
            elif(len(check_username)!=0 or len(check_email)!=0 or len(check_security_agency_name)):
                if len(check_username)!=0:
                    msg = "Account already exists !, please select different User Id"
                elif len(check_email)!=0:
                    msg = "Account already exists !, please select different email Id"
                elif len(check_security_agency_name)!=0:
                    msg = "Account already exists !, please select different Security Agency Name}"
                print('username or email_id already exists !, please select different elements')   
            elif not re.fullmatch(pass_re, password): 
                msg = helper.password_check(password)                               
                print(msg)
            elif(password != repeat_password):
                msg = "Repeated password is incorrect"
                print('Repeated password is incorrect')                  
            else:
                signup = coll.insert_one(
                    {"username": name,"email":email, "password": password, "security_agency_name":security_agency_name})
                if signup:
                    msg = "Successfully created a Valid Account"
                    print("You have Successfully created a Valid Account") 
                    conn[1].close()
                    return render_template('login.html', msg=msg) 
            conn[1].close()            
            return render_template('registration.html', msg=msg, msg_len = len(msg))          
        elif request.method == 'POST':                 
            msg = 'Please fill out the whole form !'
        return render_template('registration.html', msg=msg)   
    except Exception as e:        
        print(e)
        return render_template('registration.html', msg=msg)

@app.route('/create_case', methods = ['GET', 'POST'])
def create_case():
    msg=""
    if request.method == 'POST' and 'fir_number' in request.form and 'case_name' in request.form and \
        'case_incharge' in request.form and 'state' in request.form and 'area' in request.form \
        and 'date_of_crime' in request.form and 'suspects' in request.form and 'crime_category' in request.form and \
        'crime_sub_category' in request.form:
        fir_number = request.form['fir_number']
        case_name = request.form['case_name']
        case_incharge = request.form['case_incharge']
        state = request.form['state']  
        city = request.form['city']  
        area = request.form['area']
        date_of_crime = request.form['date_of_crime']
        suspects = request.form['suspects']        
        crime_category = request.form['crime_category']
        crime_sub_category = request.form['crime_sub_category']
        summary = request.form['summary']
        keywords = request.form['keywords']
        other_keywords = request.form['other_keywords']
        conn = helper.connect_to_db('cases')
        coll = conn[2]    
        check_fir_number = coll.find({"fir_number": fir_number})
        check_fir_number = list(check_fir_number)        
        check_case_name = coll.find({"case_name": case_name})
        check_case_name = list(check_case_name)            
        if(len(check_case_name) == 0 and len(check_fir_number) == 0):    
            create_case = coll.insert_one(
                {"username": session['username'],"fir_number":fir_number, "case_name": case_name, "case_incharge":case_incharge,\
                "state": state,"city":city, "area": area, "date_of_crime":date_of_crime, \
                "suspects": suspects,"crime_category":crime_category, "crime_sub_category": crime_sub_category, "keywords":keywords, \
                "other_keywords":other_keywords, "summary":summary, "case_status":"open", "allow_case_to_be_viewed":False, "case_solved":False})
            if create_case:            
                print("You have Successfully created a case")                 
                conn[1].close()
                return user()
        else:
            print('fir_number or case name already registered')
            msg = 'FIR number or Case Name already registered'
            conn[1].close()  
            return render_template('create_case.html', msg=msg)        
        conn[1].close()
    elif request.method == 'POST':                 
        msg = 'Please fill out the whole form !'
    return render_template('create_case.html', msg=msg)

@app.route('/case_detail_toggle_view/<fir_number>', methods = ['GET', 'POST'])
def case_detail_toggle_view(fir_number):      
    cases_conn = helper.connect_to_db('cases')
    cases_coll = cases_conn[2]        
    case_detail = cases_coll.find({"fir_number": fir_number})
    case_result = list(case_detail)                    
    if request.method == 'POST' and 'view_allow' in request.form:            
        cases_coll.update_one({"fir_number": fir_number}, {'$set': {"allow_case_to_be_viewed": True}})
    else:
        cases_coll.update_one({"fir_number": fir_number}, {'$set': {"allow_case_to_be_viewed": False}})
    if request.method == 'POST' and 'case_status' in request.form:        
        cases_coll.update_one({"fir_number": fir_number}, {'$set': {"case_status": "close"}})
    else:
        cases_coll.update_one({"fir_number": fir_number}, {'$set': {"case_status": "open"}})
    if request.method == 'POST' and 'case_solved' in request.form:        
        cases_coll.update_one({"fir_number": fir_number}, {'$set': {"case_solved": True}})
    else:
        cases_coll.update_one({"fir_number": fir_number}, {'$set': {"case_solved": False}})
    case_detail = cases_coll.find({"fir_number": fir_number})
    case_result = list(case_detail)   
    cases_conn[1].close()
    return render_template('case_detail.html', case_result = case_result)

@app.route('/view_session/<fir_number>', methods=['GET', 'POST'])
def view_session(fir_number):
    session_conn = helper.connect_to_db('sessions')
    session_coll = session_conn[2]        
    session_detail = session_coll.find({"fir_number": fir_number})
    session_result = list(session_detail)
    print('starts here')
    print(session_result)
    print('ends here')
    session_conn[1].close()
    return render_template('view_session.html', session_result = session_result)    

@app.route('/select_languages', methods=['GET', 'POST'])
def select_languages():
    
    if request.method == 'POST' and 'police_speech_language' in request.form and \
        'suspect_speech_language' in request.form and 'target_language' in request.form :
        form_police_speech_language = request.form['police_speech_language']
        form_suspect_speech_language = request.form['suspect_speech_language']
        form_target_language = request.form['target_language']
        police_speech_language = helper.get_speech_language(form_police_speech_language)
        suspect_speech_language = helper.get_speech_language(form_suspect_speech_language)
        police_text_language = helper.get_text_language(form_police_speech_language)
        suspect_text_language = helper.get_text_language(form_suspect_speech_language)
        
        try:
            speaker = request.form['speaker']   
            police_display_language_text = ""
            suspect_display_language_text = ""      
            display_language_text = ""
            audio_language = ""
            last_dialogue_text = ""
            
        except:
            speaker = "none"
            display_language_text = "none"
            last_dialogue_text = "none"
            audio_language = "none"
        # print(speaker)
        if speaker == "police":
            police_text = otherSpeechToText.speech_to_text(police_speech_language)
            police_display_language_text = otherTextToText.text_to_text(suspect_text_language, police_text)            
            display_language_text = "police: " + police_display_language_text 
            audio_language = suspect_text_language
            last_dialogue_text = "police: " + police_display_language_text 
        elif speaker == "suspect":
            suspect_text = otherSpeechToText.speech_to_text(suspect_speech_language)            
            suspect_display_language_text = otherTextToText.text_to_text(police_text_language, suspect_text)
            display_language_text = "suspect: " + suspect_display_language_text
            audio_language = police_text_language
            last_dialogue_text = "suspect: " + suspect_display_language_text
        with open("overall_" + str(form_police_speech_language) + "_to_" + str(form_suspect_speech_language) \
            + ".txt", "a+", encoding="utf-8") as f:
            if len(display_language_text)!=0:
                f.write(str(display_language_text))
                f.write("\n")
                f.write("\t")
                f.seek(0)
                display_language_text = f.read()                        
                f.close()
        print(display_language_text)        
        # with open("overall_" + str(form_police_speech_language) + "_to_" + str(form_suspect_speech_language) \
        #     + ".txt", "a+", encoding="utf-8") as f:
            
    return render_template('converter.html', display_language_text = display_language_text, speaker = speaker, \
        last_dialogue_text = last_dialogue_text, audio_language = audio_language, \
        form_police_speech_language = form_police_speech_language, form_suspect_speech_language = form_suspect_speech_language,\
        form_target_language = form_target_language)

@app.route('/hear_last_dialogue/<display_language_text>/<speaker>/<last_dialogue_text>/\
    <audio_language>/<form_police_speech_language>/<form_suspect_speech_language>/<form_target_language>', methods = ['GET','POST'])
def hear_last_dialogue(display_language_text, speaker, last_dialogue_text, audio_language, \
    form_police_speech_language, form_suspect_speech_language, form_target_language):
    content = otherTextToSpeech.hear_the_audio(last_dialogue_text, audio_language)
    print("after call", content)
    return render_template('converter.html', display_language_text = display_language_text, speaker = speaker, \
        last_dialogue_text = last_dialogue_text, audio_language = audio_language, form_target_language = form_target_language, \
        form_police_speech_language = form_police_speech_language, form_suspect_speech_language = form_suspect_speech_language)

@app.route('/save_session/<display_language_text>/<form_police_speech_language>/<form_suspect_speech_language>/<form_target_language>', methods=['GET', 'POST'])
def save_session(display_language_text, form_target_language, form_police_speech_language, form_suspect_speech_language):   
    return render_template('save_session.html', form_target_language = form_target_language, display_language_text = display_language_text, \
        form_police_speech_language = form_police_speech_language, form_suspect_speech_language = form_suspect_speech_language)

@app.route('/enter_session_details/<msg>/<form_police_speech_language>/<form_suspect_speech_language>/<form_target_language>', methods=['GET', 'POST'])
def enter_session_details(msg, form_police_speech_language, form_suspect_speech_language, form_target_language):
    msg = ""
    suspect_name = request.form['suspect_name']
    session_incharge = request.form['session_incharge']
    session_date = request.form['session_date']
    session_name = request.form['session_name']
    case_name = request.form['case_name']
    fir_number = request.form['fir_number']
    case_conn = helper.connect_to_db('cases')                
    case_coll = case_conn[2]
    check_case = case_coll.find({"fir_number": fir_number, "case_name": case_name})                  
    case_result = list(check_case)
    if(len(case_result) != 0):            
        session_conn = helper.connect_to_db('sessions')
        session_coll = session_conn[2]             
        with open("overall_" + str(form_police_speech_language) + "_to_" + str(form_suspect_speech_language) + ".txt", "r", encoding="utf-8") as f:
            f.seek(0)
            overall_text = f.read()
            f.close()    
        os.remove("overall_" + str(form_police_speech_language) + "_to_" + str(form_suspect_speech_language) + ".txt")
        target_language = helper.get_text_language(form_target_language)
        target_language_text = otherTextToText.text_to_text(target_language, overall_text)     
        session_count = session_coll.find().count({"fir_number": fir_number}) + 1
        session_detail = session_coll.insert_one({"fir_number":fir_number, "case_name": case_name, "session_incharge":session_incharge, "session_conversation_text":overall_text, \
            "suspect_name": suspect_name,"session_name":session_name, "session_date":session_date, "session_number":session_count, "target_language_text":target_language_text})
        if session_detail:
            print("case details inserted")
        else:
            print("case details not inserted")
        session_conn[1].close()
        case_conn[1].close()
        return view_session(fir_number)
    else:
        msg = "FIR number and case name aren't macthing or are incorrect!"
    return enter_session_details(msg, form_police_speech_language, form_suspect_speech_language, form_target_language)

@app.route('/search_all_cases', methods=['GET', 'POST'])
def search_all_cases():
    return render_template('filter.html')    

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html')    

@app.route('/terms_and_services', methods=['GET', 'POST'])
def terms_and_services():
    return render_template('terms_and_services.html')    

@app.route('/target_language_text_file/<target_language_text_file>', methods=['GET', 'POST'])
def target_language_text_file(target_language_text_file):
    target_language_text_file = target_language_text_file.replace("Police", "\nPolice")
    target_language_text_file = target_language_text_file.replace("Suspect", "\nSuspect")
    return render_template('target_language_text_file.html', target_language_text_file = target_language_text_file)    

@app.route('/session_conversation_text_file/<session_conversation_text_file>', methods=['GET', 'POST'])
def session_conversation_text_file(session_conversation_text_file):    
    session_conversation_text_file = session_conversation_text_file.replace("Police", "\nPolice")
    session_conversation_text_file = session_conversation_text_file.replace("Suspect", "\nSuspect")
    return render_template('session_conversation_text_file.html', session_conversation_text_file = session_conversation_text_file)    

@app.route("/about_us")
def about_us():
    if session['logged_in'] == True:
        login_status = True
    else:
        login_status = False    
    return render_template('about_us.html', login_status = login_status)

@app.route("/contactForm", methods=['GET', 'POST'])
def contactForm():
    msg = ""
    if session['logged_in'] == True:
        login_status = True        
    else:
        login_status = False        
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        mail = request.form['mail']
        number = request.form['number']
        message = request.form['message']   
        conn = helper.connect_to_db('users')
        coll = conn[2]                                     
        check_email = coll.find({"email": mail})
        check_email = list(check_email) 
        # if(len(check_email)!=0):            
        #     yag = yagmail.SMTP()
        #     contents = ["first name: " + fname + ", Last name: " + lname + "Email: " \
        #         + mail + ", number: " + number + ", message: " + message]
        #     yag.send('jappatel1704@gmail.com', 'subject', contents)
        #     msg = "your email has been recieved !"
        # else:
        #     msg = "Email id doesn't exists !"
        conn[1].close()
    return render_template('contact_us.html', login_status = login_status, msg = msg)

@app.route("/contact_us")
def contact_us():
    msg = ""
    if session['logged_in'] == True:
        login_status = True
    else:
        login_status = False
    return render_template('contact_us.html', login_status = login_status, msg = msg)

@app.route("/converter_understanding")
def converter_understanding():
    return render_template('converter_understanding.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = False
    session['email'] = False
    session['security_agency_name'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True, port=8000)


















# @app.route('/case_detail_allow_view', methods = ['GET', 'POST'])
# def case_detail_allow_view():  
#     a = "26417"  
#     cases_conn = helper.connect_to_db('cases')
#     cases_coll = cases_conn[2]        
#     case_detail = cases_coll.find({"fir_number": a})
#     prev_case_result = list(case_detail)            
#     print("before")    
#     print(prev_case_result[0]['allow_case_to_be_viewed'])       
#     if prev_case_result[0]['allow_case_to_be_viewed']:
#         cases_coll.update_one({"fir_number": a}, {'$set': {"allow_case_to_be_viewed": False}})
#     else:
#         cases_coll.update_one({"fir_number": a}, {'$set': {"allow_case_to_be_viewed": True}})
#     case_detail = cases_coll.find({"fir_number": a})
#     current_case_result = list(case_detail)
#     cases_conn[1].close()
#     print("after")    
#     print(current_case_result[0]['allow_case_to_be_viewed'])
#     return render_template('case_detail.html', case_result = current_case_result)
