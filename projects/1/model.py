from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV

#
# Dataset fields
#


#
# Model pipeline
#

# We create the preprocessing pipelines for both numeric and categorical data.
numeric_features = ["if"+str(i) for i in range(1,14)]
# list_cat = [6, 9, 13, 16, 17, 19, 25, 26]
categorical_features = ["cf"+str(i) for i in range(1,27)] + ["day_number"]

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
#    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

fields = ["id", "label"] + numeric_features + categorical_features
fields_val = ["id"] + numeric_features + categorical_features

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

w = {0:97, 1:3}

# Now we have a full prediction pipeline.
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('logregression', LogisticRegression(class_weight=w, penalty = 'l1', solver='liblinear', C = 0.7))
])

