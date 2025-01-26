import pandas as pd
import weaviate
import weaviate.classes as wvc
import ast

excel_file_path = "output/output.xlsx"
df = pd.read_excel(excel_file_path)
df_filtered = df[['doc_id', 'Title', 'Chunk', 'Processed Chunk Embeddings']]
# Convert the filtered DataFrame to a list of dictionaries
list_of_dicts = df_filtered.to_dict(orient='records')

client = weaviate.connect_to_local()
client.collections.delete("TestTable_3")
# Create the collection, Weaviate's autoschema feature will infer properties when importing.
test = client.collections.create(
    "TestTable_3",
    vectorizer_config=wvc.config.Configure.Vectorizer.none()
)
client.close()

def question_objs(list_of_dicts):
    question_objs_list = list()
    for i, d in enumerate(list_of_dicts):
        question_objs_list.append(wvc.data.DataObject(
            properties={
                "doc_id": d["doc_id"],
                "Title": d["Title"],
                "text": d["Chunk"],
            },
            vector=ast.literal_eval(d["Processed Chunk Embeddings"])
        ))
    return question_objs_list

client = weaviate.connect_to_local()

collection = client.collections.get("TestTable_3")
collection.data.insert_many(question_objs(list_of_dicts))
client.close()
