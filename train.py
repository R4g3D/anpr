import os
import sys

CUSTOM_MODEL_NAME = 'my_ssd_mobnet'
PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
TF_RECORD_SCRIPT_NAME = 'generate_tfrecord.py'
LABEL_MAP_NAME = 'label_map.pbtxt'

paths = {
    'WORKSPACE_PATH': os.path.join('Tensorflow', 'workspace'),
    'SCRIPTS_PATH': os.path.join('Tensorflow','scripts'),
    'APIMODEL_PATH': os.path.join('Tensorflow','models'),
    'ANNOTATION_PATH': os.path.join('Tensorflow', 'workspace','annotations'),
    'IMAGE_PATH': os.path.join('Tensorflow', 'workspace','images'),
    'MODEL_PATH': os.path.join('Tensorflow', 'workspace','models'),
    'PRETRAINED_MODEL_PATH': os.path.join('Tensorflow', 'workspace','pre-trained-models'),
    'CHECKPOINT_PATH': os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME),
    'OUTPUT_PATH': os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'export'),
    'TFJS_PATH':os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfjsexport'),
    'TFLITE_PATH':os.path.join('Tensorflow', 'workspace','models',CUSTOM_MODEL_NAME, 'tfliteexport'),
    'PROTOC_PATH':os.path.join('Tensorflow','protoc')
}

files = {
    'PIPELINE_CONFIG':os.path.join('Tensorflow', 'workspace','models', CUSTOM_MODEL_NAME, 'pipeline.config'),
    'TF_RECORD_SCRIPT': os.path.join(paths['SCRIPTS_PATH'], TF_RECORD_SCRIPT_NAME),
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LABEL_MAP_NAME)
}

for path in paths.values():
    if not os.path.exists(path):
        os.system("mkdir -p {}".format(path))

