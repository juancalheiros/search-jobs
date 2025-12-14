import requests
import os
import logging

from json import dump as json_dump, dumps as json_dumps
from google.cloud import pubsub_v1
from dotenv import load_dotenv


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

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

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID")

def send_message_to_pubsub(data: str):

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    logging.info(f"Publishing message to {topic_path}...")

    future = publisher.publish(topic_path, data)
    future.result()

    logging.info(f"Published messages to {topic_path}.")

def search_job():
    try: 
        if not headers.get("x-rapidapi-key"):
            raise Exception("🚨 Please add your API_KEY_RAPID in .env")

        logging.info("Initiating job search request...")
        response  = requests.get(url, headers=headers, params=query)
        data  = response.json()
        logging.info("Request sucess. Processing data...")

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

        logging.info(f"Finish process, total: {len(result)} jobs found.")
        logging.debug(f"Result data: {result}")

        send_message_to_pubsub(data=json_dumps(result).encode("utf-8"))

        return result

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    search_job()
