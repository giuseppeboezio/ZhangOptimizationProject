# ZhangOptimizationProject

This is a project for the second module of Combinatorial Decision Making and Optimization of the degree course of Artificial Intelligence at Alma Mater Studiorum (Bologna)

## Description
The purpose of the project is to minimize the reprojection error of the Zhang's method using two different optimization methods.

Zhang's method is used to understand which are the camera parameters which allow to correlate image points with real points. Optimization methods used in the project to solve the first step of Zhang's method are the followings:
* Nelder-Mead
* Particle Swarm Optimization

## Zhang's method - Refinement step for minimizing the reprojection error of the homography matrix
Camera calibration is the process whereby all parameters defining the camera model are as accurately as possible estimated for a specific cameradevice.

Camera calibration approach can rely on different images of one given planar pattern.

Given a planar chessboard pattern, known are:
* The number of internal corners of the pattern, different along the two orthogonal
directions for the sake of disambiguation (i.e. rows, columns).

* The size of the squares which form the pattern.

Internal corners can be detected easily by standard algorithms (e.g. the Harris corner detector, possibly with sub pixel refinement for improved accuracy).

<p align="center">
  <img heigth="350" width="350" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQn18pfdpPqYyrb-9bDyzdvca5ca06kLz7xqg&usqp=CAU">
</p>

The intersted part of camera calibration implemented in this project is the minimization step of the reprojection error looking for the best homography. The homography is a matrix which represents a general linear transformation between planes. Starting from a pseudorandom homography matrix (H) we use optimization methods in order to find H that minimizes the loss function of the reprojection error: 

<p align="center">
  <img heigth="350" width="350" src="formulae.PNG">
</p>

where:
* m are the image points in homogeneous coordinates (u,v,1)
* w are real points in homogeneous coordinates (x,y,z,1) but since the pattern is planar z = 0 for each point, so coordinates are (x,y,1)
* H is the homography matrix





## Nelder-Mead method

<img align="left" heigth="350" width="350" src="https://rodolfoferro.files.wordpress.com/2017/02/gif1.gif">

The method uses the concept of a simplex, which is a special polytope of n + 1 vertices in n dimensions. Examples of simplices include a line segment on a line, a triangle on a plane, a tetrahedron in three-dimensional space and so forth.

The method approximates a local optimum of a problem with n variables when the objective function varies smoothly and is unimodal.

The downhill simplex method now takes a series of steps, most steps just moving the point of the simplex where the function is largest (“highest point”) through the opposite face of the simplex to a lower point. These steps are called reflections, and they are constructed to conserve the volume of the simplex (and hence maintain its nondegeneracy). When it can do so, the method expands the simplex in one or another direction to take larger steps. When it reaches a “valley floor”, the method contracts itself in the transverse direction and tries to ooze down the valley. If there is a situation where the simplex is trying to “pass through the eye of a needle”, it contracts itself in all directions, pulling itself in around its lowest (best) point.

In this implementation has been used an adaptive Nelder-Mead method algorithm (ANMA) which allows to change coefficients according to the number of dimensions





## Particle Swarm Optimization (PSO) method

<img align="right" heigth="340" width="340" src="https://upload.wikimedia.org/wikipedia/commons/e/ec/ParticleSwarmArrowsAnimation.gif">

It optimizes a problem by iteratively trying to improve a candidate solution with regard to a given measure of quality. It solves a problem by having a population of candidate solutions, here dubbed particles, and moving these particles around in the search-space according to simple mathematical formula over the particle's position and velocity. Each particle's movement is influenced by its local best known position, but is also guided toward the best known positions in the search-space, which are updated as better positions are found by other particles. This is expected to move the swarm toward the best solutions.

In this implementation a local topology has been used to avoid a too fast convergence.

Moreover a sort of correlation breaking has been implemented each 1000 iterations to improve the search and avoiding a stuck in a local minimum position.


## Requirements
You need to have a Python version < 3.7 (we suggest to use an Anaconda environment with Python version 3.5) and installed the following libraries:
* OpenCV
* Numpy
* Matplotlib

## Suggestions for the creation of a working environment
Having corrected installed Anaconda on your PC you can follow this guide to create an environment that can execute the project:
* Open Anaconda Navigator
* Click on "Environments"
* Press "Create" button
* Insert the name and Python with version below 3.7 (we suggest 3.5)
* Wait for the creation and once the creation has ended open the prompt using these codes:

```console
activate <nameOfEnvironment>
conda install <nameOfPackage>
```
Do it for every package required accepting every installation step

## Run
### Install
Clone the repository
```console
git clone https://github.com/SalvoPisciotta/ZhangOptimizationProject.git
cd ZhangOptimizationProject
```

### Execute
From the project directory
```console
python main.py
```

## Group Members

|  Reg No.  |  Name     |  Surname  |     Email                              |    Username      |
| :-------: | :-------: | :-------: | :------------------------------------: | :--------------: |
|   985203  | Salvatore | Pisciotta | `salvatore.pisciotta2@studio.unibo.it` | [_SalvoPisciotta_](https://github.com/SalvoPisciotta) |
|  1005271  | Giuseppe  | Boezio    | `giuseppe.boezio@studio.unibo.it`      | [_giuseppeboezio_](https://github.com/giuseppeboezio) |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
