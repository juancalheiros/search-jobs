import requests
import os
import logging

from json import dumps as json_dumps, dump as json_dump, loads as json_loads
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

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID")

def send_message_to_pubsub(data: str):

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    logging.info(f"Publishing message to {topic_path}...")

    future = publisher.publish(topic_path, data)
    future.result()

    logging.info(f"Published messages to {topic_path}.")


def validation_envs() -> None:
    required_vars = ["API_KEY_RAPID", "SEARCH_TARGETS", "GCP_PROJECT_ID", "PUBSUB_TOPIC_ID"]
    empty_vars = ""
    for var in required_vars:
        if os.getenv(var) is None: 
           empty_vars += f"{var}, "
    if empty_vars:
        raise Exception(f"🚨 Please add your {empty_vars} in .env\n")

def search_job():
    try:
        validation_envs()
        result = []
        query = {
            "num_pages": int(os.getenv("NUM_PAGES", 3)),
            "country": os.getenv("COUNTRY", "br"),
            "data_posted":os.getenv("DATA_POSTED", "all"),
            "work_from_home": os.getenv("REMOTE_JOB", "false"),
        }
        search_targets = json_loads(os.getenv("SEARCH_TARGETS", "[]"))

        for target in search_targets:
            jobs = []
            email = target.get("email")

            keywords = target.get("keywords", "desenvolvedor backend").split(",")
            partial_result = []

            for job_search in keywords:
                params = {**query, "query": job_search}

                logging.info(f"Initiating job search request... {job_search}")
                response  = requests.get(url, headers=headers, params=params)
                response.raise_for_status()

                data = response.json()

                logging.info("Request sucess. Processing data...") 
                for job_data in data.get("data"):
                    jobs.append({
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
                partial_result.append({"keywords": job_search, "jobs": jobs})

            result.append({"email": email, "searches": partial_result})

            with open("vagas.json", "w", encoding="utf-8") as f:
                json_dump(result, f, indent=4, ensure_ascii=False)

            logging.info(f"Finish process. Found {len(jobs)} jobs for {keywords}")
            logging.debug(f"Result data: {result}")

            send_message_to_pubsub(data=json_dumps(result).encode("utf-8"))

        return result
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    search_job()
