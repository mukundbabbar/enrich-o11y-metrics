import csv
import requests
import json

#############################
#############################
API_TOKEN = "USER_API_TOKEN"
API_BASE = "https://api.au0.signalfx.com/v2/dimension/host.name/"
#############################
#############################


headers = {
    "X-SF-TOKEN": API_TOKEN,
    "Content-Type": "application/json"
}

def get_dimension(host):
    url = API_BASE + host
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"Failed to get dimension for host {host}: {resp.status_code} {resp.text}")
        return None

def put_dimension(host, payload):
    url = API_BASE + host
    resp = requests.put(url, headers=headers, data=json.dumps(payload))
    if resp.status_code in (200, 202):
        print(f"✅ Updated dimension for host {host}")
    else:
        print(f"❌ Failed to update dimension for host {host}: {resp.status_code} {resp.text}")

def merge_tags(existing_tags, new_tags):
    # Normalize tags (strip spaces), avoid duplicates
    existing_set = set(t.strip() for t in existing_tags)
    new_set = set(t.strip() for t in new_tags)
    combined = list(existing_set.union(new_set))
    return combined

def update_payload(payload, csv_row):
    # Append tags
    csv_tags = csv_row.get('tags', "").split('|') if csv_row.get('tags') else []
    payload_tags = payload.get('tags', [])
    payload['tags'] = merge_tags(payload_tags, csv_tags)

    # Append other columns to customProperties
    if 'customProperties' not in payload or payload['customProperties'] is None:
        payload['customProperties'] = {}

    for k, v in csv_row.items():
        if k not in ('host', 'tags'):
            if v:
                if k in payload['customProperties'] and payload['customProperties'][k]:
                    existing_values = set(x.strip() for x in payload['customProperties'][k].split(','))
                    new_values = set(x.strip() for x in v.split(','))
                    combined = existing_values.union(new_values)
                    payload['customProperties'][k] = ','.join(sorted(combined))
                else:
                    payload['customProperties'][k] = v
    return payload

def main():
    with open('hosts.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Normalise column headers: replace spaces with underscores and make lowercase
        reader.fieldnames = [name.strip().replace(" ", "_").lower() for name in reader.fieldnames]

        for row in reader:
            # Also normalise row keys for safety
            row = {k.strip().replace(" ", "_").lower(): v.strip() for k, v in row.items() if k}
            host = row.get('host')
            if not host:
                continue
            payload = get_dimension(host)
            if not payload:
                continue
            updated_payload = update_payload(payload, row)
            print(json.dumps(updated_payload, indent=2))  # Logging

            # COMMENT BELOW TO VALIDATE THE PAYLOAD BEFORE UPDATING DIMENSIONS
            put_dimension(host, updated_payload)

if __name__ == "__main__":
    main()

