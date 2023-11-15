from moviepy.editor import VideoFileClip
from transformers import pipeline
import shutil, csv, os
from app import app

video_cls = pipeline(model="jayanino/videomae-base-OKN-Test-v27")

def load_video(path,file_path):
    test_results = []
    clip = VideoFileClip(file_path)
    filename = str(clip.filename).split("/")[5] 
    duration = clip.duration
    start = 0 # start at 0 seconds
    end   = 2 # plays for 0 seconds and ends at 2 seconds
    test_results = create_vid_clip(clip,duration,start,end,filename,path,)
    return test_results

def create_vid_clip(clip,duration,start,end,filename,path):
    results = []
    vid_paths=[]
    subclip = clip.subclip(start, end)
    num_of_vid = 0
    video_details = []
    i=0
    while end < duration:
        video_details.append({"Start time": start, "End time":end})
        subclip = clip.subclip(start, end)    
        start = end - 1
        end += 1 
        vid_paths.append(f"{path}/clip{num_of_vid}.mp4")
        subclip.write_videofile(vid_paths[i])
        video_details[i].update({"Video_Name": f"{filename}"})
        num_of_vid+=1  
        i+=1
    clip.close()
    results = run_okn_detector(num_of_vid, vid_paths,video_details,path)
    return results

def run_okn_detector(num_of_vid, vid_paths,video_details,path):
    i=0
    test_results = []
    results = []
    while i < num_of_vid:
        test_results.append(video_cls(vid_paths[i]))
        i+=1
    results = show_test_results(test_results,video_details,path)
    return results

def show_test_results(test_results,video_details,path):
    results = []
    i=0
    for item in test_results:
        results.append(item[0])
        results[i].update(video_details[i])
        if item[0].get('label') == "okn":
            results[i].update({'Result': 1})
        else:
            results[i].update({'Result': 0})
        i+=1
    remove_file(path)
    return results

def remove_file(filepath):
    try:
        shutil.rmtree(filepath)
        print("fodler deleted")
    except OSError as error:
        print(error)
        print("folder path can not be removed")
    try:
        path = app.config['FILEPATH']+"/csv/"
        shutil.rmtree(path)
        print("fodler deleted")
    except OSError as error:
        print(error)
        print("folder path can not be removed")
        
    path = os.path.join(app.config['FILEPATH'], "csv")   
    os.mkdir(path) 


def generate_csv(test_results,filename):
    path = app.config['FILEPATH']+"/csv/"
    fieldnames = ["score", "label", "Start time", "End time", "Video_Name", "Result"]
    with open(f"{path}/{filename}.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(test_results)

#-----------------------------------------------------------------------------------------------
