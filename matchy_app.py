from __future__ import division

from flask import Flask, render_template, request, redirect, jsonify
app = Flask(__name__)

import json
import pprint
import requests
import math


from utils.ontology import open_ontology
from utils.load_files import load_participants_hpo_terms

#import elasticsearch and connect to clutter
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def get_gene_details(gene_name):

  query = """
  {
    gene(gene_name: "%s") {
      gene_id
      gene_name
      canonical_transcript_id
    }     
  }""" % (gene_name)

  #print(query)

  res = requests.post('http://gnomad.broadinstitute.org/api', json={'query': query})

  if res.ok:
    #print res.json()
    return res.json()

  else:
    return({'data': 'error'}) 


def get_gene_constraint(transcript_id):

  query = """
  {
    transcript(transcript_id: "%s") {
      gnomad_constraint{
        pLI
      }

    }     
  }""" % (transcript_id)

  #print(query)

  res = requests.post('http://gnomad.broadinstitute.org/api', json={'query': query})

  if res.ok:
    print res.json()
    return res.json()

  else:
    return({'data': 'error'}) 


def get_gnomad_freq(variant_id):
    query = """
    {
        variant(dataset: gnomad_r2_1, variantId:"%s"){
        variantId
        ref
        alt
        ... on GnomadVariantDetails{
          exome{
            ac
            an
            filters
          }
          genome{
            ac
            an
            filters
          }
        }  
      }
    }""" % (variant_id)

    #print(query)

    res = requests.post('http://gnomad.broadinstitute.org/api', json={'query': query})

    if res.ok:      
        res_json = res.json()

        if not 'errors' in res_json:
            variant_details = res_json['data']['variant']

            ac_total = 0
            an_total = 0

            if 'exome' in variant_details:
                ac_total += variant_details['exome']['ac']
                an_total += variant_details['exome']['an']

            if 'genome' in variant_details:
                ac_total += variant_details['genome']['ac']
                an_total += variant_details['genome']['an']



            #print res.json()
            #print("AC: %d AN: %d AF: %.20e" % (ac_total, an_total, (1.0*ac_total/an_total)))
            return ac_total/an_total

        else:
            return 0.0



#create dictionary with HGNC names as keys and ENSG names as values
genes = open("mart_export_ens_hgnc_1to1only.txt","r").readlines()
geneDic = {}
for line in genes:
	line = line.replace("\n","")
	text = line.split("\t")
	geneDic[text[0]] = text[1]



graph, alt_ids, obsolete = open_ontology()
hpo_by_proband = load_participants_hpo_terms('test_phenotypes_per_subject.json',alt_ids, obsolete)
graph.tally_hpo_terms(hpo_by_proband)


def get_resnik_score(hpo_graph, proband_1, proband_2):
    """ Calculate the similarity in HPO terms between terms for two probands.
    
    This runs through the pairs of HPO terms from the two probands and finds
    the information content for the most informative common ancestor for each
    pair. We return the largest of these IC scores, known as the maxIC.
    
    Reference:
        Resnik, J Artif Intell Res (1999), 11:95-130.
    
    Args:
        hpo_graph: ICSimilarity object for the HPO term graph, with
            information on how many times each term has been used across all
            probands.
        proband_1: list of HPO terms for one proband
        proband_2: list of HPO terms for the other proband
    
    Returns:
        A score for how similar the terms are between the two probands.
    """
    
    ic = [0.0]
    for term_1 in proband_1:
        for term_2 in proband_2:
            #print("term1: %s term2: %s most_informative: %f" %(term_1, term_2, hpo_graph.get_most_informative_ic(term_1, term_2)))            
            ic.append(hpo_graph.get_most_informative_ic(term_1, term_2))
    
    return max(ic)


def get_ERIC_score(hpo_graph, proband_1, proband_2):
    """ calculate the similarity of HPO terms across different individuals.

    Reference: https://www.nature.com/articles/s41436-019-0439-8
    Li et al., Genetics in Medicine (2019)

    Args:
        hpo_graph: ICSimilarity object for the HPO term graph, with
            information on how many times each term has been used across all
            probands.
        proband_1: list of HPO terms for one proband
        proband_2: list of HPO terms for the other proband 

    """

    scores = [0.0]
    for term_1 in proband_1:
        for term_2 in proband_2:
            a = hpo_graph.calculate_information_content(term_1)
            b = hpo_graph.calculate_information_content(term_2)
            common = 2 * hpo_graph.get_most_informative_ic(term_1, term_2)
            minimum = min(a,b)

            #print("term1: %s term2: %s a: %f b: %f common: %f" %(term_1, term_2, a, b, common))

            if minimum >= common:
                scores.append(0)
            else:
                #print("In here!")
                scores.append(common-minimum)

    return(max(scores))




@app.route('/', methods=['GET', 'POST'])
def login():
   return render_template('index.html')

@app.route("/submission")
def submission():
   return render_template("submission.html")

@app.route("/about")
def about():
   return render_template("about.html")


@app.route("/home")
def home():
   return render_template("home.html")

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

@app.route("/google")
def google_signin():
   return render_template("google_signin.html")

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
   	#print content['genomicFeatures'][0]

   	results = search_matchy(content)
   	

   	return jsonify({"results": results})


