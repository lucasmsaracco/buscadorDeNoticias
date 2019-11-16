import feedparser
import webbrowser
import configparser
import lxml.etree
import urllib.request
import request
import os
import errno
import copy

parser = configparser.ConfigParser()
parser.read('/config.ini')
config_dict = {}

for element in parser.sections():
    config_dict[element] = {}
    url = ''
    for name, value in parser.items(element):
        config_dict[element][name] = value
        if (name == 'url_base'):
            url = value
        elif not (name == 'query_interval' or name == 'tmp' or name == 'output'):
##            feed = feedparser.parse(url+value)
##            print (url+value)
##            feed_entries = feed.entries
##
##            for entry in feed.entries:
##
##                if ('title' in entry) and ('published' in entry) and ('summary' in entry):
            g = urllib.request.urlopen(url+value)
            with open('last.xml', 'b+w') as f:
                f.write(g.read())

            rootWeb = lxml.etree.parse("last.xml")
            a = value.split("/")
            
            if element=="LA_VOZ":
                filename = "Indice/"+element+"/"+name+"/"+a[2]
            else:        
                filename = "Indice/"+element+"/"+name+"/"+a[2]+".xml"
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            if not os.path.exists(filename):
                with open(filename, "b+w") as file:
                    g = urllib.request.urlopen(url+value)
                    file.write(g.read())
            else:
                for item in rootWeb.xpath(".//item"):
                    title = item.find(".//title").text
                    pubDate = item.find(".//pubDate").text   
                    root = lxml.etree.parse(filename)
                    pathTitle = ".//item[title='"+title+"']/title"
                    print(pathTitle)
                    try:
                        estaTitulo = root.find(pathTitle)
                    except:
                        pass    
                    pathPublished = ".//item[pubDate='"+pubDate+"']/title"
                    estaPublicado = root.find(pathPublished)
                    if (estaTitulo == None) and (estaPublicado == None):
                        #TODO: Guardar
                        print("Agregado")
                        dupe = copy.deepcopy(item)
                        root.getroot().insert(0,item)
                        lxml.etree.dump(root.getroot())
                f = open(filename, 'w')
                f.write(lxml.etree.tostring(root.getroot(), pretty_print=True).decode("utf-8"))
                f.close()
##                    article_title = entry.title
##                    article_published_at = entry.published # Unicode string
##                    #article_published_at_parsed = entry.published_parsed # Time object
##                    content = entry.summary
##                    afile.write(article_title + "\n" + article_published_at + entry.link + "\n" + content + "\n")
##                    #print("{}".format(article_title))
##                    #print("Publicado el: {}".format(article_published_at))
##                    #print("Contenido: {}".format(content))
##                    #print("\n")
