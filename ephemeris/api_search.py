import urllib.request
import json

def query_horizons(id_string):
    if " " in id_string:
        id_string = id_string.replace(" ", "%20")

    url_begin_str = "https://ssd.jpl.nasa.gov/api/horizons_lookup.api?sstr="
    url = url_begin_str + id_string
    try:
        with urllib.request.urlopen(url) as response:
            html_bytes = response.read()
            html_content = html_bytes.decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error making request: {e.reason}")
        return {}

    parsed = json.loads(html_content)
    total_cnt = parsed['count']
    results = parsed['result']

    id_number = {}

    if total_cnt == 0:
        pass
    elif total_cnt == 1:
        body = results[0]
        if 'asteroid' in body['type']:
            id_number = body['name'].split()[0]
        elif 'comet' in body['type']:
            id_number = f"DES={body['spkid']};"
        else:
            id_number = body['spkid']
    else:
        for body in results:
            name = body['name']
            if 'asteroid' in body['type']:
                id_number[name] = body['name'].split()[0]
            elif 'comet' in body['type']:
                id_number[name] = f"DES={body['spkid']};"
            else:
                id_number[name] = body['spkid']

    return id_number

if __name__ == "__main__":
    result = query_horizons("Neowise")
    print(result)