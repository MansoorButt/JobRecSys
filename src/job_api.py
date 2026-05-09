from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

APIFY_API_TOKEN= os.getenv("APIFY_API_TOKEN")

client = ApifyClient(APIFY_API_TOKEN)

#fetch LinkedIn jobs based on search qury and location
def fetch_linkedin_jobs(search_query,location="pakistan",rows=60):
    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy":{
            "useApifyProxy":True,
            "apifyProxyGroups":["RESIDENTIAL"],
        }
    }
    run = client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs