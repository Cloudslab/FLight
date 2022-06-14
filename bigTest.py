from core.ml.model.LinearRegression import LinearRegressionFactory

if __name__ == "__main__":
    model = LinearRegressionFactory().LinearRegressionServer(1,1,1,["127.0.0.1",5000])

    model.request_worker(["127.0.0.1",5000])
