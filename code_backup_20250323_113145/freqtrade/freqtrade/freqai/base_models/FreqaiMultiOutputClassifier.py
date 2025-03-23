# REMOVED_UNUSED_CODE: import numpy as np
# REMOVED_UNUSED_CODE: from sklearn.base import is_classifier
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from sklearn.multioutput import MultiOutputClassifier, _fit_estimator
# REMOVED_UNUSED_CODE: from sklearn.utils.multiclass import check_classification_targets
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from sklearn.utils.parallel import Parallel, delayed
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from sklearn.utils.validation import has_fit_parameter, validate_data

# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException


# REMOVED_UNUSED_CODE: class FreqaiMultiOutputClassifier(MultiOutputClassifier):
# REMOVED_UNUSED_CODE:     def fit(self, X, y, sample_weight=None, fit_params=None):
# REMOVED_UNUSED_CODE:         """Fit the model to data, separately for each output variable.
# REMOVED_UNUSED_CODE:         Parameters
# REMOVED_UNUSED_CODE:         ----------
# REMOVED_UNUSED_CODE:         X : {array-like, sparse matrix} of shape (n_samples, n_features)
# REMOVED_UNUSED_CODE:             The input data.
# REMOVED_UNUSED_CODE:         y : {array-like, sparse matrix} of shape (n_samples, n_outputs)
# REMOVED_UNUSED_CODE:             Multi-output targets. An indicator matrix turns on multilabel
# REMOVED_UNUSED_CODE:             estimation.
# REMOVED_UNUSED_CODE:         sample_weight : array-like of shape (n_samples,), default=None
# REMOVED_UNUSED_CODE:             Sample weights. If `None`, then samples are equally weighted.
# REMOVED_UNUSED_CODE:             Only supported if the underlying classifier supports sample
# REMOVED_UNUSED_CODE:             weights.
# REMOVED_UNUSED_CODE:         fit_params : A list of dicts for the fit_params
# REMOVED_UNUSED_CODE:             Parameters passed to the ``estimator.fit`` method of each step.
# REMOVED_UNUSED_CODE:             Each dict may contain same or different values (e.g. different
# REMOVED_UNUSED_CODE:             eval_sets or init_models)
# REMOVED_UNUSED_CODE:             .. versionadded:: 0.23
# REMOVED_UNUSED_CODE:         Returns
# REMOVED_UNUSED_CODE:         -------
# REMOVED_UNUSED_CODE:         self : object
# REMOVED_UNUSED_CODE:             Returns a fitted instance.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not hasattr(self.estimator, "fit"):
# REMOVED_UNUSED_CODE:             raise ValueError("The base estimator should implement a fit method")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         y = validate_data(self, X="no_validation", y=y, multi_output=True)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if is_classifier(self):
# REMOVED_UNUSED_CODE:             check_classification_targets(y)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if y.ndim == 1:
# REMOVED_UNUSED_CODE:             raise ValueError(
# REMOVED_UNUSED_CODE:                 "y must have at least two dimensions for multi-output regression but has only one."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if sample_weight is not None and not has_fit_parameter(self.estimator, "sample_weight"):
# REMOVED_UNUSED_CODE:             raise ValueError("Underlying estimator does not support sample weights.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not fit_params:
# REMOVED_UNUSED_CODE:             fit_params = [None] * y.shape[1]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.estimators_ = Parallel(n_jobs=self.n_jobs)(
# REMOVED_UNUSED_CODE:             delayed(_fit_estimator)(self.estimator, X, y[:, i], sample_weight, **fit_params[i])
# REMOVED_UNUSED_CODE:             for i in range(y.shape[1])
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.classes_ = []
# REMOVED_UNUSED_CODE:         for estimator in self.estimators_:
# REMOVED_UNUSED_CODE:             self.classes_.extend(estimator.classes_)
# REMOVED_UNUSED_CODE:         if len(set(self.classes_)) != len(self.classes_):
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 f"Class labels must be unique across targets: {self.classes_}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if hasattr(self.estimators_[0], "n_features_in_"):
# REMOVED_UNUSED_CODE:             self.n_features_in_ = self.estimators_[0].n_features_in_
# REMOVED_UNUSED_CODE:         if hasattr(self.estimators_[0], "feature_names_in_"):
# REMOVED_UNUSED_CODE:             self.feature_names_in_ = self.estimators_[0].feature_names_in_
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return self
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def predict_proba(self, X):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get predict_proba and stack arrays horizontally
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         results = np.hstack(super().predict_proba(X))
# REMOVED_UNUSED_CODE:         return np.squeeze(results)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def predict(self, X):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get predict and squeeze into 2D array
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         results = super().predict(X)
# REMOVED_UNUSED_CODE:         return np.squeeze(results)
