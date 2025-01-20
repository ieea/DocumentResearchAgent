import weaviate
import weaviate.classes.config as wc

class WeaviateManager:
    def __init__(self, name):
        self.client = weaviate.connect_to_local()
        self.name = name

    def create_class(self, properties):
        try:
            self.client.collections.create(
                name=self.name,
                properties= properties,
                vectorizer_config=wc.Configure.Vectorizer.none(),
                vector_index_config=wc.Configure.VectorIndex.hnsw()
            )
        except Exception as e:
            print(f"Error creating class: {e}")

    def delete_class(self):
        try:
            self.client.collections.delete(self.name)
        except Exception as e:
            print(f"Error deleting class: {e}")

    def close_connection(self):
        self.client.close()

    def get_class(self):
        return self.client.collections.get(self.name)

    def read_all_objects(self):
        collection = self.client.collections.get(self.name)
        for item in collection.iterator(
            include_vector=False) :
            print(item.properties)
            print(item.vector)
        return item.properties, item.vector
    
    def read_object(self):
        collection = self.client.collections.get(self.name)
        for item in collection.iterator():
            print(item.properties)
        #return collection.get(uuid)

def main():
    # Define properties
    properties = [
        wc.Property(name="title", data_type=wc.DataType.TEXT),
        wc.Property(name="content", data_type=wc.DataType.TEXT),
        wc.Property(name="date", data_type=wc.DataType.DATE),
        wc.Property(name="doc_id", data_type=wc.DataType.INT)
    ]
    # intialize name
    name = "Test_Documents_2"
    # Create an instance of WeaviateManager with properties
    manager = WeaviateManager(name)
    
    try:
        assert manager.client.is_live()
        manager.create_class(properties)
        #manager.delete_class()  # Uncomment if you want to delete the class
        #manager.read_all_objects()
        #manager.read_object()
    finally:
        manager.close_connection()

if __name__ == "__main__":
    main()