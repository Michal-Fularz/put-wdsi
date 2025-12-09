from sklearn.datasets import load_digits, load_iris, load_wine, load_diabetes, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

from autogluon.tabular import TabularPredictor
#
# from tpot import TPOTClassifier
#
# from bluecast.blueprints.cast import BlueCast
#
# from lightautoml.automl.presets.tabular_presets import TabularAutoML
# from lightautoml.tasks import Task
#
# import h2o
# from h2o.automl import H2OAutoML


def visualize_confusion_matrix_sklearn(conf_matrix, target_names):
    # Ensure target_names is a list of strings if coming from numerical labels
    display_labels = [str(name) for name in target_names]

    # Create a ConfusionMatrixDisplay object
    disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=display_labels)

    # Plot the confusion matrix
    fig, ax = plt.subplots(figsize=(8, 6))
    disp.plot(cmap=plt.cm.Blues, ax=ax, values_format='d')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()


def visualize_feature_importance(feature_importance_df):
    # Ensure the DataFrame has 'feature' and 'importance' columns
    # Resetting index if feature names are in the index
    if feature_importance_df.index.name == 'feature':  # Check if the index is already named 'feature'
        feature_importance_df = feature_importance_df.reset_index()
    elif 'feature' not in feature_importance_df.columns and feature_importance_df.index.name is None:
        # If index is unnamed, assume it holds the feature names and reset
        feature_importance_df = feature_importance_df.reset_index()
        feature_importance_df = feature_importance_df.rename(
            columns={'index': 'feature'})  # Rename default index column
    # Sort features by importance score
    feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance_df, palette='viridis')
    plt.title('Feature Importance')
    plt.xlabel('Importance Score')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.show()



def sklearn():
    dataset = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, random_state=42, test_size=0.2#, stratify=dataset.target
    )
    print(y_test)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f'{acc=}')

def todo_0():
    print("--- Executing TODO 0 ---")

    # 1. Load the Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target

    print("\nDataset Chosen: Iris")
    print("What it contains:", iris.DESCR)
    print("Number of features:", X.shape[1])

    # 2. Split the data into training and test sets (80% train, 20% test)
    # random_state is used for reproducibility. If you use the same random_state value,
    # you will get the same train and test datasets every time you run the split.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"\nShape of X_train: {X_train.shape}")
    print(f"Shape of X_test: {X_test.shape}")
    print(f"Shape of y_train: {y_train.shape}")
    print(f"Shape of y_test: {y_test.shape}")

    return X_train, X_test, y_train, y_test, iris.feature_names, iris.target_names


def todo_1(X_train, X_test, y_train, y_test, feature_names, target_names):
    print("--- Executing TODO 1 ---")

    # Convert numpy arrays to pandas DataFrames for AutoGluon
    # AutoGluon expects a DataFrame with the target column included in the training data
    train_df = pd.DataFrame(X_train, columns=feature_names)
    train_df['asd'] = y_train

    test_df = pd.DataFrame(X_test, columns=feature_names)
    test_df['target'] = y_test  # Include target for leaderboard evaluation

    label_column = 'target'
    problem_type = 'multiclass'  # Iris is a multiclass classification problem

    # 1. Create a TabularPredictor object
    # verbosity=2 provides more detailed output during fitting
    predictor = TabularPredictor(
        label=label_column,
        problem_type=problem_type,
        verbosity=2,  # Default is 2, higher values (e.g., 4) show more details
        path='AutogluonModels'
    )

    # 2. Call the fit method
    # preset='medium_quality' is a good starting point for comparison
    # time_limit can be added, e.g., time_limit=3600 (for 1 hour)
    predictor.fit(
        train_data=train_df,
        presets='medium_quality',  # 'best_quality', 'high_quality', 'medium_quality', 'fast_inference'
        # time_limit=60, # Optional: limit training time to X seconds
        verbosity=2
    )

    # 3. Call leaderboard to see developed models and their results
    # Passing test_df will evaluate models on the test set
    leaderboard = predictor.leaderboard(test_df, silent=True)
    print("\nLeaderboard on test data:")
    print(leaderboard)

    # Get the best score
    best_model_score = leaderboard['score_test'].iloc[0]
    print(f"\nBest model test score: {best_model_score:.4f}")

    # The leaderboard shows validation scores (val) and test scores.
    # They are generally not identical because validation is performed on a subset of the training data
    # (or through cross-validation), while the test score is on unseen data.
    # Differences can highlight overfitting to the validation set or different data distributions.

    return predictor, best_model_score


