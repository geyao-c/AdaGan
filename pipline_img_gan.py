from util import toolsf
import datetime
import os
import argparse
import time

"""
python image_gnrt.py --netG_path ./model/netG_iter50000.pth --gnrt_num 1000 --img_saved_dir ./result/image
"""

if __name__ == '__main__':
    gimg_root = './result/gnrted_img/'
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    gimg_root = os.path.join(gimg_root, now)

    AdaGAN_gimg_root = os.path.join(gimg_root, 'AdaGAN')
    WGAN_gimg_root = os.path.join(gimg_root, 'WGAN')

    # 这个文件夹下的模型都是20张源数据集图片训练得到的
    netG_root = '/home/lenovo/code/AdaGan/result/2022-08-24-10:41:28'
    AnetG_root = os.path.join(netG_root, 'AdaGan')
    WnetG_root = os.path.join(netG_root, 'WGAN')
    siter, delta, liter = 2500, 2500, 50000

    class_name_list = ["blister", "hydatoncus", "Demodicosis", "parakeratosis", "papillomatosis", "molluscum"]
    gnrt_num = 1000

    cmd_list = []
    while siter <= liter:
        start = time.time()
        for class_name in class_name_list:
            AnetG_path = os.path.join(AnetG_root, class_name, 'save_model', 'netG_iter{}.pth'.format(siter))
            WnetG_path = os.path.join(WnetG_root, class_name, 'save_model', 'netG_iter{}.pth'.format(siter))

            AdaGAN_gimg_dir = os.path.join(AdaGAN_gimg_root, str(siter), class_name)
            WGAN_gimg_dir = os.path.join(WGAN_gimg_root, str(siter), class_name)

            AdaGAN_gnrt_cmd = "python image_gnrt.py --netG_path {} --gnrt_num {} --img_saved_dir {}".format(
                AnetG_path, gnrt_num, AdaGAN_gimg_dir
            )
            WGAN_gnrt_cmd = "python image_gnrt.py --netG_path {} --gnrt_num {} --img_saved_dir {}".format(
                WnetG_path, gnrt_num, WGAN_gimg_dir
            )
            cmd_list.append(AdaGAN_gnrt_cmd)
            cmd_list.append(WGAN_gnrt_cmd)
        toolsf.execute_command(cmd_list)
        end = time.time()
        cmd_list = []
        print('siter{}图片已生成完毕, 耗时{:.2f}'.format(siter, end - start))
        siter += delta


