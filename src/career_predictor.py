
import pandas as pd

logs = pd.read_csv("data/user_logs.csv")

career_paths = {
    "Data Analyst":["python","sql","excel","power bi","tableau","pandas","numpy","statistics","data visualization","data analysis"],
    "Data Scientist":["python","sql","pandas","numpy","machine learning","deep learning","tensorflow","scikit-learn","statistics","matplotlib"],
    "Machine Learning Engineer":["python","tensorflow","pytorch","deep learning","machine learning","docker","git","scikit-learn","numpy","opencv"],
    "AI Engineer":["python","tensorflow","pytorch","transformers","hugging face","nlp","llm","generative ai","langchain","rag"],
    "Backend Developer":["python","django","flask","fastapi","sql","mysql","postgresql","git","docker","rest api"],
    "Frontend Developer":["html","css","javascript","typescript","react","next.js","bootstrap","tailwind css","git","figma"],
    "Full Stack Developer":["html","css","javascript","react","node.js","express.js","mongodb","sql","git","docker"],
    "Android Developer":["java","kotlin","android","android studio","firebase","git","sqlite","rest api","xml","flutter"],
    "Cloud Engineer":["aws","azure","gcp","docker","kubernetes","terraform","linux","git","jenkins","cloudformation"],
    "DevOps Engineer":["docker","kubernetes","jenkins","terraform","ansible","linux","aws","git","github actions","nginx"],
    "Cybersecurity Analyst":["network security","ethical hacking","penetration testing","wireshark","linux","python","firewall","cryptography","security","kali linux"],
    "Network Engineer":["networking","ccna","routing","switching","tcp/ip","dns","dhcp","firewall","linux","windows server"],
    "Software Tester":["manual testing","selenium","java","python","testng","jira","automation testing","bug tracking","api testing","postman"],
    "Data Engineer":["python","sql","spark","hadoop","airflow","aws","etl","data warehouse","docker","kafka"],
    "Business Intelligence Analyst":["power bi","tableau","sql","excel","data visualization","statistics","python","dashboard","business analysis","reporting"],
    "Database Administrator":["mysql","postgresql","oracle","sql","database","backup","performance tuning","linux","mongodb","database security"],
    "Embedded Systems Engineer":["c","c++","embedded c","microcontroller","arduino","raspberry pi","stm32","electronics","iot","pcb"],
    "IoT Developer":["arduino","raspberry pi","embedded c","mqtt","iot","python","esp32","sensors","wifi","cloud"],
    "Blockchain Developer":["solidity","ethereum","web3","smart contracts","javascript","node.js","git","blockchain","cryptography","metamask"],
    "UI/UX Designer":["figma","adobe xd","photoshop","illustrator","wireframing","prototyping","user research","design thinking","ui design","ux design"]
}

def load_student_skills(user_skills=None):
    if user_skills is not None:
        return {s.lower().strip() for s in user_skills if s.strip()}
    skills=set()
    for log in logs["Log"]:
        if pd.isna(log): continue
        skills.add(str(log).lower().strip())
    return skills

def get_star_rating(score):
    return "⭐⭐⭐⭐⭐" if score>=90 else "⭐⭐⭐⭐" if score>=75 else "⭐⭐⭐" if score>=60 else "⭐⭐" if score>=40 else "⭐"

def predict_career(user_skills=None):
    student=load_student_skills(user_skills)
    out=[]
    for career,req in career_paths.items():
        matched=sorted(student.intersection(req))
        missing=sorted(set(req)-student)
        score=round(len(matched)/len(req)*100,2)
        out.append({"career":career,"match_score":score,"stars":get_star_rating(score),"matched_skills":matched,"missing_skills":missing,"matched_count":len(matched),"total_skills":len(req)})
    out.sort(key=lambda x:x["match_score"],reverse=True)
    return out

def generate_report(user_skills=None):
    p=predict_career(user_skills)
    return {"recommended_career":p[0],"top_matches":p[:3]}

def display_report(user_skills=None):
    r=generate_report(user_skills)
    b=r["recommended_career"]
    print("\n========== CAREER PREDICTION ==========\n")
    print(b["stars"])
    print(b["career"])
    print(f"Match Score : {b['match_score']}%")
    print("\nMatched Skills")
    for s in b["matched_skills"]: print("✔",s.title())
    print("\nMissing Skills")
    for s in b["missing_skills"]: print("✘",s.title())
    print("\nTop Career Matches")
    for c in r["top_matches"]: print(f"- {c['career']} ({c['match_score']}%)")

if __name__=="__main__":
    display_report()

