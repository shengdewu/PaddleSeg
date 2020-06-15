#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import os
import random

from paddle.fluid.io import Dataset

from utils.download import download_file_and_uncompress

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
URL = "https://paddleseg.bj.bcebos.com/dataset/optic_disc_seg.zip"


class OpticDiscSeg(Dataset):
    def __init__(self,
                 data_dir=None,
                 train_list=None,
                 val_list=None,
                 test_list=None,
                 shuffle='False',
                 mode='train',
                 transform=None,
                 download=True):
        self.data_dir = data_dir
        self.shuffle = shuffle
        self.transform = transform
        self.file_list = list()

        if mode.lower() not in ['train', 'eval', 'test']:
            raise Exception(
                "mode should be 'train', 'eval' or 'test', but got {}.".format(
                    mode))

        if transform is None:
            raise Exception("transform is necessary, but it is None.")

        self.data_dir = data_dir
        if self.data_dir is None:
            if not download:
                raise Exception("data_file not set and auto download disabled.")
            self.data_dir = download_file_and_uncompress(url=URL,
                                                         savepath=LOCAL_PATH,
                                                         extrapath=LOCAL_PATH)
            if mode == 'train':
                file_list = os.path.join(self.data_dir, 'train_list.txt')
            elif mode == 'eval':
                file_list = os.paht.join(self.data_dir, 'val_list.txt')
            else:
                file_list = os.path.join(self.data_dir, 'test_list.txt')
        else:
            if mode == 'train':
                file_list = train_list
            elif mode == 'eval':
                file_list = val_list
            else:
                file_list = test_list

        with open(file_list, 'r') as f:
            for line in f:
                items = line.strip().split()
                if len(items) != 2:
                    if mode == 'train' or mode == 'eval':
                        raise Exception(
                            "File list format incorrect! It should be"
                            " image_name label_name\\n")
                    image_path = os.path.join(self.data_dir, items[0])
                    grt_path = None
                else:
                    image_path = os.path.join(self.data_dir, items[0])
                    grt_path = os.path.join(self.data_dir, items[1])
                self.file_list.append([image_path, grt_path])
        if shuffle:
            random.shuffle(self.file_list)

    def __getitem__(self, idx):
        print(idx)
        image_path, grt_path = self.file_list[idx]
        return self.transform(im=image_path, label=grt_path)

    def __len__(self):
        return len(self.file_list)
