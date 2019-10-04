import requests


def test_request(request_json):
	#res = requests.post('http://localhost:5000/match', json=test_json)
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
#print(test_json)
test_request(test_json)
print("")

print("Test 2 - Gene search: LAMA1")
test_json = {"patient": {"id": "test_patient", "contact": contact_details}, "genomicFeatures": [{"gene": {"id": "LAMA1"}}]}
test_request(test_json)