def todo_1_1():
    print("--- Executing TODO 1.1 ---")

    # Load the Wine dataset
    wine = load_wine()
    X, y = wine.data, wine.target
    # Print info
    print("\nDataset Chosen: Wine Recognition")
    print("What it contains:", wine.DESCR)
    print("Number of features:", X.shape[1])

    # Split the data into training and test sets (80% train, 20% test)
    random_state_val = 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state_val)

    print(f"\nShape of X_train: {X_train.shape}")
    print(f"Shape of X_test: {X_test.shape}")

    # Convert numpy arrays to pandas DataFrames for AutoGluon
    feature_names = wine.feature_names
    target_names = wine.target_names

    train_df = pd.DataFrame(X_train, columns=feature_names)
    train_df['target'] = y_train

    test_df = pd.DataFrame(X_test, columns=feature_names)
    test_df['target'] = y_test # Include target for leaderboard evaluation and prediction

    label_column = 'target'
    problem_type = 'multiclass' # Wine is a multiclass classification problem

    # Create and fit TabularPredictor
    predictor_wine = TabularPredictor(
        label=label_column,
        problem_type=problem_type,
        verbosity=2,
        path='AutogluonModels_Wine' # Separate path for Wine dataset models
    )

    print("\nFitting AutoGluon model for Wine dataset...")
    predictor_wine.fit(
        train_data=train_df,
        presets='medium_quality',
        # time_limit=60, # Uncomment to limit training time
        verbosity=2
    )

    # Display leaderboard for comparison
    print("\nLeaderboard on Wine test data:")
    leaderboard_wine = predictor_wine.leaderboard(test_df, silent=True)
    print(leaderboard_wine)

    best_model_score_wine = leaderboard_wine['score_test'].iloc[0]
    print(f"\nBest model test score from leaderboard: {best_model_score_wine:.4f}")

    # Calculate and display additional metrics using sklearn.metrics

    # Use the predict method on the test set
    print("\nMaking predictions on the test set...")
    y_pred = predictor_wine.predict(test_df.drop(columns=[label_column]))
    y_true = test_df[label_column]

    print("\n--- Sklearn Metrics for Wine Dataset ---")
    accuracy = accuracy_score(y_true, y_pred)
    # For multiclass, precision, recall, f1_score need 'average' parameter
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    conf_matrix = confusion_matrix(y_true, y_pred)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision (weighted): {precision:.4f}")
    print(f"Recall (weighted): {recall:.4f}")
    print(f"F1-score (weighted): {f1:.4f}")
    print("Confusion Matrix:")
    print(conf_matrix)
    visualize_confusion_matrix_sklearn(conf_matrix, target_names)

    # --- TODO 1.2: Feature Importance ---
    print("\n--- Feature Importance Analysis (TODO 1.2) ---")
    # Get feature importance for the best model
    feature_importance = predictor_wine.feature_importance(test_df)
    print("\nFeature Importance (Full list):\n", feature_importance)

    print("\nTop 5 Features:\n", feature_importance.head(5))

    visualize_feature_importance(feature_importance)

    return predictor_wine, y_pred, y_true, {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': conf_matrix.tolist() # Convert numpy array to list for easier output
    }


def leaderboard_featiure_importance_explanation():
    # Compare metrics with leaderboard result
    print("\n--- Comparison and Reflection ---")
    print(f"Leaderboard score (typically accuracy or F1): {best_model_score_wine:.4f}")
    print(f"Calculated Accuracy: {accuracy:.4f}")
    print("Differences might arise from:")
    print(
        "- Leaderboard might use a default metric (e.g., accuracy, F1) that aligns with 'accuracy_score' or 'f1_score'.")
    print(
        "- AutoGluon's internal scoring during leaderboard generation might use slightly different rounding or a "
        "specific average method for multiclass problems (e.g., micro, macro, weighted). Here we used 'weighted' "
        "average for precision, recall, and F1 which is generally suitable for imbalanced datasets.")
    print(
        "- The 'score_test' on the leaderboard usually reflects the primary evaluation metric AutoGluon optimizes for, "
        "which for multiclass classification is often accuracy or log_loss. If it was optimizing for log_loss, then the "
        "direct comparison to accuracy would show differences.")

    print("\nReflection on Feature Importance:")
    print("The feature importance helps to identify which characteristics of the wine (e.g., alcohol, malic_acid) "
          "are most influential in predicting its class. Comparing these numerical insights with any prior knowledge or "
          "visual explorations of the dataset can provide valuable understanding into the underlying data patterns and "
          "model's decision-making process."
    )


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


def autogluon():
    dataset = load_iris()
    X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    y = dataset.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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
    pd.set_option('display.max_columns', None)

    # X_train, X_test, y_train, y_test, feature_names, target_names = todo_0()
    # predictor, best_score_todo1 = todo_1(X_train, X_test, y_train, y_test, feature_names, target_names)

    predictor_wine_1_1, predictions_1_1, true_labels_1_1, metrics_1_1 = todo_1_1()


    # sklearn()
    # autogluon()
    # tpot_iris()
    # tpot_digits()
    # lightautoml_iris()
    # h2o_iris()
    # bluecast_hello_world()
    # bluecast_iris()
