# sports/sparql_queries.py
from SPARQLWrapper import SPARQLWrapper, JSON


def get_all_athletes():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <https://www.w3.org/1999/02/22-rdf-syntax-ns>
        
        SELECT ?athlete ?athleteName ?birthDate
        WHERE {
          ?athlete a dbo:Person ;
                   rdf:type dbo:Athlete ;
                   rdf:type dbo:SoccerPlayer ;
                   dbo:birthDate ?birthDate;
                   foaf:name ?athleteName .
        }
        LIMIT 10000
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']


def get_player_details(name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <https://www.w3.org/1999/02/22-rdf-syntax-ns>
        
        SELECT ?athlete ?athleteName ?birthDate 
               (GROUP_CONCAT(DISTINCT ?positionLabel; separator=", ") AS ?positions)
               (GROUP_CONCAT(DISTINCT ?teamLabel; separator=", ") AS ?teams)
               (GROUP_CONCAT(DISTINCT ?eventLabel; separator=", ") AS ?events)
        WHERE {
          ?athlete a dbo:Person ;
                   rdf:type dbo:Athlete ;
                   rdf:type dbo:SoccerPlayer ;
                   foaf:name ?athleteName ;
                   foaf:name "%s"@en;
                   dbo:birthDate ?birthDate.
          OPTIONAL {
            ?athlete dbo:position ?position .
            ?position rdfs:label ?positionLabel .
            FILTER(LANG(?positionLabel) = "en")
          }
          OPTIONAL {
            ?athlete dbo:team ?team .
            ?team rdfs:label ?teamLabel .
            FILTER(LANG(?teamLabel) = "en")
          }
        OPTIONAL {
            ?event dbo:wikiPageWikiLink ?athlete.
                   {
                       ?event rdf:type dbo:SoccerTournament ;
                        rdfs:label ?eventLabel .
                    }
                    UNION
                    {
                         ?event rdf:type dbo:FootballLeagueSeason ;
                         rdfs:label ?eventLabel .
                     }
            FILTER(LANG(?eventLabel) = "en")
          }
        }
        GROUP BY ?athlete ?athleteName ?birthDate
    """ % name)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']


def get_all_football_events():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <https://www.w3.org/1999/02/22-rdf-syntax-ns>
        
        SELECT ?event ?eventLabel 
        WHERE {
         ?athlete a dbo:Person ;
                   rdf:type dbo:Athlete ;
                   rdf:type dbo:SoccerPlayer .
         ?event dbo:wikiPageWikiLink ?athlete.
                   {
                       ?event rdf:type dbo:SoccerTournament ;
                        rdfs:label ?eventLabel .
                    }
                    UNION
                    {
                         ?event rdf:type dbo:FootballLeagueSeason ;
                         rdfs:label ?eventLabel .
                     }
            FILTER(LANG(?eventLabel) = "en")
        }
        GROUP BY ?event
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']


def get_football_event_details():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <https://www.w3.org/1999/02/22-rdf-syntax-ns>
        
        SELECT ?event ?eventLabel ?eventCountry ?championsLabel
                         (GROUP_CONCAT(DISTINCT ?athleteName; separator=", ") AS ?athleteNames)
        WHERE {
                   {
                       ?event rdf:type dbo:SoccerTournament .
                    }
                    UNION
                    {
                         ?event rdf:type dbo:FootballLeagueSeason.
                     }
            
            ?event 
                       rdfs:label ?eventLabel;
                       dbp:country ?eventCountry;
                       dbp:champions ?champions.
            {?champions rdf:type dbo:SportsClub.} UNION {?champions rdf:type dbo:SoccerClub}
            ?champions rdfs:label ?championsLabel
            FILTER(LANG(?eventCountry) = "en")
            FILTER(LANG(?eventLabel) = "en")
            FILTER(LANG(?championsLabel) = "en")
            
            ?athlete a dbo:Person ;
                   rdf:type dbo:Athlete ;
                   rdf:type dbo:SoccerPlayer;
                   foaf:name ?athleteName.
                    FILTER(LANG(?athleteName) = "en")
        
             ?event dbo:wikiPageWikiLink ?athlete.
        }
        GROUP BY ?event ?eventLabel ?eventCountry ?championsLabel
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']
