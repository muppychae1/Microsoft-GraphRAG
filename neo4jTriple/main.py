from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import Dict, Any
import pandas as pd
import time
import os

FILE_PATH="./neo4jTriple/data/triple.csv"


# 전역 변수 선언
driver = None


# 환경변수 설정
def load_env_variables():
    load_dotenv()
    os.environ["NEO4J_URI"] = os.getenv("NEO4J_URI")
    os.environ["NEO4J_USERNAME"] = os.getenv("NEO4J_USERNAME")
    os.environ["NEO4J_PASSWORD"] = os.getenv("NEO4J_PASSWORD")
    os.environ["NEO4J_DATABASE"] = os.getenv("NEO4J_DATABASE")


# Neo4j 연결
def initialize_neo4j():
    global driver 
    uri = os.environ["NEO4J_URI"]
    username = os.environ["NEO4J_USERNAME"]
    password = os.environ["NEO4J_PASSWORD"]
    driver = GraphDatabase.driver(uri, auth=(username, password))


# 모든 노드를 삭제하는 함수 추가
def delete_all_nodes():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        print("All nodes and relationships deleted.")


# CSV 파일 읽고, 데이터를 Neo4j에 저장하는 함수
def load_csv_and_store_to_neo4j():
    # CSV 파일을 읽음
    df = pd.read_csv(FILE_PATH, encoding='utf-8')
    
    with driver.session() as session:
        for index, row in df.iterrows():
            subject = row['subject']
            predicate = row['predicate']
            object_ = row['object']
            
            # Cypher 쿼리 실행: subject, object는 노드로, predicate는 관계로 저장
            query = (
                "MERGE (a:Image {name: $subject}) "
                "MERGE (b:Entity {name: $object}) "
                f"MERGE (a)-[r:{predicate}]->(b)"
            )
            
            session.run(query, subject=subject, predicate=predicate, object=object_)
            print(f"Processed triple: ({subject})-[:{predicate}]->({object_})")
            
        print("All triples have been stored in Neo4j.")


def main():
    load_env_variables()    # 환경 변수
    initialize_neo4j()      # neo4j DB 연결
    delete_all_nodes()      # 모든 노드 삭제
    load_csv_and_store_to_neo4j()


if __name__ == "__main__":
    main()