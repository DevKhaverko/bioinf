from prefect import flow

@flow
def my_favorite_function():
    print("Hello world")

my_favorite_function()