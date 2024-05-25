import pandas as pd
from dashvector import Doc
from db.vecdb import VecDB
from utils.conf import Conf


def upload_user_nlp_emb(vecdb):
    df = pd.read_csv("/Users/shijiexu/Downloads/user_nlp.csv")
    docs = []
    for index, row in df.iterrows():
        # print("{} {}".format(index, row['unique_id'], row['embeddings']))
        row_embeddings = row['embeddings'][1:-1].strip().replace("    "," ").replace("   "," ").replace("  "," ").replace("\n","").split(" ")
        embs = []
        try:
            for e in row_embeddings:
                embs.append(float(e))
        except Exception as e:
            print(row_embeddings)
            print(e)
            break
        docs.append(Doc(id=str(index), vector=embs,
                        fields={'id': str(index), 'type': "userid", 'name': row['unique_id']}))
    table = "user_nlp_emb"
    vecdb.upsert(table=table, data=docs, dimension=384)

def upload_vtag_nlp_emb(vecdb):
    df = pd.read_csv("/Users/shijiexu/Downloads/tag_nlp.csv")
    docs = []
    for index, row in df.iterrows():
        # print("{} {}".format(index, row['hashtag_mapped'], row['embeddings'], row['kmeans_100000_batch']))
        row_embeddings = row['embeddings'][1:-1].strip().replace("    "," ").replace("   "," ").replace("  "," ").replace("\n", "").split(" ")
        embs = []
        for e in row_embeddings:
            embs.append(float(e))
        docs.append(Doc(id=str(index), vector=embs,
                        fields={'id': str(index), 'type': "itemid", 'name': row['hashtag_mapped'], 'cluster_id': str(row['kmeans_100000_batch'])}))
    table = "tag_nlp_emb"
    vecdb.upsert(table=table, data=docs, dimension=384, batch=5000)

if __name__ == "__main__":
    print("hello")
    conf = Conf().conf_parse("../conf/conf.yaml")
    vecdb = VecDB(conf['vecdb'])
    vecdb.connect()

    # upload_user_nlp_emb(vecdb)
    upload_vtag_nlp_emb(vecdb)

