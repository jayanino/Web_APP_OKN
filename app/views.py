from flask import render_template, request, redirect, flash,url_for, send_from_directory, abort,send_file
from werkzeug.utils import secure_filename
from app import app, scripts
import os
#checks the extension of file
def allowed_video(filename):
    if not filename:
        return False
    ext = filename.rsplit(".",1)[1]

    if ext.upper() in app.config["VID_EXTENSION"]:
        return True
    else:
        return False
#checks the file size 
def allowed_file_size(filesize):
    if filesize:
        if int(filesize) <= app.config["MAX_FILE_SIZE"]:
            return True
        else:
            return False
    else: return False
#download csv file
@app.route("/get-csv/<filename>")
def get_file(filename):
    path = "../"+app.config['FILEPATH']+"/csv"
    try:
        return send_from_directory(path,filename, as_attachment=True)
        
    except FileNotFoundError:
        abort(404)

@app.route('/' , methods=['GET', 'POST'])
def home():
    filename=''
    results=[]
    is_okn_page = True
    if request.method == "POST":

        if request.files:

            if not allowed_file_size(request.cookies.get("filesize")):
                flash("File Exceeded maximum size")
                return render_template("okn_program.html",is_okn_page=is_okn_page,filename=filename)
            
            video = request.files["video"]

            if video.filename == "":
                flash("Video must have a filename")
                return render_template("okn_program.html",is_okn_page=is_okn_page,filename=filename)
                
            
            if not allowed_video(video.filename):
                flash("Please upload a video file, allowed extension: MP4, MOV")              
                return render_template("okn_program.html",is_okn_page=is_okn_page,filename=filename)
            
            else:          
                filename = secure_filename(video.filename)
                directory = filename.split(".")[0]
                path = os.path.join(app.config["FILEPATH"],directory)
                os.mkdir(path)
                video.save(os.path.join(path, filename))
                filepath = (f"{path}/{filename}")
          
                results = scripts.load_video(path,filepath)
                scripts.generate_csv(results,filename)   
                filename = filename+".csv"

            return render_template("okn_program.html", results=results,is_okn_page=is_okn_page,filename=filename)  
                                
    return render_template("okn_program.html",filename=filename)

