from copylot.hardware.orca_camera.camera import OrcaCamera

if __name__ == '__main__':
    camera = OrcaCamera()
    camera.live_capturing_and_show()
