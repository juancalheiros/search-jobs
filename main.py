import requests
import os

from json import dump as json_dump
from dotenv import load_dotenv


load_dotenv()

url = os.getenv("URL_SEARCH_JOBS", "https://jsearch.p.rapidapi.com/search")
headers = { 
    "x-rapidapi-key" : os.getenv("API_KEY_RAPID"),
    "x-rapidapi-host": os.getenv("RAPID_API_HOST", "jsearch.p.rapidapi.com"),
}
query = {
    "query": os.getenv("QUERY_SEARCH", "desenvolvedor fullstack"),
    "num_pages": int(os.getenv("NUM_PAGES", 3)),
    "country": os.getenv("COUNTRY", "br"),
    "data_posted":os.getenv("DATA_POSTED", "all"),
    "work_from_home": os.getenv("REMOTE_JOB", "false"),
}


def search_job():
    try: 
        if not headers.get("x-rapidapi-key"):
            raise Exception("🚨 Please add your API_KEY_RAPID in .env")

        response  = requests.get(url, headers=headers, params=query)
        data  = response.json()

        result = []

        for job_data in data.get("data"):
            result.append({
                "job_id": job_data.get("job_id"),
                "job_title": job_data.get("job_title"),
                "company": job_data.get("employer_name"), 
                "job_apply_link": job_data.get("job_apply_link"),
                "description": job_data.get("job_description"),
                "job_is_remote": job_data.get("job_is_remote"),
                "job_location": job_data.get("job_location"),
                "job_google_link": job_data.get("job_google_link"),
                "apply_options": job_data.get("apply_options"),
            })

        with open("vagas.json", "w", encoding="utf-8") as f:
            json_dump(result, f, indent=4, ensure_ascii=False)

        return result

    except Exception as e:
        print(f"Erro ao buscar vagas: {e}")
        return []

if __name__ == "__main__":
    search_job()
