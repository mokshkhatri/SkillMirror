def recommend(results):
    print(f"\n{'Rank':<6} {'Job Title':<35} {'Company':<25} {'Score':<8} {'Apply Link'}")
    print("-" * 120)
    for rank, job in enumerate(results, 1):
        print(f"{rank:<6} {job['job_title']:<35} {job['company_name']:<25} {job['score']:<8} {job['job_url']}")

def get_market_skills(results):
    all_skills = []
    for job in results:
        skills = str(job['skills']).lower().replace(',', ' ').split()
        all_skills.extend(skills)
    
    skill_counts = {}
    for skill in all_skills:
        skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    top_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)[:10]
    return top_skills