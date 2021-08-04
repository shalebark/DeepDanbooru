import os
import tensorflow as tf
import deepdanbooru as dd

def measure_project(project_path, use_validation):
    project_context, model, tags = dd.project.load_project(project_path)

    ## loading project configs
    print(f'Loading Project Configs ... ')
    width = project_context['image_width']
    height = project_context['image_height']
    database_path = project_context['database_path']
    minimum_tag_count = project_context['minimum_tag_count']
    # model_type = project_context['model']
    optimizer_type = project_context['optimizer']
    learning_rate = project_context['learning_rate'] if 'learning_rate' in project_context else 0.001
    learning_rates = project_context['learning_rates'] if 'learning_rates' in project_context else None
    minibatch_size = project_context['minibatch_size']
    # epoch_count = project_context['epoch_count']
    # export_model_per_epoch = project_context[
    #     'export_model_per_epoch'] if 'export_model_per_epoch' in project_context else 10
    # checkpoint_frequency_mb = project_context['checkpoint_frequency_mb']
    # console_logging_frequency_mb = project_context['console_logging_frequency_mb']
    rotation_range = project_context['rotation_range']
    scale_range = project_context['scale_range']
    shift_range = project_context['shift_range']
    use_mixed_precision = project_context['mixed_precision'] if 'mixed_precision' in project_context else False
    # checkpoint_path = os.path.join(project_path, 'checkpoints')

    print(f'Loading Optimizer ... ')
    if optimizer_type == 'adam':
        optimizer = tf.optimizers.Adam(learning_rate)
        print('Using Adam optimizer ... ')
    elif optimizer_type == 'sgd':
        optimizer = tf.optimizers.SGD(
            learning_rate, momentum=0.9, nesterov=True)
        print('Using SGD optimizer ... ')
    elif optimizer_type == 'rmsprop':
        optimizer = tf.optimizers.RMSprop(learning_rate)
        print('Using RMSprop optimizer ... ')
    else:
        raise Exception(
            f"Not supported optimizer : {optimizer_type}")

    if use_mixed_precision:
        optimizer = tf.keras.mixed_precision.LossScaleOptimizer(optimizer)
        print('Optimizer is changed to LossScaleOptimizer.')

    print(f'Compiling Model ... ')
    model.compile(optimizer=optimizer, loss=tf.keras.losses.BinaryCrossentropy(),
                  metrics=[
                      tf.keras.metrics.Precision(),
                      tf.keras.metrics.Recall(),
                      tf.keras.metrics.BinaryCrossentropy()
                    ]
                )

    print(f'Loading database ... ')
    image_records = dd.data.load_image_records(
        database_path, minimum_tag_count, use_validation)

    image_paths = [image_record[0]
                    for image_record in image_records]

    tag_strings = [image_record[1]
                    for image_record in image_records]

    dataset_wrapper = dd.data.DatasetWrapper(
        (image_paths, tag_strings), tags, width, height, scale_range=scale_range, rotation_range=rotation_range, shift_range=shift_range)
    dataset = dataset_wrapper.get_dataset(None).batch(minibatch_size)

    results = model.evaluate(dataset)
    print(f'Loss: {results[0]}, Precision: {results[1]}, Recall: {results[2]}')
