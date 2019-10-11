import requests


def test_request(request_json):
	res = requests.post('http://yale-matchy.org:5000/match', json=test_json)

	if res.ok:
		print res.json()



gene = {"id": "EFTUD2"}
variant_type = {"id": "SO:0001587",
      			"label": "STOPGAIN"}

contact_details = {
	"name": "Monkol Lek",
	"institution": "Yale University",
	"href": "",
	"email": "monkol.lek@yale.edu",
	"roles": ["researcher"]		
}


print("Test 1 - Gene search: EFTUD2")
test_json = {"patient": {"id": "test_patient", "contact": contact_details}, "genomicFeatures": [{"gene": gene, "type": variant_type}]}
print("Request:")
print(test_json)
print("Response:")
test_request(test_json)
print("====")

print("Test 2 - Gene search: LAMA1")
test_json = {"patient": {"id": "test_patient", "contact": contact_details}, "genomicFeatures": [{"gene": {"id": "LAMA1"}}]}
print("Request:")
print(test_json)
print("Response:")
test_request(test_json)
print("====")


print("Test 3 - Gene search: LIMS2")
test_json = {"patient": {"id": "test_patient", "contact": contact_details}, "genomicFeatures": [{"gene": {"id": "LIMS2"}}]}
print("Request:")
print(test_json)
print("Response:")
test_request(test_json)
print("====")


variant = {"alternateBases": "C",
          	"assembly": "GRCh37",
          	"end": 128412081,
          	"referenceBases": "G",
          	"referenceName": "2",
          	"start": 128412080
        	}

print("Test 4 - Gene search: LIMS2 and variant: ")
test_json = {"patient": {"id": "test_patient", "contact": contact_details}, "genomicFeatures": [{"gene": {"id": "LIMS2"}, "variant": variant}]}
print("Request:")
print(test_json)
print("Response:")
test_request(test_json)
print("====")



features = [
    {"id":"HP:0001644"}, 
    {"id":"HP:0003325"}, 
    {"id":"HP:0000158"}
    ]

print("Test 5 - Gene search: LIMS2 and phenotype: ")
test_json = {"patient": {"id": "test_patient", "contact": contact_details}, "genomicFeatures": [{"gene": {"id": "LIMS2"}}], "features": features}
print("Request:")
print(test_json)
print("Response:")
test_request(test_json)
print("====")

