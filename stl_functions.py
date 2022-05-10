import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
from matplotlib import image

def get_stl(filename):
    figure = plt.figure()
    axes = figure.add_subplot(111, projection='3d',azim=270,elev=0,proj_type='ortho')
    axes.dist = 6
    your_mesh = mesh.Mesh.from_file('./Photos/Overhang.stl')
    collection = axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
    collection.set_facecolor('yellow')
    collection.set_alpha(0.3)
    scale = your_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    plt.axis('off')
    axes.plot([0, 250], [0, 0], [0, 0], color='yellow', lw=0.1, alpha=1)
    # axes.plot([0, 0], [0, 0], [0, 10], color='yellow', lw=0.1, alpha=1)
    # axes.plot([250, 250], [0, 0], [0, 10], color='yellow', lw=0.1, alpha=1)
    plt.savefig('CAD_view.png', transparent=True, dpi=1500, bbox_inches='tight',pad_inches = 0)
    crop_image()

def crop_image():
    CAD_view = np.array(plt.imread('CAD_view.png'))

    shape = CAD_view.shape
    for i, j in enumerate(CAD_view[::-1]):
        if np.sum(j) != shape[1] * 3:
            bottom_bound = i-1
            # CAD_view = CAD_view[i:][::-1]
            break
    for i, j in enumerate(CAD_view):
        if np.sum(j) != shape[1] * 3:
            top_bound = i
            # CAD_view = CAD_view[i:]
            break
    for i in range(shape[1]):
        if np.sum(CAD_view[:,i]) != shape[0]*3:
            left_bound = i
            break
    for i in range(shape[1]-1,0,-1):
        if np.sum(CAD_view[:,i]) != shape[0]*3:
            right_bound = i
            break

    for i in range(shape[1]):
        if np.sum(CAD_view[:,i]) != shape[0]*3:
            left_bound = i
            break

    image.imsave('final_stl_image.png', CAD_view[top_bound:-(bottom_bound+1),left_bound+1:right_bound])

if __name__ == "__main__":
    get_stl("Photos/Overhang.stl")