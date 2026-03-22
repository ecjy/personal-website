import urllib.request
import urllib.parse
import json
import time

publications = [
    "Evolution of cortical cerebral microinfarcts on 3T MRI: risk factors and clinical relevance",
    "Spatial navigation as a digital marker for clinically differentiating cognitive impairment severity",
    "Visit-to-visit blood pressure variability, brain MRI measures, and cognition in non-demented older adults",
    "Development of a Prognostic Model for Poststroke Dementia Using Multiple International Cohorts: A STROKOG Collaboration Study",
    "Association of Atrial Electrophysiological Abnormalities With Cognitive Decline and Cerebrovascular Disease",
    "Associations between Cognitive Frailty and Circulating Cardiovascular Biomarkers in a Memory Clinic Cohort",
    "Synergistic effect between cortical cerebral microinfarcts and brain atrophy on cognitive decline",
    "White Matter Hyperintensities Moderate the Association Between Diabetes and Cognitive Decline",
    "Effect of metabolic syndrome severity on cerebral haemodynamics and cognitive decline: a longitudinal study",
    "Mind the gap: Does brain age improve Alzheimer's disease prediction?",
    "Adherence to lifestyle intervention activities in the SINgapore GERiatric Intervention Study to Reduce Physical Frailty and Cognitive Decline (SInGER)",
    "A deep-learning retinal aging biomarker for cognitive decline",
    "Retinal thickness predicts the risk of cognitive decline over five years",
    "Additive Impact of Cardiometabolic Multimorbidity and Depression on Cognitive Decline and Dementia",
    "Unsupervised multimodal modeling of cognitive and brain health trajectories",
    "Validating the clinical utility of AI-guided tools for early dementia prediction in an untargeted ethnic-diverse memory clinic cohort",
    "Brain free-water increases in mild behavioral impairment",
    "Association of interleukin-6 and interleukin-8 with cognitive decline in a memory clinic-based cohort",
    "Longitudinal associations between β-amyloid and cortical thickness in non-demented older adults with cerebrovascular disease",
    "Cortical cerebral microinfarcts on 3T MRI and cognitive decline: A 5-year longitudinal study",
    "The SINgapore GERiatric Intervention Study to Reduce Physical Frailty and Cognitive Decline (SInGER): A pilot randomized controlled trial",
    "Automated quantification of cerebral microinfarcts on 3T MRI",
    "Scientific Reports 10 (1), 6457",
    "Profile of and risk factors for poststroke cognitive impairment in diverse ethnoregional groups",
    "Association of magnetic resonance imaging markers of cerebrovascular disease burden and cognition",
    "Cerebral microinfarcts on 3T MRI: a population-based study"
]

def get_json(url):
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def search_pubmed(title):
    query = urllib.parse.quote(title)
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json"
    data = get_json(url)
    if data:
        id_list = data.get("esearchresult", {}).get("idlist", [])
        if id_list:
            return id_list[0]
    return None

def get_details(pmid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
    data = get_json(url)
    if data:
        result = data.get("result", {}).get(pmid, {})
        doi = ""
        for articleid in result.get("articleids", []):
            if articleid.get("idtype") == "doi":
                doi = articleid.get("value")
        return {
            "pmid": pmid,
            "title": result.get("title"),
            "journal": result.get("fulljournalname"),
            "pubdate": result.get("pubdate"),
            "doi": doi
        }
    return None

results = []
for pub in publications:
    # Safely print for logs
    safe_pub = pub.encode('ascii', 'ignore').decode()
    print(f"Searching for: {safe_pub}...")
    pmid = search_pubmed(pub)
    if pmid:
        details = get_details(pmid)
        if details:
            details["query"] = pub
            results.append(details)
            print(f"  Found: {details['doi']}")
        else:
            results.append({"error": "No details", "query": pub})
    else:
        results.append({"error": "Not found", "query": pub})
    time.sleep(0.5)

with open("pubmed_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nDone! Results saved to pubmed_results.json")
