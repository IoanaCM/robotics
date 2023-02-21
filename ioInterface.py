import numpy as np

#Global variables
map_size = 210          # Map size in cm
margin = 10             # Margin on web display in cm (cm*scale pixels)
scale = 3               # Scale on web interface (How many pixels per cm)
draw_arrows = False     # draw arrows on particles to show theta

def printMetrics(metrics):
    ((mu_x,mu_y,mu_theta),(sigma_x,sigma_y,sigma_theta)) = metrics
    mx = "{:.3f}".format(mu_x)
    my = "{:.3f}".format(mu_y)
    mt = "{:.3f}".format(mu_theta)
    sx = "{:.3f}".format(sigma_x)
    sy = "{:.3f}".format(sigma_y)
    st = "{:.3f}".format(sigma_theta)
    print(f"Mean position: (x={mx}, y={my}, theta={mt}), Standard Deviation: (x={sx}, y={sy}, theta={st})")


def drawLine(line):
    """
    Wrapper for web interface\n
    line :: 4-tuple (x0,y0,x1,y1) - robot coordinates of line
    """
    map_size = 210
    margin = 10
    scale = 3

    x0,y0,x1,y1 = line
    #transform from robot coordinates to screen coordinates
    tx0 = (x0 + margin) * scale
    ty0 = (-y0 + margin + map_size) * scale
    tx1 = (x1 + margin) * scale
    ty1 = (-y1 + margin + map_size) * scale
    graphic = (tx0,ty0,tx1,ty1)
    print("drawLine:" + str(graphic))
    return


def transformPoint(point):
    """
    converts point from robot coordinates to screen coordinates
    point :: tuple ((x,y,theta),weight)
    """
    ((x,y,theta), weight) = point

    return ((x + margin) * scale, (-y + margin + map_size) * scale, theta, weight)

def drawParticles(particles):
    """
    Wrapper for web interface\n
    particles :: list of tuples [((x,y,theta),weight)]
    """

    #transform from robot coordinates to screen coordinates
    transformed_particles = list(map(transformPoint, particles))
    print("drawParticles:" + str(transformed_particles))

    if draw_arrows:
      for p in particles:
        ((x,y,theta),_) = p
        drawLine((x, y, x + 3*np.cos(theta), y + 3*np.sin(theta)))

    return
