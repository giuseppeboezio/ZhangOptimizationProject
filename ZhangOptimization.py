import numpy as np
from numpy import linalg as la
import cv2


def process_corners(dir):
  #Load the image in greyscale color from the given directory path
  img=cv2.imread(dir,cv2.IMREAD_GRAYSCALE)

  #Set pattern size for openCv m=number corners in (columns,rows) coordinates
  #The  model proposed is always formed by 8x5 corners.
  pattern_size=(8,5)

  #Method that helps to find the corners into the image
  #And use a boolean variable found that is false in case of failure
  found , corners = cv2.findChessboardCorners(img, pattern_size)

  #If found is True then we use function cornerSubPix
  if found:
    #max_count=30 and criteria_eps_error=1 are the stop condition for define the corners
    term = (cv2.TERM_CRITERIA_EPS +  cv2.TERM_CRITERIA_COUNT , 30 ,1)
    #Redefine the corner positions
    cv2.cornerSubPix(img, corners, (5,5), (-1,-1), term)

  '''
  #Visualized found corners in the image
  vis=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
  cv2.drawChessboardCorners(vis, pattern_size, corners, found)
  #plt.imshow(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
  #plt.show()
  '''

  #Setting square size in mm
  square_size=28
  #Build che coordinates i,j of coordinates for each point 
  #Method np.indices return an array containing 2D arrays
  indices=np.indices(pattern_size, dtype = np.float32)
  #Get real 3D coordinates
  indices *= square_size
  #Put them in a correct way with the transpose
  coordinates_3D=np.transpose(indices, [2,1,0])
  coordinates_3D=coordinates_3D.reshape(-1,2)
  #Concatenate the third axis z that is equal to 0
  coordinates_3D_points = np.concatenate([coordinates_3D, np.ones([coordinates_3D.shape[0], 1], dtype=np.float32)], axis=-1)
  corners_points = corners.reshape(-1,2)
  corners_image_points = np.concatenate([corners_points, np.ones([corners_points.shape[0], 1], dtype=np.float32)], axis=-1)

  print(corners_image_points)
  print(coordinates_3D_points)

  return (corners_image_points, coordinates_3D_points)


def loss_function(m,H,w):
    # m is a matrix of points where rows are projective image points
    # H is the homography matrix
    # w is a matrix where rows are projective real points with only x y due to planar pattern
    sum = 0
    num_points = m.shape[0]
    for i in range(num_points):
        sum = sum + la.norm(m[i,:].T - H @ w[i,:].T,2)**2
    return sum


#Function for print only the values of the list of tuples
def printing(l):
    print('Value')
    for i in range(len(l)):
        print('{}'.format(l[i][0] , l[i][1]))


def centroid_calculation(simplex,loss_function,m,w):
    centroid = np.zeros(len(simplex)-1)
    for i in range(len(simplex)-1):
        centroid += simplex[i][1]
    centroid /= float( len(simplex)-1 )
    centroid_value = loss_function(m,np.reshape(centroid,(3,3)),w)

    return (centroid_value,centroid)


def reflection(worst,centroid,coeff,loss_function,m,w):
    reflection_point = centroid[1] * ( 1.0 + coeff ) - coeff * worst[1]
    reflection_value = loss_function(m, np.reshape(reflection_point,(3,3)) ,w)
    return (reflection_value, reflection_point)


def expansion(reflection,centroid,coeff,loss_function,m,w):
    expansion_point = centroid[1] * (1-coeff) + coeff*reflection[1]
    expansion_value = loss_function(m, np.reshape(expansion_point,(3,3)) ,w)
    return (expansion_value,expansion_point)


def contraction(worst,centroid,coeff,loss_function,m,w):
    contraction_point = centroid[1] * (1-coeff) + coeff*worst[1]
    contraction_value = loss_function(m, np.reshape(contraction_point,(3,3)), w)
    return (contraction_value,contraction_point)


def shrink(simplex,coeff,loss_function,m,w):
    for i in range (1,len(simplex)):
        shrink_point = (simplex[0][1]+simplex[i][1])/2
        shrink_value = loss_function(m, np.reshape(shrink_point, (3,3)), w)
        simplex[i] = (shrink_value, shrink_point)
    return simplex


def nelder_mead_optimizer(loss_function,m,w,start,max_it = 50,toll = 10e-6,reflect_coeff = 1.0,exp_coeff = 2.0,contract_coeff = 0.5,shrink_coeff = 0.5):
    #Create list of tuples (loss function value, vertex)
    simplex_list = []
    for i in range(len(start)):
        simplex_list.append( (loss_function(m, np.reshape(start[i],(3,3)), w) , start[i] )  )

    counter_it = 0
    best_value = 1

    while(counter_it<=max_it and best_value >= toll):
        counter_it += 1

        #Sorting wrt the loss_function value of vertices and assign the best/worst vertex to respectevely variables
        simplex_list = sorted(simplex_list, key= lambda pair: pair[0])
        best_tuple = simplex_list[0]
        second_worst_tuple = simplex_list[-2]
        worst_tuple = simplex_list[-1]

        #Find the centroid of the simplex
        centroid_tuple = centroid_calculation(simplex_list,loss_function,m,w)

        #Reflection
        reflection_tuple = reflection(worst_tuple,centroid_tuple,reflect_coeff,loss_function,m,w)
        #Reflection evaluation
        if( reflection_tuple[0] >= best_tuple[0] and reflection_tuple[0] < second_worst_tuple[0] ):
            #accept the reflection and impose the worst equal to the reflection_tuple
            simplex_list[-1] = reflection_tuple
            print("reflection")
        elif( reflection_tuple[0] < best_tuple[0]):
            #Expansion
            expansion_tuple = expansion(reflection_tuple,centroid_tuple,exp_coeff,loss_function,m,w)
            #Expansion evaluation
            if(expansion_tuple[0] < reflection_tuple[0]):
                #accept the expansion and impose the worst equal to the refletion_tuple
                simplex_list[-1] = expansion_tuple
                print("expansion")
            else:
                #accept the reflection and impose the worst equal to the reflection_tuple
                simplex_list[-1] = reflection_tuple
                print("reflection")
        elif(reflection_tuple[0]<worst_tuple[0] and reflection_tuple[0] >= second_worst_tuple[0]):
            #Contraction
            contraction_tuple = contraction(worst_tuple,centroid_tuple,contract_coeff,loss_function,m,w)
            #Contraction evaluation
            if(contraction_tuple[0] < worst_tuple[0]):
                #accept the contraction and impose the worst equal to the contraction_tuple
                simplex_list[-1] = contraction_tuple
                print("contraction")
            else:
                #Shrink and update the simplex_list
                simplex_list = shrink(simplex_list,shrink_coeff,loss_function,m,w)

    return simplex_list[0]

#Main
if __name__ == '__main__':
    #Set the name of the image file
    img = 'Chessboard.jpg'
    #Get m and w that represent respectively the image coordinates and the world coordinates already trasformed from R to P
    m , w = process_corners(img)
    #Call the function that will return the min value of H
    #Function that prints the points of the image and the projection error refering to the optimal H
    #TODO:-starting points
    #TODO:-call the nelder_mead function
    #TODO:-output





    