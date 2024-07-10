import requests
import psycopg2

def create_database():
    # Conectar ao banco de dados
    conn = psycopg2.connect(
        database="champions",
        user="postgres",
        password="insertpassword", #trocar senha
        host="127.0.0.1",
        port="5432"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Dropar e criar a tabela
    cursor.execute("DROP TABLE IF EXISTS CHAMPIONS")
    
    sql = ''' 
    CREATE TABLE CHAMPIONS(
        NAME CHAR(20) NOT NULL,
        ROLES CHAR(30), 
        TITLE CHAR(40)   
    )
    '''
    cursor.execute(sql)
    conn.close()

def check_duplicate(cursor, name):
    cursor.execute("SELECT 1 FROM CHAMPIONS WHERE NAME = %s", (name,))
    return cursor.fetchone() 

def get_champion_data():
    url = "https://ddragon.leagueoflegends.com/cdn/14.13.1/data/pt_BR/champion.json"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        champions = data['data']
        
        # Conectar ao banco de dados
        conn = psycopg2.connect(
            database="champions",
            user="postgres",
            password="1311",
            host="127.0.0.1",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Inserir dados na tabela
        for champ_name, champ_info in champions.items():
            name = champ_info['name']
            title = champ_info['title']
            roles = ', '.join(champ_info['tags'])
            
            if not check_duplicate(cursor, name):
                cursor.execute(
                    "INSERT INTO CHAMPIONS (NAME, ROLES, TITLE) VALUES (%s, %s, %s)",
                    (name, roles, title)
                )
            else:
                print(f"Erro ao adicionar: {name}. Campeão já adicionado.")

        cursor.close()
        conn.close()
        
        print("OK!!!!!!!!!!!")
    else:
        print(f"Falha ao conectar. Erro: {response.status_code}")

create_database()  # Cria a tabela no banco de dados
get_champion_data()  # Obtém e insere os dados dos campeões
