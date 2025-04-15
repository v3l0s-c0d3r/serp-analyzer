import requests
import threading
import re
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# CONFIGURATION
# =========================
# Replace these with your own credentials.
API_KEY = "your_google_api_key"
SEARCH_ENGINE_ID = "your_search_engine_id"

# =========================
# GOOGLE CUSTOM SEARCH API CALL
# =========================
def perform_search(query, num_results=10):
    """
    Query the Google Custom Search API and return a list of results.
    Each result is expected to have at least title, link, and snippet.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': num_results
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get('items', [])
        return items
    except Exception as e:
        print(f"Error during API request: {e}")

# =========================
# DISPLAY SERP RESULTS
# =========================
def display_serp_results(results):
    """
    Display the SERP results by printing the title, link and snippet.
    (The snippet shows where keywords matched.)
    """
    if not results:
        print("No results found.")
        return

    print("\n=== SERP Results ===")
    for idx, item in enumerate(results, start=1):
        title = item.get("title", "No Title")
        link = item.get("link", "No Link")
        snippet = item.get("snippet", "No Description")
        print(f"\nResult {idx}:")
        print("Title: ", title)
        print("Link: ", link)
        print("Description: ", snippet)
        print("-" * 60)

# get keywords from features

def get_features_keywords(features: dict[str]) -> list[(str, str)]:
    # get the features keys
    res = []
    for ft in list(features):
        # a, b =ft.split("_")
        res.append(tuple(ft.split("_")))

    return res



def extract_crime_features(results):
    """
    Given a list of SERP results, scan each snippet for
    keywords associated with crime-reporting features.
    (This is a heuristic approach.)
    Returns a dictionary with feature counts.
    """
    features = {
        "incident_details": {
            "incident date": 0, 
            "incident time": 0, 
            "crime location": 0, 
            "crime scene description": 0,
            "type of crime": 0, 
            "crime category": 0, 
            "crime subcategory": 0, 
            "method of operation": 0,
            "crime motive": 0, 
            "crime description": 0, 
            "crime narrative": 0, 
            "weather conditions at crime": 0,
            "light conditions": 0, 
            "area type": 0, 
            "neighborhood description": 0, 
            "building type": 0,
            "entry method": 0, 
            "victim presence": 0, 
            "police response time": 0, 
            "crime timeline": 0,
            "crime escalation": 0
        },
        "criminal_details": {
            "criminal name": 0, 
            "suspect name": 0, 
            "alias used": 0, 
            "criminal age": 0, 
            "criminal gender": 0,
            "criminal nationality": 0, 
            "criminal ethnicity": 0, 
            "criminal race": 0, 
            "criminal occupation": 0,
            "criminal address": 0, 
            "criminal physical description": 0, 
            "criminal height": 0, 
            "criminal weight": 0,
            "criminal hair color": 0, 
            "criminal eye color": 0, 
            "criminal distinguishing marks": 0,
            "criminal tattoos or scars": 0, 
            "criminal record": 0, 
            "criminal gang affiliation": 0
        },
        "victim_details": {
            "victim name": 0, 
            "victim age": 0, 
            "victim gender": 0, 
            "victim nationality": 0, 
            "victim ethnicity": 0,
            "victim occupation": 0, 
            "victim address": 0, 
            "victim physical description": 0, 
            "victim injury details": 0,
            "victim statement": 0, 
            "victim relationship to criminal": 0, 
            "number of victims": 0,
            "wounded vs fatal injuries": 0, 
            "victim condition on arrival": 0, 
            "victim hospital admission": 0
        },
        "witness_details": {
            "witness name": 0, 
            "witness statement": 0, 
            "witness contact info": 0, 
            "number of witnesses": 0,
            "eyewitness accounts": 0, 
            "witness descriptions": 0, 
            "witness reliability": 0,
            "witness location at time of crime": 0
        },
        "weapons_and_evidence_details": {
            "weapon used": 0, 
            "type of weapon": 0, 
            "weapon serial number": 0, 
            "forensic evidence": 0, 
            "DNA evidence": 0,
            "fingerprint evidence": 0, 
            "ballistics report": 0, 
            "CCTV footage": 0, 
            "surveillance footage": 0,
            "digital evidence": 0, 
            "cyber evidence": 0, 
            "trace evidence": 0, 
            "blood spatter analysis": 0,
            "trace DNA analysis": 0, 
            "evidence chain of custody": 0, 
            "explosive residue": 0
        },
        "law_enforcement_investigation_details": {
            "police report number": 0, 
            "arrest details": 0, 
            "arrest warrant information": 0, 
            "suspect arrest": 0,
            "law enforcement response": 0, 
            "investigation lead": 0, 
            "forensic team involvement": 0,
            "crime lab report": 0, 
            "case officer name": 0, 
            "police department": 0, 
            "interagency cooperation": 0,
            "suspect interrogation details": 0, 
            "criminal charges": 0, 
            "prosecution details": 0,
            "extradition request": 0, 
            "search warrant details": 0, 
            "evidence seizure": 0, 
            "suspect custody details": 0,
            "police interview": 0, 
            "investigative timeline": 0, 
            "crime scene reconstruction": 0
        },
        "court_and_legal_proceedings": {
            "court hearing date": 0, 
            "court location": 0, 
            "judge name": 0, 
            "prosecutor name": 0, 
            "defense attorney name": 0,
            "trial proceedings": 0, 
            "court verdict": 0, 
            "sentencing details": 0, 
            "imprisonment duration": 0,
            "probation details": 0, 
            "plea bargain": 0, 
            "legal charges": 0, 
            "trial evidence": 0, 
            "jury decision": 0,
            "appeal information": 0, 
            "court documents": 0, 
            "case dismissal": 0, 
            "criminal record update": 0,
            "bail information": 0
        },
        "media_and_news_reporting_details": {
            "news outlet": 0,
            "reporter name": 0,
            "publication date": 0,
            "article headline": 0,
            "article subheading": 0,
            "article summary": 0,
            "article body text": 0,
            "source attribution": 0,
            "photo evidence": 0,
            "video footage provided": 0,
            "social media posts": 0,
            "public reaction": 0,
            "press conference details": 0,
            "editorial commentary": 0,
            "citation of sources": 0,
            "update timestamp": 0
        },
        "aftermath_and_impact_details": {
            "crime aftermath": 0, 
            "community impact": 0, 
            "crime prevention measures": 0, 
            "crime hot spots": 0,
            "criminal network analysis": 0, 
            "historical crime context": 0, 
            "prior incidents": 0,
            "location crime statistics": 0, 
            "criminal sentencing history": 0, 
            "victim support services": 0,
            "media bias": 0, 
            "investigation status": 0, 
            "ongoing investigation": 0, 
            "closed case status": 0,
            "crime cost analysis": 0
        }
    }

    # Get keywords from features keys. Assume get_features_keywords returns tuples of (key, keyword, ...)
    keywords = get_features_keywords(features)
    
    for item in results:
        snippet = item.get("snippet", "").lower()

        # Look for phrases – these are crude heuristics.
        for (key, keyword, *_) in keywords:
            if key in snippet and keyword in snippet:
                # Create a combined key from the keyword pair.
                combined_key = f"{key}_{keyword}"
                # Update the count.
                # (This example stores the count at the top level of the features dict;
                # you may choose to store it elsewhere.)
                if combined_key in features:
                    features[combined_key] += 1
                else:
                    features[combined_key] = 1

        # Check for additional keyword occurrences.
        if "victim" in snippet:
            # Update the victim name count inside the victim_details dictionary.
            features["victim_details"]["victim name"] += 1  
        if re.search(r'\b\d+\s+victims\b', snippet):
            features["victim_details"]["number of victims"] += 1

    return features


def visualize_crime_features(features: dict):
    """
    Visualize the aggregated counts of only the top-level keys in the features dictionary.
    
    If a top-level key's value is a nested dictionary, the sum of its values is used.
    Otherwise, the value is used directly.
    """
    top_labels = list(features.keys())
    top_counts = []

    for key in top_labels:
        value = features[key]
        # If the value is a dictionary, sum its integer values.
        if isinstance(value, dict):
            aggregated_count = sum(value.values())
        else:
            aggregated_count = value
        top_counts.append(aggregated_count)

    plt.figure(figsize=(12, 6))
    plt.bar(top_labels, top_counts, color='salmon')
    plt.xlabel("Top-level Crime-Reporting Features")
    plt.ylabel("Aggregated Frequency")
    plt.title("Distinctive Top-level Features in Crime Reporting Papers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()



# =========================
# EXTRACTION FOR DEEP LEARNING JOURNAL PAPERS
# =========================
def extract_deep_learning_subheadings(results):
    """
    Scan through the SERP results (title and snippet) for common deep learning
    sub-headings found in journal papers.
    Returns a dictionary with counts for each sub-heading.
    """
    # Common sub-headings in deep learning papers:
    possible_subheadings = [
        "Introduction",  
        "Related Work",  
        "Background and Preliminaries",  
        "Problem Statement",  
        "Deep Learning Overview",  
        "Model Architecture",  
        "Neural Network Design",
        "Case Studies",  
        "Applications and Use Cases",  
        "Image Recognition Applications",  
        "Natural Language Processing Applications",  
        "Speech and Audio Processing Applications",  
        "Reinforcement Learning Applications",   
        "Ethical Considerations",
        "Future Research Directions",  
        "Open Challenges in Deep Learning",  
        "Conclusion and Summary",  
        "Supplementary Material",  
        "Acknowledgements"
    ]
    subheading_counts = {heading: 0 for heading in possible_subheadings}
    
    for item in results:
        combined_text = item.get("title", "") + " " + item.get("snippet", "")
        for heading in possible_subheadings:
            if heading.lower() in combined_text.lower():
                subheading_counts[heading] += 1

    return subheading_counts



def visualize_deep_learning_subheadings(subheading_counts):
    """
    Visualize the sub-heading frequencies using a bar chart.
    """
    labels = list(subheading_counts.keys())
    counts = list(subheading_counts.values())

    plt.figure(figsize=(12, 6))
    plt.bar(labels, counts, color='skyblue')
    plt.xlabel("Sub-headings")
    plt.ylabel("Frequency")
    plt.title("Distinctive Sub-headings in Deep Learning Journal Papers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# =========================
# USER MODES (EXECUTED IN SEPARATE THREADS)
# =========================
def general_search_mode():
    query = input("\nEnter your search query: ")
    results = perform_search(query)
    display_serp_results(results)

def crime_reporting_mode():
    query = input("\nEnter your crime-reporting papers search query: ")
    results = perform_search(query)
    display_serp_results(results)

    # Use a thread pool to concurrently extract features and visualize
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_extract = executor.submit(extract_crime_features, results)
        features = future_extract.result()

        print("\n=== Extracted Crime Features ===")
        for feature, count in features.items():
            print(f"{feature}: {count}")

        # Visualize the feature counts.
        future_vis = executor.submit(visualize_crime_features, features)
        # Wait until the visualization thread completes (plt.show() is blocking)
        future_vis.result()

def deep_learning_mode():
    query = input("\nEnter your deep learning journal papers search query: ")
    results = perform_search(query)
    display_serp_results(results)

    # Use a thread pool to concurrently extract sub-headings and visualize
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_extract = executor.submit(extract_deep_learning_subheadings, results)
        subheading_counts = future_extract.result()

        print("\n=== Extracted Deep Learning Sub-headings Frequency ===")
        for heading, count in subheading_counts.items():
            print(f"{heading}: {count}")

        # Visualize the sub-heading frequencies.
        future_vis = executor.submit(visualize_deep_learning_subheadings, subheading_counts)
        future_vis.result()
