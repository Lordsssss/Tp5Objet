import sqlite3

dbName = "database.db"


def connexionDB():
    global connexion
    try:
        connexion = sqlite3.connect(dbName)
    except sqlite3.Error as error:
        print("connexion error",error)

def fermetureDB():
    if connexion:
        connexion.close()
    else:
        print("error fermeture")

def verifierExisteTable(table):
    existe = False
    cur = connexion.cursor()
    
    sql_tableExiste = "SELECT count(name) FROM sqlite_master WHERE type=? AND name=?"
    
    try:
        cur.execute(sql_tableExiste, ('table', table))
        
        if cur.fetchone()[0]==1:
            existe = True
        else:
            existe = False
    except sqlite3.Error as error:
        print("database table check",error)
    
    return existe

def creationTable():
    table = """CREATE TABLE USER(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nfcId INTEGER,
            username TEXT NOT NULL,
            creationDate TEXT NOT NULL,
            description TEXT NOT NULL );"""
    
    connexionDB()
    
    if verifierExisteTable("USER"):
        print("table existe deja")
    else:
        try:
            connexion.execute(table)
        except sqlite3.Error as error:
            print("creation table ",error)
    
    fermetureDB()

def ajouterUser(nfcId,username,creationData,description):
    sql_insert = "INSERT INTO USER (nfcId,username,creationDate,description) VALUES(?,?,?,?)"
    
    connexionDB()
    
    try:
        cur_insert = connexion.cursor()
        donnees_param = (nfcId,username,creationData,description)
        cur_insert.execute(sql_insert,donnees_param)
        connexion.commit()
        cur_insert.close()
    except sqlite3.Error as error:
        print("insert error", error)
    finally:
        fermetureDB()

def selectionListeUser():
    slq_select = "SELECT username FROM USER"
    
    connexionDB()
    try:
        cur_select = connexion.cursor()
        cur_select.execute(slq_select)
        data = cur_select.fetchall()
    except sqlite3.Error as error:
        print("selection error",error)
    finally:
        fermetureDB()
    return data

def verifierNfcId(nfcId):
    sql_select = "SELECT 1 FROM USER WHERE nfcId=? LIMIT 1"
    
    connexionDB()
    
    try:
        cur_select = connexion.cursor()
        cur_select.execute(sql_select, (nfcId,))
        data = cur_select.fetchone()
        if data is None:
            return False
        else:
            return True
    except sqlite3.Error as error:
        print("verification error", error)
    finally:
        fermetureDB()
        