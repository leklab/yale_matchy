from flask import Flask, render_template, request, redirect, jsonify
app = Flask(__name__)

import json
import pprint
#import elasticsearch and connect to clutter
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


#create dictionary with HGNC names as keys and ENSG names as values
genes = open("mart_export_ens_hgnc_1to1only.txt","r").readlines()
geneDic = {}
for line in genes:
	line = line.replace("\n","")
	text = line.split("\t")
	geneDic[text[0]] = text[1]


@app.route('/', methods=['GET', 'POST'])
def login():
   return render_template('login_test.html')

@app.route("/home")
def home():
   return render_template("home.html")

@app.route("/about")
def about():
   return render_template("about.html")

@app.route("/publications")
def publications():
   return render_template("publications.html")

@app.route("/statistics")
def statistics():
   return render_template("statistics.html")

@app.route("/contact-us")
def contactUs():
   return render_template("contact-us.html")

@app.route("/account")
def account():
   return render_template("account.html")

@app.route("/help/eula")
def eula():
   return render_template("eula.html")

@app.route("/help/faq")
def faq():
   return render_template("faq.html")

@app.route("/help/submission-help")
def submissionHelp():
   return render_template("submission-help.html")

@app.route("/help/features-table")
def featuresTable():
   return render_template("features-table.html")

@app.route("/help/matchy-api")
def matchyApi():
   return render_template("matchy-api.html")

@app.route("/help/mme-api")
def mmeApi():
   return render_template("mme-api.html")

@app.route("/help/external-data-sources")
def externalData():
   return render_template("external-data.html")

@app.route("/my_submissions")
def mySubmissions():
   return render_template("my-submissions.html")

@app.route('/match', methods=['GET', 'POST'])
def api_response():
   	content = request.json
   	print content['genomicFeatures'][0]

   	search_matchy(content)

   	return jsonify({"uuid":"ok"})


def search_matchy(request_json):

	test_json = request_json['genomicFeatures'][0]
	print(test_json['gene']['id'])

	geneENSG = geneDic[test_json['gene']['id']]

  	res = es.search(index="patients", 
  		body={
			"query":{
		    	"match":{ "gene": geneENSG } 
    		}
    	}
    )

  	for hit in res['hits']['hits']:
  		print(hit['_source']['doc']['id'])
  		
  		for d in hit['_source']['doc']['disorders']:
  			print(d['label'])

  	#print(res)


@app.route('/search-result', methods=['GET', 'POST'])
def searchResult():
	geneHGNC = request.form['gene']
	geneENSG = geneDic[geneHGNC]
	inheritancePattern=request.form['inheritance-pattern']
	variantType=request.form['variant-type']
	chr=request.form['chr']
	position=request.form['position']
	ref=request.form['ref']
	alt=request.form['alt']
	phenotype=request.form['phenotype']

        res = es.search(index="patients", body={
#		"query":{
#		    "match":{ "gene":geneENSG} 
 #               }
		"query": {
			"dis_max": {
				"queries": [
					{"match":{"gene":geneENSG}},
					{"match":{"phenotype":phenotype}}, 
					{"match":{"variant-type":variantType}}
				],
				"tie_breaker": 1
				} #,
		#"sort" : ["_score"]
		}
	}, size=100)
	
	return render_template('search-result.html', gene=geneHGNC, inheritancePattern=inheritancePattern, variantType=variantType, chr=chr, position=position, alt=alt, ref=ref, phenotype=phenotype,res=res)

if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0')

