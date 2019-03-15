import multiprocessing as mp
import os

import numpy as np
from PIL import Image

from ksvd import ApproximateKSVD


def foo(im_name):
    solver = ApproximateKSVD(n_components=128, tol=1e-2, max_iter=2)
    stego_payload = ["005", "025", "050"]

    cover = Image.open(f"stego/000/{im_name}")
    cover_X = np.array(cover).astype('float')

    for payload in stego_payload:
        print(f"START {payload} {im_name}")
        stego = Image.open(f"stego/{payload}/{im_name}")
        stego_X = np.array(stego).astype('float')

        stego_dictionary = solver.fit(stego_X).components_
        cover_dictionary = solver.fit(cover_X).components_

        diff = cover_dictionary-stego_dictionary
        print(f"STOP {payload} {im_name}")

        with open(f'output/{payload}/{im_name}', 'w') as f:
            f.write(str(np.around(diff, 4).tolist()))


def main():
    pool = mp.Pool(4)
    picslist = os.listdir("stego/000")
    pool.map(foo, picslist)


if __name__ == "__main__":
    main()
