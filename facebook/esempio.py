access_token = "853458888154064|pOWWt9MdhJFilaJidskGyaFZpXU"
        
        #Apro l'xml contenente le notizie          
        tree = etree.parse(self.input()[0].path)
        rootParser = tree.getroot()
        
        #Creo questo xml che conterrà i commenti trovati da facebook
        root = etree.Element('root')              
        for child in rootParser:
            pld = child.attrib['nome']
            node_pld = etree.SubElement(root, "pld")
            node_pld.set("nome",pld)
            for news in child:
                for newsTitle in news.findall('titolo'): 
                    titolo = newsTitle.attrib['titolo']
                for newsUrl in news.findall('url_notizia'):
                    url = newsUrl.attrib['url']
                    try:
                        driver = webdriver.Chrome()
                        driver.get("https://www.facebook.com/pg/"+pld.replace(" ","")+"/posts/?ref=page_internal")
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME,"_1fa6")))
                        tField = driver.find_element_by_class_name("_58al")
                        tField.send_keys(titolo)
                        tField.send_keys(Keys.RETURN)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME,"UFIShareLink")))
                        element = driver.find_element_by_class_name("UFIShareLink")
                        postId = str(element.get_attribute("outerHTML")).split("https://www.facebook.com/shares/view?id=")[1].split("\"")[0]
                        driver.close()
                        #Qui costruisco il nodo della notizia, poi chiamo l'API di facebook per prendere i commenti e li inserisco
                        node_post = etree.SubElement(node_pld, "post")
                        node_post_url = etree.SubElement(node_post, "URL")
                        node_post_url.text = url
                        node_post_id = etree.SubElement(node_post, "ID")
                        node_post_id.text = postId
                        node_post_comments = etree.SubElement(node_post, "lista_commenti")
                        posts = requests.get("https://graph.facebook.com/179618821150_"+postId+"/comments?fields=message,from,comments{message,from,comments}&access_token="+access_token).json()
                        #Chiamo l'api di Facebook per prendere i commenti e le risposte:
                        while True:
                            try:
                                for post in posts['data']:
                                    try: 
                                        node_commento = etree.SubElement(node_post_comments, "commento")
                                        messaggio = post['message']
                                        autore = post['from']['name']
                                        id_autore = post['from']['id']
                                        id_commento = post['id']               
                                        node_testo_commento = etree.SubElement(node_commento, "testo_commento")
                                        node_testo_commento.text = messaggio               
                                        node_id_autore = etree.SubElement(node_commento, "id_autore")
                                        node_id_autore.text = id_autore
                                        node_id = etree.SubElement(node_commento, "id_commento")
                                        node_id.text = id_commento
                                        node_autore_commento = etree.SubElement(node_commento, "autore")
                                        node_autore_commento.text = autore
                                        try:
                                            variabile_chiama_errore = post['comments']['data'][0]['message']
                                            node_lista_risposte = etree.SubElement(node_commento, "lista_risposte")
                                            flag=True
                                            while flag:
                                                for reply in post['comments']['data']:
                                                    node_risposta = etree.SubElement(node_lista_risposte, "risposta")
                                                    messaggio = reply['message']
                                                    autore = reply['from']['name']
                                                    id_autore = reply['from']['id']
                                                    id_commento = reply['id']                
                                                    node_testo_commento = etree.SubElement(node_risposta, "testo_commento")
                                                    node_testo_commento.text = messaggio           
                                                    node_id_autore = etree.SubElement(node_risposta, "id_autore")
                                                    node_id_autore.text = id_autore
                                                    node_id = etree.SubElement(node_risposta, "id_commento")
                                                    node_id.text = id_commento
                                                    node_autore_commento = etree.SubElement(node_risposta, "autore")
                                                    node_autore_commento.text = autore
                                                post = requests.get(post['comments']['paging']['next']).json()
                                        except KeyError:
                                             flag=False                    
                                    except KeyError:
                                        pass
                                posts = requests.get(posts['paging']['next']).json()
                            except KeyError:
                                break                                                        
                    except TimeoutException:
                        driver.close() 
        tree = etree.ElementTree(root)
        tree.write(self.output().path)  
