from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import Dict, Any
import pandas as pd
import time
import os

# Graph를 만들고 싶은 artifacts를 담고있는 디렉토리로 변경해줘야 함
GRAPHRAG_FOLDER="./ragtest/output/book_session_1/artifacts"


# 전역 변수 선언
driver = None


# 환경변수 설정
def load_env_variables():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
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
        

# Neo4j 쿼리 결과를 Pandas DataFrame으로 변환하는 방법
def db_query(cypher: str, params: Dict[str, Any] = {}) -> pd.DataFrame:
    """Executes a Cypher statement and returns a DataFrame"""
    with driver.session() as session:
        result = session.run(cypher, params)
        # 결과를 Pandas DataFrame으로 변환
        return pd.DataFrame([record.data() for record in result])


# Pandas 데이터프레임을 Neo4j 데이터베이스에 한 번에 일정한 크기만큼씩 가져오기기 위한 코드
def batched_import(statement, df, batch_size=1000):
    """
    Parameters:
    - statement: Cypher 쿼리
    - df : import할 데이터 프레임
    - batch_size : 한 번에 가져올 데이터 행(row) 수, 기본값은 1000
    """
    total = len(df)             # 전체 데이터프레임의 행 수
    start_s = time.time()       # 시작 시간 기록
    for start in range(0,total, batch_size):                # 0부터 total까지 batch_size 간격으로 반복
        batch = df.iloc[start: min(start+batch_size,total)] # 현재 배치에 포함될 데이터프레임의 부분
        # Neo4j에 데이터를 삽입하는 Cypher 쿼리를 실행
        result = driver.execute_query("UNWIND $rows AS value " + statement, 
                                    rows=batch.to_dict('records'),
                                    database_=os.environ["NEO4J_DATABASE"])
        # print(result.summary.counters)                      # 현재 배치에서 적용된 변경 사항 출력
    # print(f'{total} rows in { time.time() - start_s} s.')   # 전체 소요 시간 출력    
    return total  # 처리된 전체 행 수 반환


# Neo4j DB에 여러 제약 조건 생성
def create_constraints():
    statements = """
    create constraint chunk_id if not exists for (c:__Chunk__) require c.id is unique;
    create constraint document_id if not exists for (d:__Document__) require d.id is unique;
    create constraint entity_id if not exists for (c:__Community__) require c.community is unique;
    create constraint entity_id if not exists for (e:__Entity__) require e.id is unique;
    create constraint entity_title if not exists for (e:__Entity__) require e.name is unique;
    create constraint entity_title if not exists for (e:__Covariate__) require e.title is unique;
    create constraint related_id if not exists for ()-[rel:RELATED]->() require rel.id is unique;
    """.split(";")

    for statement in statements:
        if len((statement or "").strip()) > 0:
            # print(statement)
            driver.execute_query(statement)



def import_doc(doc_df) : 
    statement ="""
    MERGE (d:__Document__ {id:value.id})
    SET d += value {.title}
    """

    batched_import(statement, doc_df)


def load_text_units(text_df) : 
    statement = """
    MERGE (c:__Chunk__ {id:value.id})
    SET c += value {.text, .n_tokens}
    WITH c, value
    UNWIND value.document_ids AS document
    MATCH (d:__Document__ {id:document})
    MERGE (c)-[:PART_OF]->(d)
    """

    batched_import(statement, text_df)



def load_nodes(entity_df) :
    entity_statement = """
    MERGE (e:__Entity__ {id:value.id})
    SET e += value {.human_readable_id, .description, name:replace(value.name,'"','')}
    WITH e, value
    CALL db.create.setNodeVectorProperty(e, "description_embedding", value.description_embedding)
    CALL apoc.create.addLabels(e, case when coalesce(value.type,"") = "" then [] else [apoc.text.upperCamelCase(replace(value.type,'"',''))] end) yield node
    UNWIND value.text_unit_ids AS text_unit
    MATCH (c:__Chunk__ {id:text_unit})
    MERGE (c)-[:HAS_ENTITY]->(e)
    """

    batched_import(entity_statement, entity_df)



def import_relationships(rel_df) :
    rel_statement = """
    MATCH (source:__Entity__ {name:replace(value.source,'"','')})
    MATCH (target:__Entity__ {name:replace(value.target,'"','')})
    // not necessary to merge on id as there is only one relationship per pair
    MERGE (source)-[rel:RELATED {id: value.id}]->(target)
    SET rel += value {.rank, .weight, .human_readable_id, .description, .text_unit_ids}
    RETURN count(*) as createdRels
    """

    batched_import(rel_statement, rel_df)



def import_communities(community_df) :
    statement = """
    MERGE (c:__Community__ {community:value.id})
    SET c += value {.level, .title}
    /*
    UNWIND value.text_unit_ids as text_unit_id
    MATCH (t:__Chunk__ {id:text_unit_id})
    MERGE (c)-[:HAS_CHUNK]->(t)
    WITH distinct c, value
    */
    WITH *
    UNWIND value.relationship_ids as rel_id
    MATCH (start:__Entity__)-[:RELATED {id:rel_id}]->(end:__Entity__)
    MERGE (start)-[:IN_COMMUNITY]->(c)
    MERGE (end)-[:IN_COMMUNITY]->(c)
    RETURN count(distinct c) as createdCommunities
    """

    batched_import(statement, community_df)



def import_community_reports(community_report_df) :
    community_statement = """
    MERGE (c:__Community__ {community:value.community})
    SET c += value {.level, .title, .rank, .rank_explanation, .full_content, .summary}
    WITH c, value
    UNWIND range(0, size(value.findings)-1) AS finding_idx
    WITH c, value, finding_idx, value.findings[finding_idx] as finding
    MERGE (c)-[:HAS_FINDING]->(f:Finding {id:finding_idx})
    SET f += finding
    """
    batched_import(community_statement, community_report_df)


def main():
    load_env_variables()    # 환경 변수
    initialize_neo4j()      # neo4j DB 연결
    delete_all_nodes()      # 모든 노드 삭제
    create_constraints()    # Neo4j DB에 여러 제약 조건 생성
    

    # import documents
    doc_df = pd.read_parquet(f'{GRAPHRAG_FOLDER}/create_final_documents.parquet', columns=["id", "title"])    
    import_doc(doc_df)


    # loading text units
    text_df = pd.read_parquet(f'{GRAPHRAG_FOLDER}/create_final_text_units.parquet',
                            columns=["id","text","n_tokens","document_ids"])
    load_text_units(text_df)


    # loading nodes
    entity_df = pd.read_parquet(f'{GRAPHRAG_FOLDER}/create_final_entities.parquet',
                                columns=["name","type","description","human_readable_id","id","description_embedding","text_unit_ids"])
    load_nodes(entity_df)


    # import relationships
    rel_df = pd.read_parquet(f'{GRAPHRAG_FOLDER}/create_final_relationships.parquet',
                            columns=["source","target","id","rank","weight","human_readable_id","description","text_unit_ids"])
    import_relationships(rel_df)
    

    # import communities
    community_df = pd.read_parquet(f'{GRAPHRAG_FOLDER}/create_final_communities.parquet', 
                    columns=["id","level","title","text_unit_ids","relationship_ids"])
    import_communities(community_df)


    community_report_df = pd.read_parquet(f'{GRAPHRAG_FOLDER}/create_final_community_reports.parquet',
                            columns=["id","community","level","title","summary", "findings","rank","rank_explanation","full_content"])
    import_community_reports(community_report_df)




if __name__ == "__main__":
    main()