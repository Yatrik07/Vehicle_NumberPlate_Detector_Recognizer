import tensorflow as tf

def create_model():
    model2 = tf.keras.Sequential()

    model2.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, strides=(1, 1), padding="valid", activation='relu',
                                      input_shape=(225, 225, 3)))
    model2.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, strides=(1, 1), padding="valid",
                                      activation='relu'))
    model2.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2)))
    model2.add(tf.keras.layers.BatchNormalization())
    model2.add(tf.keras.layers.Conv2D(filters=128, kernel_size=3, strides=(1, 1), padding="valid",
                                      activation='relu'))
    model2.add(tf.keras.layers.Conv2D(filters=128, kernel_size=3, strides=(1, 1), padding="valid",
                                      activation='relu'))
    model2.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2)))
    model2.add(tf.keras.layers.BatchNormalization())
    model2.add(tf.keras.layers.Conv2D(filters=256, kernel_size=3, strides=(1, 1), padding="valid",
                                      activation='leaky_relu'))
    model2.add(tf.keras.layers.Conv2D(filters=256, kernel_size=3, strides=(1, 1), padding="valid",
                                      activation='leaky_relu'))
    model2.add(tf.keras.layers.Conv2D(filters=256, kernel_size=3, strides=(1, 1), padding="valid",
                                      activation='leaky_relu'))
    model2.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2)))
    model2.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, strides=(1, 1), padding="same",
                                      activation='relu'))
    model2.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, strides=(1, 1), padding="same",
                                      activation='relu'))
    model2.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, strides=(1, 1), padding="same",
                                      activation='relu'))
    model2.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2)))
    model2.add(tf.keras.layers.BatchNormalization())
    model2.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, strides=(1, 1), padding="valid",
                                      activation='relu'))
    model2.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, strides=(1, 1), padding="valid",
                                      activation='relu'))
    model2.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, strides=(1, 1), padding="valid",
                                      activation='relu'))

    model2.add(tf.keras.layers.BatchNormalization())

    model2.add(tf.keras.layers.GlobalAveragePooling2D())
    model2.add(tf.keras.layers.Dropout(0.2))
    model2.add(tf.keras.layers.Dense(256, activation="relu"))
    model2.add(tf.keras.layers.Dropout(0.2))
    model2.add(tf.keras.layers.Dense(64, activation="relu"))

    model2.add(tf.keras.layers.Dense(4))

    model2.compile(optimizer=tf.keras.optimizers.Adam(), loss="mse", metrics="accuracy")


    return model2






