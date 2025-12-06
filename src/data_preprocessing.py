import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import (
    TRAIN_FILE_PATH,
    TEST_FILE_PATH,
    PROCESSED_DIR,
    CONFIG_PATH,
    PROCESSED_TRAIN_FILE_PATH,
    PROCESSED_TEST_FILE_PATH
)
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)


class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)
        self.label_encoder = LabelEncoder()

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    # ============================================================
    def preprocess_data(self, df):
        """Cleans the dataset, removes duplicates, encodes categories, and handles skewness."""

        try:
            logger.info("Starting Data Preprocessing")

            df.drop(columns=['Booking_ID'], inplace=True, errors='ignore')
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            # ---- Label Encoding ----
            logger.info("Applying Label Encoding")
            mappings = {}

            for col in cat_cols:
                df[col] = self.label_encoder.fit_transform(df[col].astype(str))

                mappings[col] = {
                    label: code for label, code in zip(
                        self.label_encoder.classes_,
                        self.label_encoder.transform(self.label_encoder.classes_)
                    )
                }

            logger.info("Label Encoding Mappings:")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            # ---- Handle Skewness ----
            logger.info("Handling Skewness")
            skew_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x: x.skew())

            for col in skewness[skewness > skew_threshold].index:
                df[col] = np.log1p(df[col])

            logger.info("Preprocessing Completed")
            return df

        except Exception as e:
            logger.error(f"Error in Preprocessing: {e}")
            raise CustomException("Data Preprocessing Failed", e)

    # ============================================================
    def balance_data(self, df):
        """Balances the training dataset using SMOTE."""

        try:
            logger.info("Applying SMOTE (Only to Training Data)")
            X = df.drop(columns='booking_status')
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info("SMOTE Balancing Completed")
            return balanced_df

        except Exception as e:
            logger.error(f"Error in SMOTE Balancing: {e}")
            raise CustomException("Balancing Data Failed", e)

    # ============================================================
    def select_features(self, df):
        """Selects the top N most important features using Random Forest."""

        try:
            logger.info("Selecting Top Features Using Random Forest")

            X = df.drop(columns='booking_status')
            y = df['booking_status']

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importances = model.feature_importances_

            feature_importances_df = pd.DataFrame({
                'Feature': X.columns,
                'Importance': feature_importances
            })

            feature_importances_df = feature_importances_df.sort_values(
                by='Importance', ascending=False
            )

            num_features = self.config['data_processing']['no_of_features']

            top_features = feature_importances_df['Feature'].head(num_features).values

            logger.info(f"Top {num_features} Features: {top_features}")

            selected_df = df[list(top_features) + ['booking_status']]

            logger.info("Feature Selection Completed")

            return selected_df

        except Exception as e:
            logger.error(f"Error in Feature Selection: {e}")
            raise CustomException("Feature Selection Failed", e)

    # ============================================================
    def save_data(self, df, file_path):
        """Saves the processed dataset."""

        try:
            df.to_csv(file_path, index=False)
            logger.info(f"Data Saved Successfully at: {file_path}")

        except Exception as e:
            logger.error(f"Error Saving Data: {e}")
            raise CustomException("Saving Data Failed", e)

    # ============================================================
    def process(self):
        """Main end-to-end data preprocessing pipeline."""

        try:
            logger.info("Loading Train and Test Data")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            # ---- Preprocess ----
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            # ---- SMOTE only on train ----
            train_df = self.balance_data(train_df)

            # ---- Feature Selection ----
            train_df = self.select_features(train_df)

            # Match test data to selected features
            test_df = test_df[train_df.columns]

            # ---- Save Outputs ----
            self.save_data(train_df, PROCESSED_TRAIN_FILE_PATH)
            self.save_data(test_df, PROCESSED_TEST_FILE_PATH)

            logger.info("Data Preprocessing Pipeline Completed Successfully")

        except Exception as e:
            logger.error(f"Pipeline Error: {e}")
            raise CustomException("Data Preprocessing Pipeline Failed", e)


# ============================================================
if __name__ == "__main__":
    processor = DataProcessor(
        TRAIN_FILE_PATH,
        TEST_FILE_PATH,
        PROCESSED_DIR,
        CONFIG_PATH
    )
    processor.process()
