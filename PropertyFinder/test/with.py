class ManagedResource:
    def __enter__(self):
        print("Setting up the resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Cleaning up the resource")

with ManagedResource() as resource:
    print("Doing something with the resource")