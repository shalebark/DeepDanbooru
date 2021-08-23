import tensorflow as tf
import tensorflow_addons as tfa

def load_metrics(metrics, num_classes):
    tf_metrics = [fnc for fnc in dir(tf.keras.metrics) if fnc[0].isupper()]
    tfa_metrics = [fnc for fnc in dir(tfa.metrics) if fnc[0].isupper()]

    # map(lambda metric: getattr(tf.keras.metrics, metric)(), metrics)

    tf_metric_functions = [ getattr(tf.keras.metrics, metric) for metric in metrics if metric in tf_metrics ]
    tfa_metric_functions = [ getattr(tfa.metrics, metric)(num_classes=num_classes) for metric in metrics if metric in tfa_metrics ]

    return tf_metric_functions + tfa_metric_functions

def read_metrics(results, metrics, sep=',\n'):
    sep.join([f'{metric}: {results[i]}' for (i, metric) in enumerate(['Loss'] + metrics) ])
