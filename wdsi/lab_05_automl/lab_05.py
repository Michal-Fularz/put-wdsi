from tpot import TPOTClassifier
from sklearn.datasets import load_digits, load_iris, load_wine, load_diabetes, load_breast_cancer
from sklearn.model_selection import train_test_split

import pandas as pd
from lightautoml.automl.presets.tabular_presets import TabularAutoML
from lightautoml.tasks import Task

from autogluon.tabular import TabularPredictor

import h2o
from h2o.automl import H2OAutoML

from bluecast.blueprints.cast import BlueCast


def tpot_iris():
    dataset = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(dataset.data, dataset.target,
                                                        random_state=42,
                                                        train_size=0.75, test_size=0.25, stratify=dataset.targer)

    pipeline_optimizer = TPOTClassifier(generations=5, population_size=20, cv=5,
                                        random_state=42, verbosity=2)
    pipeline_optimizer.fit(X_train, y_train)
    print(pipeline_optimizer.score(X_test, y_test))
    print(pipeline_optimizer.fitted_pipeline_)
    pipeline_optimizer.export('tpot_exported_pipeline.py')


def tpot_digits():
    digits = load_digits()
    X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, random_state=42,
                                                        train_size=0.75, test_size=0.25)

    pipeline_optimizer = TPOTClassifier(generations=5, population_size=20, cv=5,
                                        random_state=42, verbosity=2)
    pipeline_optimizer.fit(X_train, y_train)
    print(pipeline_optimizer.score(X_test, y_test))
    print(pipeline_optimizer.fitted_pipeline_)
    pipeline_optimizer.export('tpot_exported_pipeline.py')


def lightautoml_iris():
    # Load the IRIS dataset
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    # Combine training features and target into a single DataFrame for LightAutoML
    train_data = X_train.copy()
    train_data['target'] = y_train

    test_data = X_test.copy()
    test_data['target'] = y_test

    # Initialize the LightAutoML automl model
    automl = TabularAutoML(task=Task('multiclass'), timeout=300)  # Set timeout for model training in seconds

    # Train the model on the training data
    automl.fit_predict(train_data, roles={'target': 'target'}, verbose=3)

    # Evaluate on the test set
    predictions = automl.predict(test_data)
    predictions_df = predictions.to_pandas()
    print(automl.create_model_str_desc())
    print(predictions)

    # print("Predictions:\n", predictions_df.head())

    return automl, predictions_df


def autogluon_wine():
    dataset = load_iris()
    X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    y = dataset.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    # Combine training features and target into a single DataFrame for AutoGluon
    train_data = X_train.copy()
    train_data['target'] = y_train

    test_data = X_test.copy()
    test_data['target'] = y_test

    # Initialize the AutoGluon TabularPredictor
    predictor = TabularPredictor(label='target', problem_type='multiclass')

    # Train the model on the training data
    predictor.fit(train_data, presets='high_quality', time_limit=300)

    leaderboard = predictor.leaderboard(test_data)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(leaderboard)

    # predictor.plot_ensemble_model()

    # Evaluate on the test set
    predictions = predictor.predict(test_data.drop(columns=['target']))
    accuracy = predictor.evaluate_predictions(y_true=test_data['target'], y_pred=predictions)

    print("\nPredictions:\n", predictions.head())
    print("\nAccuracy:\n", accuracy)

    return predictor


def h2o_iris():
    # Initialize the H2O server
    h2o.init()

    # Load the IRIS dataset
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    # Combine training features and target into a single DataFrame
    train_data = X_train.copy()
    train_data['target'] = y_train

    test_data = X_test.copy()
    test_data['target'] = y_test

    # Convert the data to H2O Frames
    train_h2o = h2o.H2OFrame(train_data)
    test_h2o = h2o.H2OFrame(test_data)

    # Set the target column as categorical for classification
    train_h2o['target'] = train_h2o['target'].asfactor()
    test_h2o['target'] = test_h2o['target'].asfactor()

    # Define the features and target
    x = train_data.columns[:-1].tolist()
    y = 'target'

    # Run H2O AutoML
    aml = H2OAutoML(max_runtime_secs=300, seed=42)  # Set a timeout of 300 seconds
    aml.train(x=x, y=y, training_frame=train_h2o)

    # View the leaderboard
    leaderboard = aml.leaderboard
    print("\nLeaderboard:\n", leaderboard)

    # Make predictions on the test data
    predictions = aml.leader.predict(test_h2o)
    print("\nPredictions:\n", predictions.head())

    # Shut down the H2O server
    h2o.shutdown(prompt=False)

    return aml


def bluecast_hello_world():
    from bluecast.blueprints.welcome import WelcomeToBlueCast

    welcome = WelcomeToBlueCast()
    welcome.automl_configurator()

    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target

    # Combine features and target into a single DataFrame
    data = X.copy()
    data['target'] = y

    # Split the data into training and testing sets
    train_data, test_data = train_test_split(data, test_size=0.25, random_state=42, stratify=data['target'])

    # here users can chose from the given options and click 'submit' to create the instance
    # after submit the automl instance can be retrieved and used like:
    automl = welcome.automl_instance
    automl.fit(train_data, target_col="target")
    y_hat = automl.predict(test_data)


def bluecast_iris():
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target

    # Combine features and target into a single DataFrame
    data = X.copy()
    data['target'] = y

    # Split the data into training and testing sets
    train_data, test_data = train_test_split(data, test_size=0.25, random_state=42, stratify=data['target'])

    # Initialize the BlueCast AutoML model
    automl = BlueCast(class_problem="multiclass")

    # Train the model on the training data
    automl.fit(train_data, target_col="target")

    # Make predictions on the test data
    y_probs, y_classes = automl.predict(test_data.drop(columns=['target']))

    # Display the first few predictions
    print("Predicted probabilities:\n", y_probs)
    print("Predicted classes:\n", y_classes)

    return automl



if __name__ == "__main__":
    # tpot_iris()
    # tpot_digits()
    # lightautoml_iris()
    # autogluon_wine()
    # h2o_iris()
    # bluecast_hello_world()
    bluecast_iris()
