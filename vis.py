import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from pyqtgraph.Qt import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('3D Cube')
w.setCameraPosition(distance=10)

# Create cube vertices
verts = np.array([
    [-1,-1,-1], [ 1,-1,-1],
    [ 1, 1,-1], [-1, 1,-1],
    [-1,-1, 1], [ 1,-1, 1],
    [ 1, 1, 1], [-1, 1, 1]
])

# Define faces using vertex indices
faces = np.array([
    [0,1,2], [0,2,3],
    [4,5,6], [4,6,7],
    [0,1,5], [0,5,4],
    [2,3,7], [2,7,6],
    [1,2,6], [1,6,5],
    [0,3,7], [0,7,4]
])

colors = np.ones((faces.shape[0], 4))
colors[:,0] = 0.5

mesh = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False, drawEdges=True)
w.addItem(mesh)

sys.exit(app.exec_())