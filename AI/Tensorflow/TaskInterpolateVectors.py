#############################################################################
#
#   Source from:

#   Forked from:

#   Reimplemented by: Leonel Hernández
#
##############################################################################
import PIL
import imageio.v2 as imageio
from skimage import transform
import test as np
import tensorflow as tf
from PIL.Image import Image

from Helpers.TaskPhotoEnhancer import TaskPhotoEnhancer


def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


def interpolate_hypersphere(v1, v2, num_steps):
    v1_norm = tf.norm(v1)
    v2_norm = tf.norm(v2)
    v2_normalized = v2 * (v1_norm / v2_norm)

    vectors = []
    for step in range(num_steps):
        interpolated = v1 + (v2_normalized - v1) * step / (num_steps - 1)
        interpolated_norm = tf.norm(interpolated)
        interpolated_normalized = interpolated * (v1_norm / interpolated_norm)
        vectors.append(interpolated_normalized)
    return tf.stack(vectors)


model_path = "./models/progan-128"


class TaskInterpolateVectors(TaskPhotoEnhancer):

    def __init__(self, args):
        super().__init__(args)
        self.model = tf.saved_model.load(model_path).signatures['default']
        self.losses = []
        self.image_list = []
        self.latent_dim = 512
        tf.random.set_seed(22)
        self.initial_vector = tf.random.normal([1, self.latent_dim])
        self.num_optimization_steps = 200
        self.steps_per_image = 5

    def interpolate_between_vectors(self):
        v1 = tf.random.normal([self.latent_dim])
        v2 = tf.random.normal([self.latent_dim])
        # Creates a tensor with 25 steps of interpolation between v1 and v2.
        vectors = interpolate_hypersphere(v1, v2, 50)
        # Uses module to generate images from the latent space.
        return self.model(vectors)['default']

    def find_closest_latent_vector(self, target_image, progress):
        vector = tf.Variable(self.initial_vector)
        optimizer = tf.optimizers.Adam(learning_rate=0.01)
        loss_fn = tf.losses.MeanAbsoluteError(reduction="sum")

        for step in range(self.num_optimization_steps):
            if (step % 100) == 0:
                print()
            print('.', end='')
            with tf.GradientTape() as tape:
                image = self.model(vector.read_value())['default'][0]
                if (step % self.steps_per_image) == 0:
                    self.image_list.append(image.numpy())
                    image = tensor_to_image(image)
                    progress.emit(image)
                target_image_difference = loss_fn(image, target_image[:, :, :3])
                # The latent vectors were sampled from a normal distribution. We can get
                # more realistic images if we regularize the length of the latent vector to
                # the average length of vector from this distribution.
                regularizer = tf.abs(tf.norm(vector) - np.sqrt(self.latent_dim))

                loss = target_image_difference + tf.cast(regularizer, tf.float64)
                self.losses.append(loss.numpy())
            grads = tape.gradient(loss, [vector])
            optimizer.apply_gradients(zip(grads, [vector]))

        return self.image_list, self.losses

    def executeEnhanceWork(self, image, progress_callback):
        image = imageio.imread(image)
        image = transform.resize(image, [128, 128])
        image_list, losses = self.find_closest_latent_vector(image, progress_callback)
        last_image = image_list[len(image_list)-1]
        return PIL.Image.fromarray(last_image)