if not os.path.exists(os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection')):
    os.system("git clone https://github.com/tensorflow/models {}".format(paths['APIMODEL_PATH']))
    print("Compile and Install Dependencies:")
    print("apt-get install protobuf-compiler")
    print("cd Tensorflow/models/research && protoc object_detection/protos/*.proto --python_out=. && cp object_detection/packages/tf2/setup.py . && python -m pip install .")
    quit()

VERIFICATION_SCRIPT = os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection', 'builders', 'model_builder_tf2_test.py')

if len(sys.argv) == 0 or sys.argv[1] == "test":
    print("Verify Dependencies:")
    print(VERIFICATION_SCRIPT)
    print("Run this to ensure all dependencies are satisfied, resolve any that aren't.")
    print("")
    quit()

import object_detection

if not os.path.exists(os.path.join(paths['PRETRAINED_MODEL_PATH'], PRETRAINED_MODEL_NAME+'.tar.gz')):
    os.system("wget {}".format(PRETRAINED_MODEL_URL))
    os.system("mv {} {}".format(PRETRAINED_MODEL_NAME+'.tar.gz', paths['PRETRAINED_MODEL_PATH']))
    os.system("tar -zxvf {} -C {}".format(os.path.join(paths['PRETRAINED_MODEL_PATH'], PRETRAINED_MODEL_NAME+'.tar.gz'), paths['PRETRAINED_MODEL_PATH']))

if not os.path.exists(os.path.join(paths['IMAGE_PATH'], train)) and not os.path.exists(os.path.join(paths['IMAGE_PATH'], test)):
    os.system("mkdir -p {}".format(os.path.join(paths['IMAGE_PATH'], train)))
    os.system("mkdir -p {}".format(os.path.join(paths['IMAGE_PATH'], test)))
    os.system("git clone https://github.com/R4g3D/anpr-data.git {}".format(paths['IMAGE_PATH']))
    os.system("mv {}/annotations/Cars{0..410}.* {}/images/Cars{0..410}.* {}/train/".format(paths['IMAGE_PATH'], paths['IMAGE_PATH'], paths['IMAGE_PATH']))
    os.system("mv {}/annotations/* {}/images/* {}/test/".format(paths['IMAGE_PATH'], paths['IMAGE_PATH'], paths['IMAGE_PATH']))
    os.system("rm -rf {}".format(paths['IMAGE_PATH'], anpr-data))

labels = [{'name':'licence', 'id':1}]

with open(files['LABELMAP'], 'w') as f:
    for label in labels:
        f.write('item { \n')
        f.write('\tname:\'{}\'\n'.format(label['name']))
        f.write('\tid:{}\n'.format(label['id']))
        f.write('}\n')

if not os.path.exists(files['TF_RECORD_SCRIPT']):
    os.system("git clone https://github.com/nicknochnack/GenerateTFRecord {}".format(paths['SCRIPTS_PATH']))
    os.system("sed -i 's/int(member\[4\]\[0\]\.text)/int(member\[5\]\[0\]\.text)/g' {}".format(files['TF_RECORD_SCRIPT']))
    os.system("sed -i 's/int(member\[4\]\[1\]\.text)/int(member\[5\]\[1\]\.text)/g' {}".format(files['TF_RECORD_SCRIPT']))
    os.system("sed -i 's/int(member\[4\]\[2\]\.text)/int(member\[5\]\[2\]\.text)/g' {}".format(files['TF_RECORD_SCRIPT']))
    os.system("sed -i 's/int(member\[4\]\[3\]\.text)/int(member\[5\]\[3\]\.text)/g' {}".format(files['TF_RECORD_SCRIPT']))

os.system("python {} -x {} -l {} -o {}".format(files['TF_RECORD_SCRIPT'], os.path.join(paths['IMAGE_PATH'], 'train'), files['LABELMAP'], os.path.join(paths['ANNOTATION_PATH'], 'train.record')))
os.system("python {} -x {} -l {} -o {}".format(files['TF_RECORD_SCRIPT'], os.path.join(paths['IMAGE_PATH'], 'test'), files['LABELMAP'], os.path.join(paths['ANNOTATION_PATH'], 'test.record')))

os.system("cp {} {}".format(os.path.join(paths['PRETRAINED_MODEL_PATH'], PRETRAINED_MODEL_NAME, 'pipeline.config'), os.path.join(paths['CHECKPOINT_PATH'])))

import tensorflow as tf
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format

config = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])

pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
with tf.io.gfile.GFile(files['PIPELINE_CONFIG'], "r") as f:
    proto_str = f.read()
    text_format.Merge(proto_str, pipeline_config)

pipeline_config.model.ssd.num_classes = len(labels)
pipeline_config.train_config.batch_size = 4
pipeline_config.train_config.fine_tune_checkpoint = os.path.join(paths['PRETRAINED_MODEL_PATH'], PRETRAINED_MODEL_NAME, 'checkpoint', 'ckpt-0')
pipeline_config.train_config.fine_tune_checkpoint_type = "detection"
pipeline_config.train_input_reader.label_map_path= files['LABELMAP']
pipeline_config.train_input_reader.tf_record_input_reader.input_path[:] = [os.path.join(paths['ANNOTATION_PATH'], 'train.record')]
pipeline_config.eval_input_reader[0].label_map_path = files['LABELMAP']
pipeline_config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [os.path.join(paths['ANNOTATION_PATH'], 'test.record')]

config_text = text_format.MessageToString(pipeline_config)
with tf.io.gfile.GFile(files['PIPELINE_CONFIG'], "wb") as f:
    f.write(config_text)

TRAINING_SCRIPT = os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection', 'model_main_tf2.py')

command = "python {} --model_dir={} --pipeline_config_path={} --num_train_steps=10000".format(TRAINING_SCRIPT, paths['CHECKPOINT_PATH'],files['PIPELINE_CONFIG'])

if sys.argv[1] == "train":
    print("Train Model:")
    print(command)
