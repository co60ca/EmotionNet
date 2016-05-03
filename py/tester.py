import runner
import sys

# like
# setup('ggn-net/deploy.prototxt',
# 'snapshots/ggn_full_crop_halfface_iter_56000.caffemodel')
runner.setup(sys.argv[1], sys.argv[2])

runner.class_imgs_to_csv(runner.all_dir(sys.argv[3]), sys.stdout)
