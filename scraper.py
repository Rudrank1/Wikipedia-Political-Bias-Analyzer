import requests
from bs4 import BeautifulSoup
import csv

def fetch_wikipedia_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except Exception as e:
        print("Error fetching " + url)
    return None

def extract_party_affiliation(soup):
    party_keywords = {
        'democrat': 'Democratic',
        'republican': 'Republican',
        'independent': 'Independent'
    }
    
    infobox = soup.find('table', {'class': 'infobox'})
    if infobox:
        rows = infobox.find_all('tr')
        for row in rows:
            header = row.find('th')
            data = row.find('td')
            if header and data:
                header_text = header.get_text().strip()
                if 'party' in header_text.lower():
                    data_text = data.get_text().strip().lower()
                    for keyword, party in party_keywords.items():
                        if keyword in data_text:
                            return party
    return "Unknown"

def analyze_bias(text):
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    sentence_count = len(sentences)
    
    positive_terms = [
        "visionary", "compassionate", "innovative", "principled", "resilient",
        "empathetic", "articulate", "trustworthy", "inspirational", "renowned",
        "dynamic", "courageous"
    ]
    
    negative_terms = [
        "dishonest", "self-serving", "ineffective", "indecisive", "manipulative",
        "unethical", "unreliable", "arrogant", "polarizing", "negligent", "inept",
        "closed-minded", "dishonorable", "notorious", "infamous", "authoritarian",
        "despot", "bigoted"
    ]
    
    positive_sentence_count = sum(1 for sentence in sentences if any(term in sentence for term in positive_terms))
    negative_sentence_count = sum(1 for sentence in sentences if any(term in sentence for term in negative_terms))
    
    achievements = sum(text.lower().count(term) for term in ['achievement', 'notable', 'award', 'honor'])
    criticisms = sum(text.lower().count(term) for term in ['criticism', 'controversy', 'scandal'])
    
    bias_score = achievements - criticisms + positive_sentence_count - negative_sentence_count
    
    return {
        'sentence_count': sentence_count,
        'positive_sentence_count': positive_sentence_count,
        'negative_sentence_count': negative_sentence_count,
        'achievements': achievements,
        'criticisms': criticisms,
        'bias_score': bias_score
    }

def find_table_with_column_count(soup, column_count):
    tables = soup.find_all('table', {'class': 'sortable'})
    for table in tables:
        rows = table.find_all('tr')
        if len(rows) > 1:
            headers = rows[0].find_all('th')
            if len(headers) == column_count:
                return table
    return None

def get_senators(soup):
    senators = []
    table = find_table_with_column_count(soup, 11)
    if table:
        print("Found table for Senators.")
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('th')
            if len(cols) >= 1:
                name_tag = cols[0].find('a')
                if name_tag:
                    name = name_tag.get_text(strip=True)
                    print("Extracted Senator:", name)
                    senators.append(name)
    else:
        print("Senators table with 11 columns not found.")
    
    return senators

def get_representatives(soup):
    representatives = []
    table = find_table_with_column_count(soup, 8)
    if table:
        print("Found table for Representatives.")
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 1:
                name_tag = cols[0].find('a')
                if name_tag:
                    name = name_tag.get_text(strip=True)
                    if not name:
                        name_tag = cols[0].find('b')
                        if name_tag:
                            name = name_tag.get_text(strip=True)
                    if name:
                        print("Extracted Representative:", name)
                        representatives.append(name)
    else:
        print("Representatives table with 8 columns not found.")
    
    return representatives

def save_to_csv(file_name, data):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Index', 'Name', 'URL', 'Party Affiliation', 'Sentence Count', 'Positive Sentence Count', 'Negative Sentence Count', 'Achievements', 'Criticisms', 'Bias Score'])
        for index, entry in enumerate(data, start=1):
            writer.writerow([index] + entry)

senator_list_url = "https://en.wikipedia.org/wiki/List_of_current_United_States_senators"
house_member_list_url = "https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"

senator_soup = fetch_wikipedia_page(senator_list_url)
house_soup = fetch_wikipedia_page(house_member_list_url)

senators = get_senators(senator_soup) if senator_soup else []
representatives = get_representatives(house_soup) if house_soup else []

senator_results = []
representative_results = []

for name in senators:
    url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
    print(f"Processing {url}...")
    soup = fetch_wikipedia_page(url)
    if soup:
        page_text = ' '.join([para.get_text().strip() for para in soup.find_all('p') if para.get_text().strip()])
        party = extract_party_affiliation(soup)
        bias_analysis = analyze_bias(page_text)
        senator_results.append([name, url, party, bias_analysis['sentence_count'], bias_analysis['positive_sentence_count'], bias_analysis['negative_sentence_count'], bias_analysis['achievements'], bias_analysis['criticisms'], bias_analysis['bias_score']])
    else:
        senator_results.append([name, url, "Error: No content fetched."])

for name in representatives:
    url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
    print(f"Processing {url}...")
    soup = fetch_wikipedia_page(url)
    if soup:
        page_text = ' '.join([para.get_text().strip() for para in soup.find_all('p') if para.get_text().strip()])
        party = extract_party_affiliation(soup)
        bias_analysis = analyze_bias(page_text)
        representative_results.append([name, url, party, bias_analysis['sentence_count'], bias_analysis['positive_sentence_count'], bias_analysis['negative_sentence_count'], bias_analysis['achievements'], bias_analysis['criticisms'], bias_analysis['bias_score']])
    else:
        representative_results.append([name, url, "Error: No content fetched."])

save_to_csv('Databases/senators_info.csv', senator_results)
print("Senators' information has been saved to 'Databases/senators_info.csv'.")

save_to_csv('Databases/representatives_info.csv', representative_results)
print("Representatives' information has been saved to 'Databases/representatives_info.csv'.")