def search_matchy(request_json):

    test_json = request_json['genomicFeatures'][0]
    #print(test_json['gene']['id'])

    variant_str = ''

    if 'variant' in test_json:
        chrom = test_json['variant']['referenceName'] if 'referenceName' in test_json['variant'] else ""
        
        #start and end coordinates are whacky but +1 works for snps for now    
        chrom_start = str(test_json['variant']['start']+1) if 'start' in test_json['variant'] else ""
        
        chrom_ref = test_json['variant']['referenceBases'] if 'referenceBases' in test_json['variant'] else ""
        chrom_alt = test_json['variant']['alternateBases'] if 'alternateBases' in test_json['variant'] else ""

        variant_str = "%s-%s-%s-%s" % (chrom,chrom_start,chrom_ref,chrom_alt)
        print(variant_str)



    phenotypes = []
    #print(request_json)


    if 'features' in request_json:
      for f in request_json['features']:
        if 'id' in f:
          phenotypes.append(f['id'])


    print(phenotypes)


    results = genotype_match(test_json['gene']['id'],variant_str,phenotypes)
    print(results)

    return results

  	#print(res)


def get_variant_score(genomic_features, ensembl_gene_id, variant):

  variant_scores = [0.0]

  for g in genomic_features:
      print(g['gene']['id'])
      #{u'assembly': u'GRCh37', u'start': 42929130, u'alternateBases': u'A', u'referenceName': u'17', u'end': 42929131, u'referenceBases': u'G'}
      if g['gene']['id'] == ensembl_gene_id and g['variant']:
          #print(g['variant'])
          chrom = g['variant']['referenceName'] if 'referenceName' in g['variant'] else ""
          
          #start and end coordinates are whacky but +1 works for snps for now    
          chrom_start = str(g['variant']['start']+1) if 'start' in g['variant'] else ""
          
          chrom_ref = g['variant']['referenceBases'] if 'referenceBases' in g['variant'] else ""
          chrom_alt = g['variant']['alternateBases'] if 'alternateBases' in g['variant'] else ""

          variant_str = "%s-%s-%s-%s" % (chrom,chrom_start,chrom_ref,chrom_alt)
          print(variant_str)

          if variant_str == variant:
              gnomad_af = get_gnomad_freq(variant_str)
              print("Variant matches: %s gnomAD freq: %.3e" % (variant_str,gnomad_af))


              #gnomAD has 141,456 samples
              gnomAD_singleton_af = 1/(2*141456)              
              max_variant_score = math.log(gnomAD_singleton_af)

              if(gnomad_af < gnomAD_singleton_af):
                variant_scores.append(1.0)
              else:
                variant_scores.append(math.log(gnomad_af)/max_variant_score)



  return max(variant_scores)


def get_phenotype_score(features, phenotypes):

  db_entry_phenotypes = []

  for f in features:
    if 'id' in f:
      db_entry_phenotypes.append(f['id'])


  #print(db_entry_phenotypes)
  #print(phenotypes)

  score = get_ERIC_score(graph, db_entry_phenotypes,phenotypes)
  max_phenotype_score = -1*math.log(1/40)


  print("Phenotype score: %f" % (score/max_phenotype_score))


  return score/max_phenotype_score

  #get_ERIC_score()




def genotype_match(gene_name, variant, phenotypes):

    #geneENSG = geneDic[gene_name]

    gene_details = get_gene_details(gene_name)
    #print("geneENSG: %s gene_details: %s" % (geneENSG, gene_details['data']['gene']['gene_id']))

    ensembl_gene_id = gene_details['data']['gene']['gene_id']
    canonical_transcript_id = gene_details['data']['gene']['canonical_transcript_id']

    print(canonical_transcript_id)
    constraint_details = get_gene_constraint(canonical_transcript_id)
    gene_constraint_pLI = constraint_details['data']['transcript']['gnomad_constraint']['pLI']

    #print("pLI: %lf" % (gene_constraint_pLI))
    print(gene_constraint_pLI)

    #At the moment genotype and phenotype are equal weighting (i.e. 0.5 each)
    #Gene only matches are scored based on pLI
    #TO DO: If inheritance model is specified use something different for recessive
    gene_score = gene_constraint_pLI

    results = []


    res = es.search(index="patients", 
    body={
    "query":{
        "match":{ "gene": ensembl_gene_id } 
      }
    }
    )

    for hit in res['hits']['hits']:
        doc = hit['_source']['doc']
        #print(doc)


        matchy_score = 0.0

        if 'genomicFeatures' in doc:
          variant_score = get_variant_score(doc['genomicFeatures'],ensembl_gene_id, variant)
        else:
          variant_score = 0.0    

  
        print("gene_score: %f variant_score: %f" % (gene_score,variant_score))

        if variant_score > 0:
            matchy_score += 0.5*variant_score
        else:
            matchy_score += 0.5*gene_score

        #If there are more than one gene. Then gene does not strictly have to match the query gene
        #There is no direct mapping between gene and phenotype
        if 'features' in doc:
          phenotype_score = get_phenotype_score(doc['features'],phenotypes)
        else:
          phenotype_score = 0.0

        matchy_score = round((matchy_score+0.5*phenotype_score),3)

        results.append({"score": {"patient": matchy_score}, "patient": {"id": doc['id'], "contact": doc['contact']}})

    return results


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

